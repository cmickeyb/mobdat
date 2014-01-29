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

@file    SumoConnector.py
@author  Mic Bowman
@date    2013-12-03

This file defines the SumoConnector class that translates mobdat events
and operations into and out of the sumo traffic simulator.

"""
import os, sys
import logging
import subprocess, threading, string, time, platform

sys.path.append(os.path.join(os.environ.get("SUMO_HOME"), "tools"))
sys.path.append(os.path.join(os.environ.get("OPENSIM","/share/opensim"),"lib","python"))
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "lib")))

from sumolib import checkBinary

import traci
import traci.constants as tc
import EventRouter, EventHandler, EventTypes
import ValueTypes

import math

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class SumoConnector(EventHandler.EventHandler) :

    # -----------------------------------------------------------------
    def __init__(self, evrouter, settings) :
        EventHandler.EventHandler.__init__(self, evrouter)

        self.Logger = logging.getLogger(__name__)

        # the sumo time scale is 1sec per iteration so we need to scale
        # to the 100ms target for our iteration time, this probably 
        # should be computed based on the target step size
        self.TimeScale = 1.0 / float(settings["General"]["Interval"])

        self.ConfigFile = settings["SumoConnector"]["ConfigFile"]
        self.Port = settings["SumoConnector"]["SumoPort"]
        self.TrafficLights = {}

        self.DumpCount = 50
        self.EdgesPerIteration = 25

        self.VelocityFudgeFactor = settings["SumoConnector"].get("VelocityFudgeFactor",0.90)

        self.AverageClockSkew = 0.0
        # self.LastStepTime = 0.0

        self.Clock = time.time

        ## this is an ugly hack because the cygwin and linux
        ## versions of time.clock seem seriously broken
        if platform.system() == 'Windows' :
            self.Clock = time.clock

        # for cf in settings["SumoConnector"].get("ExtensionFiles",[]) :
        #     execfile(cf,{"EventHandler" : self})

    # -----------------------------------------------------------------
    # -----------------------------------------------------------------
    def __NormalizeCoordinate(self,pos) :
        return ValueTypes.Vector3((pos[0] - self.XBase) / self.XSize, (pos[1] - self.YBase) / self.YSize, 0.0)

    # -----------------------------------------------------------------
    # see http://www.euclideanspace.com/maths/geometry/rotations/conversions/eulerToQuaternion/
    # where heading is interesting and bank and attitude are 0
    # -----------------------------------------------------------------
    def __NormalizeAngle(self,heading) :
        # convert to radians
        heading = (2.0 * heading * math.pi) / 360.0
        return ValueTypes.Quaternion.FromHeading(heading)

    # -----------------------------------------------------------------
    def __NormalizeVelocity(self, speed, heading) :
        # i'm not at all sure why the coordinates for speed are off
        # by 270 degrees... but this works
        heading = (2.0 * (heading + 270.0) * math.pi) / 360.0

        # the 0.9 multiplier just makes sure we dont overestimate
        # the velocity because of the time shifting, experience
        # is better if the car falls behind a bit rather than
        # having to be moved back because it got ahead
        x = self.VelocityFudgeFactor * self.TimeScale * speed * math.cos(heading)
        y = self.VelocityFudgeFactor * self.TimeScale * speed * math.sin(heading)

        return ValueTypes.Vector3(x / self.XSize, y / self.YSize, 0.0)

    # -----------------------------------------------------------------
    def _RecomputeRoutes(self) :
        if len(self.CurrentEdgeList) == 0 :
            self.CurrentEdgeList = list(self.EdgeList)

        count = 0
        while self.CurrentEdgeList and count < self.EdgesPerIteration :
            edge = self.CurrentEdgeList.pop()
            traci.edge.adaptTraveltime(edge, traci.edge.getTraveltime(edge)) 
            count += 1
    # # -----------------------------------------------------------------
    # def AddVehicle(self, vehid, routeid, typeid) :
    #     traci.vehicle.add(vehid, routeid, typeID=typeid)

    # # -----------------------------------------------------------------
    # def GetTrafficLightState(self, identity) :
    #     return traci.trafficlights.getReadYellowGreenState(identity)

    # # -----------------------------------------------------------------
    # def SetTrafficLightState(self, identity, state) :
    #     return traci.trafficlights.setRedYellowGreenState(identity, state)

    # -----------------------------------------------------------------
    def HandleTrafficLights(self, currentStep) :
        changelist = traci.trafficlights.getSubscriptionResults()
        for tl, info in changelist.iteritems() :
            state = info[tc.TL_RED_YELLOW_GREEN_STATE]
            if state != self.TrafficLights[tl] :
                self.TrafficLights[tl] = state
                event = EventTypes.EventTrafficLightStateChange(tl,state)
                self.PublishEvent(event)

    # -----------------------------------------------------------------
    def HandleInductionLoops(self, currentStep) :
        changelist = traci.inductionloop.getSubscriptionResults()
        for il, info in changelist.iteritems() :
            count = info[tc.LAST_STEP_VEHICLE_NUMBER]
            if count > 0 :
                event = EventTypes.EventInductionLoop(il,count)
                self.PublishEvent(event)

    # -----------------------------------------------------------------
    def HandleDepartedVehicles(self, currentStep) :
        dlist = traci.simulation.getDepartedIDList()
        for v in dlist :
            traci.vehicle.subscribe(v,[tc.VAR_POSITION, tc.VAR_SPEED, tc.VAR_ANGLE])

            vtype = traci.vehicle.getTypeID(v)
            event = EventTypes.EventCreateObject(v, vtype)
            self.PublishEvent(event)

    # -----------------------------------------------------------------
    def HandleArrivedVehicles(self, currentStep) :
        alist = traci.simulation.getArrivedIDList()
        for v in alist :
            event = EventTypes.EventDeleteObject(v)
            self.PublishEvent(event)

    # -----------------------------------------------------------------
    def HandleVehicleUpdates(self, currentStep) :
        changelist = traci.vehicle.getSubscriptionResults()
        for v, info in changelist.iteritems() :
            pos = self.__NormalizeCoordinate(info[tc.VAR_POSITION])
            ang = self.__NormalizeAngle(info[tc.VAR_ANGLE])
            vel = self.__NormalizeVelocity(info[tc.VAR_SPEED], info[tc.VAR_ANGLE])
            event = EventTypes.EventObjectDynamics(v, pos, ang, vel)
            self.PublishEvent(event)

    # -----------------------------------------------------------------
    # def HandleRerouteVehicle(self, event) :
    #     traci.vehicle.rerouteTraveltime(str(event.ObjectIdentity))
 
    # -----------------------------------------------------------------
    def HandleAddVehicleEvent(self, event) :
        traci.vehicle.add(event.ObjectIdentity, event.Route, typeID=event.ObjectType)
        traci.vehicle.changeTarget(event.ObjectIdentity, event.Target)

    # -----------------------------------------------------------------
    # Returns True if the simulation can continue
    def HandleTimerEvent(self, event) :
        self.CurrentStep = event.CurrentStep
        self.CurrentTime = event.CurrentTime

        # Compute the clock skew
        self.AverageClockSkew = (9.0 * self.AverageClockSkew + (self.Clock() - self.CurrentTime)) / 10.0

        # handle the time scale computation based on the inter-interval
        # times
        # if self.LastStepTime > 0 :
        #     delta = ctime - self.LastStepTime
        #     if delta > 0 :
        #         self.TimeScale = (9.0 * self.TimeScale + 1.0 / delta) / 10.0
        # self.LastStepTime = ctime

        try :
            traci.simulationStep()

            self.HandleInductionLoops(self.CurrentStep)
            self.HandleTrafficLights(self.CurrentStep)
            self.HandleDepartedVehicles(self.CurrentStep)
            self.HandleVehicleUpdates(self.CurrentStep)
            self.HandleArrivedVehicles(self.CurrentStep)
        except TypeError as detail: 
            self.Logger.error("[sumoconector] simulation step failed with type error %s" % (str(detail)))
            sys.exit(-1)
        except ValueError as detail: 
            self.Logger.error("[sumoconector] simulation step failed with value error %s" % (str(detail)))
            sys.exit(-1)
        except NameError as detail: 
            self.Logger.error("[sumoconector] simulation step failed with name error %s" % (str(detail)))
            sys.exit(-1)
        except AttributeError as detail: 
            self.Logger.error("[sumoconnector] simulation step failed with attribute error %s" % (str(detail)))
            sys.exit(-1)
        except :
            self.Logger.error("[sumoconnector] error occured in simulation step; %s" % (sys.exc_info()[0]))
            sys.exit(-1)

        self._RecomputeRoutes()

        if (event.CurrentStep % self.DumpCount) == 0 :
            count = traci.vehicle.getIDCount()
            event = EventTypes.SumoConnectorStatsEvent(self.CurrentStep, self.AverageClockSkew, count)
            self.PublishEvent(event)

        return True

    # -----------------------------------------------------------------
    def HandleShutdownEvent(self, event) :
        try :
            idlist = traci.vehicle.getIDList()
            for v in idlist : 
                traci.vehicle.remove(v)
        
            traci.close()
            sys.stdout.flush()

            self.SumoProcess.wait()
            self.Logger.info('shut down')
        except :
            exctype, value =  sys.exc_info()[:2]
            self.Logger.warn('shutdown failed with exception type %s; %s' %  (exctype, str(value)))

    # -----------------------------------------------------------------
    def SimulationStart(self) :
        sumoBinary = checkBinary('sumo')
        sumoCommandLine = [sumoBinary, "-c", self.ConfigFile]
        
        self.SumoProcess = subprocess.Popen(sumoCommandLine, stdout=sys.stdout, stderr=sys.stderr)
        traci.init(self.Port)

        self.SimulationBoundary = traci.simulation.getNetBoundary()
        self.XBase = self.SimulationBoundary[0][0]
        self.XSize = self.SimulationBoundary[1][0] - self.XBase
        self.YBase = self.SimulationBoundary[0][1]
        self.YSize = self.SimulationBoundary[1][1] - self.YBase

        # initialize the edge list, drop all the internal edges
        self.EdgeList = []
        for edge in traci.edge.getIDList() :
            # this is just to ensure that everything is initialized first time
            traci.edge.adaptTraveltime(edge, traci.edge.getTraveltime(edge)) 

            # only keep the "real" edges for computation for now
            if not edge.startswith(':') :
                self.EdgeList.append(edge)
        self.CurrentEdgeList = list(self.EdgeList)

        # initialize the traffic light state
        tllist = traci.trafficlights.getIDList()
        for tl in tllist :
            self.TrafficLights[tl] = traci.trafficlights.getRedYellowGreenState(tl)
            traci.trafficlights.subscribe(tl,[tc.TL_RED_YELLOW_GREEN_STATE])
        
        # initialize the induction loops
        illist = traci.inductionloop.getIDList()
        for il in illist :
            traci.inductionloop.subscribe(il, [tc.LAST_STEP_VEHICLE_NUMBER])

        # subscribe to the events
        self.SubscribeEvent(EventTypes.EventAddVehicle, self.HandleAddVehicleEvent)
        self.SubscribeEvent(EventTypes.TimerEvent, self.HandleTimerEvent)
        self.SubscribeEvent(EventTypes.ShutdownEvent, self.HandleShutdownEvent)

        # all set... time to get to work!
        self.HandleEvents()

