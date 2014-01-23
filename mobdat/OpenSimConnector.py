#!/usr/bin/env python
"""
Copyright (c) 2014, Intel Corporation

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

* Redistributions of source code must retain the above copyright notice,
  this list of conditions and the following disclaimer. 

* Redistributions in binary form must reproduce the above copyright
  notice, this list of conditions and the following disclaimer in the
  documentation and/or other materials provided with the distribution. 

* Neither the name of Intel Corporation nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission. 

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER
OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE. 

@file    OpenSimConnector.py
@author  Mic Bowman
@date    2013-12-03

Simple test combining sumo traffic simulation and opensim 3d virtual world.

"""

import os, sys
import logging
import math

# we need to import python modules from the $SUMO_HOME/tools directory
sys.path.append(os.path.join(os.environ.get("SUMO_HOME"), "tools"))
sys.path.append(os.path.join(os.environ.get("OPENSIM","/share/opensim"),"lib","python"))
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "lib")))

import uuid
import OpenSimRemoteControl
import EventHandler, EventTypes, ValueTypes

import Queue, threading, time, platform
import random

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class OpenSimUpdateThread(threading.Thread) :

    # -----------------------------------------------------------------
    def __init__(self, workq, endpoint, capability, scene, vmap, binary = False) :
        threading.Thread.__init__(self)

        self.Logger = logging.getLogger(__name__)

        self.TotalUpdates = 0
        self.WorkQ = workq
        self.EndPoint = endpoint
        self.Capability = capability
        self.Scene = scene
        self.Vehicles = vmap
        self.Binary = binary

        # logfile = 'log%d' % (random.randint(0,1000))
        # self.OpenSimConnector = OpenSimRemoteControl.OpenSimRemoteControl(self.EndPoint, request = 'async', logfile = logfile)
        self.OpenSimConnector = OpenSimRemoteControl.OpenSimRemoteControl(self.EndPoint, request = 'async')
        self.OpenSimConnector.Capability = self.Capability
        self.OpenSimConnector.Scene = self.Scene
        self.OpenSimConnector.Binary = self.Binary

    # -----------------------------------------------------------------
    def run(self) :
        self.ProcessUpdatesLoop()
        
        updates = self.TotalUpdates
        messages = self.OpenSimConnector.MessagesSent
        mbytes = self.OpenSimConnector.BytesSent / 1000000.0
        self.Logger.info('%d updates sent to OpenSim in %d messages using %f MB',updates, messages, mbytes)

    # -----------------------------------------------------------------
    def ProcessUpdatesLoop(self) :
        while True :
            try :
                # wait synchronously for the first incoming request
                vname = self.WorkQ.get(True)
                if not vname :
                    return

                updates = [vname]
                self.WorkQ.task_done()

                count = 1

                # then grab everything thats in the queue
                while not self.WorkQ.empty() :
                    vname = self.WorkQ.get()
                    if not vname :
                        self.WorkQ.task_done()
                        return

                    updates.append(vname)
                    self.WorkQ.task_done()

                    count += 1
                    if count >= 50 :
                        break

                self.ProcessUpdates(updates)

            except Queue.Empty as detail :
                pass

    # -----------------------------------------------------------------
    def ProcessUpdates(self, vnames) :
        # print 'sending %d updates' % (len(vnames))

        updates = []
        for vname in vnames :
            if vname not in self.Vehicles :
                self.Logger.warn("missing vehicle %s in update thread" % (vname))
                continue

            vehicle = self.Vehicles[vname]
            vid = vehicle.VehicleID
            vpos = vehicle.Position.ToList()
            vvel = vehicle.Velocity.ToList()
            vrot = vehicle.Rotation.ToList()
            vacc = vehicle.Acceleration.ToList()
            update = OpenSimRemoteControl.BulkUpdateItem(vid, vpos, vvel, vrot, vacc)
            updates.append(update)
            vehicle.InUpdateQueue = False

        count = len(updates)
        if count > 0 :
            self.TotalUpdates += count
            result = self.OpenSimConnector.BulkDynamics(updates)


# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class OpenSimVehicleDynamics :

    # -----------------------------------------------------------------
    @staticmethod
    def ComputeVelocity(velocity, acceleration, deltat) :
        return velocity + aceleration * deltat
    
    # -----------------------------------------------------------------
    @staticmethod
    def ComputePosition(position, velocity, acceleration, deltat) :
        return position + velocity * deltat + aceleration * (0.5 * deltat * deltat)

    # -----------------------------------------------------------------
    @staticmethod
    def CreateTweenUpdate(oldpos, newpos, deltat) :
        """
        Compute the dynamics (position, velocity and acceleration) that occurs
        at a time between two update events.
        """

        # this is the average acceleration over the time interval
        acceleration = newpos.Velocity.SubVector(oldpos.Velocity) / deltat

        tween = OpenSimVehicleDynamics()
        tween.Position = ComputePosition(oldpos.Position, oldpos.Velocity, acceleration, 0.5 * deltat)
        tween.Velocity = ComputeVelocity(oldpos.Velocity, acceleration, 0.5 * deltat)
        tween.Rotation = newpos.Rotation # this is just wrong but i dont like quaternion math
        tween.Acceleration = acceleration
        tween.UpdateTime = oldpos.UpdateTime + 0.5 * deltat
        return tween

    # -----------------------------------------------------------------
    def __init__(self) :
        self.Position = ValueTypes.Vector3()
        self.Velocity = ValueTypes.Vector3()
        self.Acceleration = ValueTypes.Vector3()
        self.Rotation = ValueTypes.Quaternion()
        self.UpdateTime = 0

    # -----------------------------------------------------------------
    def InterpolatePosition(self, deltat) :
        return ComputePosition(self.Position, self.Velocity, self.Acceleration, deltat)
    

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class OpenSimVehicle :

    # -----------------------------------------------------------------
    def __init__(self, vname, vehicle) :
        self.VehicleName = vname # Name of the sumo vehicle
        self.VehicleID = vehicle  # UUID of the vehicle object in OpenSim

        self.LastUpdate = OpenSimVehicleDynamics()
        self.TweenUpdate = OpenSimVehicleDynamics()

        self.InUpdateQueue = False

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class OpenSimConnector(EventHandler.EventHandler) :

    # -----------------------------------------------------------------
    def __init__(self, evrouter, settings) :
        """Initialize the OpenSimConnector by creating the opensim remote control handlers.

        Keyword arguments:
        evhandler -- the initialized event handler, EventRegistry type
        settings -- dictionary of settings from the configuration file
        """

        EventHandler.EventHandler.__init__(self, evrouter)

        self.Logger = logging.getLogger(__name__)

        # Get the world size
        wsize =  settings["OpenSimConnector"]["WorldSize"]
        self.WorldSize = ValueTypes.Vector3(wsize[0], wsize[1], wsize[2])

        woffs = settings["OpenSimConnector"]["WorldOffset"]
        self.WorldOffset = ValueTypes.Vector3(woffs[0], woffs[1], woffs[2])

        # Initialize the vehicle and vehicle types
        self.Vehicles = {}
        self.VehicleTypes = {}
        for vtype in settings["VehicleTypes"] :
            self.VehicleTypes[vtype["Name"]] = vtype

        # Initialize some of the update control variables
        self.PositionDelta = settings["OpenSimConnector"].get("PositionDelta",0.1)
        self.VelocityDelta = settings["OpenSimConnector"].get("VelocityDelta",0.1)
        self.AccelerationDelta = settings["OpenSimConnector"].get("AcclerationDelta",0.1)
        self.Interpolated = 0

        # Setup the remote control object
        if 'Capability' not in settings["OpenSimConnector"] :
            self.Logger.error("missing or expired opensim remote control capability")
            sys.exit(-1)

        self.Capability = uuid.UUID(settings["OpenSimConnector"]["Capability"])
        self.EndPoint = settings["OpenSimConnector"]["EndPoint"]
        self.AsyncEndPoint = settings["OpenSimConnector"]["AsyncEndPoint"]
        self.Scene = settings["OpenSimConnector"]["Scene"]
        self.Binary = settings["OpenSimConnector"].get("Binary",False)

        self.UpdateThreadCount = settings["OpenSimConnector"].get("UpdateThreadCount",2)

        self.DumpCount = 50
        self.CurrentStep = 0
        self.CurrentTime = 0
        self.AverageClockSkew = 0.0
        self.AverageQueueLength = 0.0

        self.Clock = time.time

        ## this is an ugly hack because the cygwin and linux
        ## versions of time.clock seem seriously broken
        if platform.system() == 'Windows' :
            self.Clock = time.clock

    # -----------------------------------------------------------------
    def HandleCreateObjectEvent(self,event) :
        vtype = self.VehicleTypes[event.ObjectType]
        vname = event.ObjectIdentity

        vehicle = uuid.uuid4()
        result = self.OpenSimConnector.CreateObject(vtype["AssetID"], objectid=vehicle, name=vname, parm=vtype.get("StartParam","{}"))

        self.Vehicles[vname] = OpenSimVehicle(vname,str(vehicle))

        # print "Created vehicle " + str(vname) + " with id " + str(vehicle)
        return True

    # -----------------------------------------------------------------
    def HandleDeleteObjectEvent(self,event) :
        vname = event.ObjectIdentity
        vehicleID = self.Vehicles[vname].VehicleID

        result = self.OpenSimConnector.DeleteObject(vehicleID)
        del self.Vehicles[vname]

        # print "Deleted vehicle " + vname + " with id " + str(vehicle)
        return True

    # -----------------------------------------------------------------
    def HandleObjectDynamicsEvent(self,event) :
        vname = event.ObjectIdentity
        if vname not in self.Vehicles :
            self.Logger.warn("attempt to update unknown vehicle %s" % (vname))
            return True

        vehicle = self.Vehicles[vname]

        deltat = self.CurrentTime - vehicle.LastUpdate.UpdateTime
        if deltat == 0 : return True

        # Save the dynamics information, acceleration is only needed in the tween update
        update = OpenSimVehicleDynamics()
        update.Position = event.ObjectPosition.ScaleVector(self.WorldSize).AddVector(self.WorldOffset)
        update.Velocity = event.ObjectVelocity.ScaleVector(self.WorldSize)
        update.Rotation = event.Rotation
        update.UpdateTime = self.CurrentTime

        # Compute the tween update (the update halfway between the last reported position and
        # the current reported position, with the tween we know the acceleration as opposed to
        # the current update where we dont know acceleration
        tween = OpenSimVehicleDynamics.CreateTweenUpdate(vehicle.LastUpdate, update, deltat)

        # if the vehicle is already in the queue then just save the new values
        # and call it quits
        if vehicle.InUpdateQueue :
            vehicle.TweenUpdate = tween
            vehicle.LastUpdate = update
            return True

        # check to see if the change in position or velocity is signficant enough to
        # warrant sending an update, emphasize velocity changes because dead reckoning
        # will handle position updates reasonably if the velocity is consistent

        # Condition 1: this is not the first update
        if vehicle.UpdateTime > 0 :
            # Condition 2: the acceleration is about the same
            if vehicle.TweenUpdate.Acceleration.ApproxEquals(tween.Acceleration, self.AccelerationDelta) :
                # Condition 3: the position check, need to handle lane changes so this check
                # is not redundant with acceleration check
                ipos = vehicle.TweenUpdate.InterpolatePosition(deltat)
                if ipos.ApproxEquals(tween.Position,self.PositionDelta) :
                    self.Interpolated += 1
                    return True
            
        vehicle.TweenUpdate = tween
        vehicle.LastUpdate = update
        vehicle.InUpdateQueue = True

        # if self.WorkQ.full() :
        #     print "full queue at time step %d" % (self.CurrentStep)

        self.WorkQ.put(vname)

        # print "Moved vehicle " + vname + " with id " + str(vehicle) + " to location " + str(position)
        return True

    # -----------------------------------------------------------------
    # Returns True if the simulation can continue
    def HandleTimerEvent(self, event) :
        self.CurrentStep = event.CurrentStep
        self.CurrentTime = event.CurrentTime

        # Compute the clock skew
        self.AverageClockSkew = (9.0 * self.AverageClockSkew + (self.Clock() - self.CurrentTime)) / 10.0

        # Compute weighted average queue length
        self.AverageQueueLength = (9.0 * self.AverageQueueLength + self.WorkQ.qsize()) / 10.0

        # Send the event if we need to
        if (self.CurrentStep % self.DumpCount) == 0 :
            event = EventTypes.OpenSimConnectorStatsEvent('OpenSimConnector', self.CurrentStep, self.AverageClockSkew, self.AverageQueueLength)
            self.PublishEvent(event)

    # -----------------------------------------------------------------
    def HandleShutdownEvent(self, event) :
        # clean up all the outstanding vehicles
        for vehicle in self.Vehicles.itervalues() :
            self.OpenSimConnector.DeleteObject(vehicle.VehicleID)

        # print 'waiting for update thread to terminate'
        for count in range(self.UpdateThreadCount) :
            self.WorkQ.put(None)

        for count in range(self.UpdateThreadCount) :
            self.UpdateThreads[count].join()

        self.Logger.info('create/delete messages sent to opensim: %d', self.OpenSimConnector.MessagesSent)
        self.Logger.info('%d vehicles interpolated correctly', self.Interpolated)
        self.Logger.info('shut down')

    # -----------------------------------------------------------------
    def SimulationStart(self) :
        self.OpenSimConnector = OpenSimRemoteControl.OpenSimRemoteControl(self.EndPoint, request = 'async')
        self.OpenSimConnector.Capability = self.Capability
        self.OpenSimConnector.Scene = self.Scene

        # Connect to the event registry
        self.SubscribeEvent(EventTypes.EventCreateObject, self.HandleCreateObjectEvent)
        self.SubscribeEvent(EventTypes.EventDeleteObject, self.HandleDeleteObjectEvent)
        self.SubscribeEvent(EventTypes.EventObjectDynamics, self.HandleObjectDynamicsEvent)
        self.SubscribeEvent(EventTypes.TimerEvent, self.HandleTimerEvent)
        self.SubscribeEvent(EventTypes.ShutdownEvent, self.HandleShutdownEvent)

        # Start the worker threads
        self.WorkQ = Queue.Queue(0)
        self.UpdateThreads = []
        for count in range(self.UpdateThreadCount) :
            thread = OpenSimUpdateThread(self.WorkQ, self.EndPoint, self.Capability, self.Scene, self.Vehicles, self.Binary)
            thread.start()
            self.UpdateThreads.append(thread)

        # all set... time to get to work!
        self.HandleEvents()

