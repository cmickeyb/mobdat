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

@file    SocialConnector.py
@author  Mic Bowman
@date    2013-12-03

This module defines the SocialConnector class. This class implements
the social (people) aspects of the mobdat simulation.

"""

import os, sys
import logging

sys.path.append(os.path.join(os.environ.get("SUMO_HOME"), "tools"))
sys.path.append(os.path.join(os.environ.get("OPENSIM","/share/opensim"),"lib","python"))
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "lib")))

import heapq
import BaseConnector, EventRouter, EventHandler, EventTypes, Traveler, Trip

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class SocialConnector(EventHandler.EventHandler, BaseConnector.BaseConnector) :
           
    # -----------------------------------------------------------------
    def __init__(self, evrouter, settings, world, netsettings) :
        EventHandler.EventHandler.__init__(self, evrouter)
        BaseConnector.BaseConnector.__init__(self, settings, world, netsettings)

        self.__Logger = logging.getLogger(__name__)

        self.MaximumTravelers = int(settings["General"].get("MaximumTravelers", 0))
        self.TripCallbackMap = {}
        self.TripTimerEventQ = []

        self.Travelers = {}
        self.CreateTravelers()

        self.__Logger.warn('SocialConnector initialization complete')

    # -----------------------------------------------------------------
    def AddTripToEventQueue(self, trip) :
        heapq.heappush(self.TripTimerEventQ, trip)

    # -----------------------------------------------------------------
    def CreateTravelers(self) :
        #for person in self.PerInfo.PersonList.itervalues() :
        count = 0
        for name, person in self.World.IterNodes(nodetype = 'Person') :
            if count % 100 == 0 :
                self.__Logger.warn('%d travelers created', count)

            traveler = Traveler.Traveler(person, self)
            self.Travelers[name] = traveler

            count += 1
            if self.MaximumTravelers > 0 and self.MaximumTravelers < count :
                break

            
    # XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    # EVENT GENERATORS
    # XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

    # -----------------------------------------------------------------
    def GenerateTripBegEvent(self, trip) :
        """
        GenerateTripBegEvent -- create and publish a 'tripstart' event
        at the beginning of a trip
        
        trip -- object of type Trip
        """
        pname = trip.Traveler.Person.Name
        tripid = trip.TripID
        sname = trip.Source.Name
        dname = trip.Destination.Name

        event = EventTypes.TripBegStatsEvent(self.CurrentStep, pname, tripid, sname, dname)
        self.PublishEvent(event)


    # -----------------------------------------------------------------
    def GenerateTripEndEvent(self, trip) :
        """
        GenerateTripEndEvent -- create and publish an event to capture
        statistics about a completed trip
        
        trip -- a Trip object for a recently completed trip
        """
        pname = trip.Traveler.Person.Name
        tripid = trip.TripID
        sname = trip.Source.Name
        dname = trip.Destination.Name

        event = EventTypes.TripEndStatsEvent(self.CurrentStep, pname, tripid, sname, dname)
        self.PublishEvent(event)

    # -----------------------------------------------------------------
    def GenerateAddVehicleEvent(self, trip) :
        """
        GenerateAddVehicleEvent -- generate an AddVehicle event to start
        a new trip

        trip -- Trip object initialized with traveler, vehicle and destination information
        """

        vname = str(trip.VehicleName)
        vtype = str(trip.VehicleType)
        rname = str(trip.Source.Capsule.DestinationName)
        tname = str(trip.Destination.Capsule.SourceName)

        self.__Logger.debug('add vehicle %s from %s to %s',vname, rname, tname)

        # save the trip so that when the vehicle arrives we can get the trip
        # that caused the car to be created
        self.TripCallbackMap[vname] = trip

        event = EventTypes.EventAddVehicle(vname, vtype, rname, tname)
        self.PublishEvent(event)

    # XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    # EVENT HANDLERS
    # XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

    # -----------------------------------------------------------------
    def HandleDeleteObjectEvent(self, event) :
        """
        HandleDeleteObjectEvent -- delete object means that a car has completed its
        trip so record the stats and add the next trip for the person

        event -- a DeleteObject event object
        """

        vname = event.ObjectIdentity
        
        trip = self.TripCallbackMap.pop(vname)
        trip.TripCompleted(self)

    # -----------------------------------------------------------------
    def HandleTimerEvent(self, event) :
        """
        HandleTimerEvent -- timer event happened, process pending events from
        the eventq

        event -- Timer event object
        """
        self.CurrentStep = event.CurrentStep

        if self.CurrentStep % 100 == 0 :
            wtime = self.WorldTime
            qlen = len(self.TripTimerEventQ)
            stime = self.TripTimerEventQ[0].ScheduledStartTime if self.TripTimerEventQ else 0.0
            self.__Logger.info('at time %0.3f, timer queue contains %s elements, next event scheduled for %0.3f', wtime, qlen, stime)

        while self.TripTimerEventQ :
            if self.TripTimerEventQ[0].ScheduledStartTime > self.WorldTime :
                break

            trip = heapq.heappop(self.TripTimerEventQ)
            trip.TripStarted(self)

    # -----------------------------------------------------------------
    def HandleShutdownEvent(self, event) :
        pass

    # -----------------------------------------------------------------
    def SimulationStart(self) :
        self.SubscribeEvent(EventTypes.EventDeleteObject, self.HandleDeleteObjectEvent)
        self.SubscribeEvent(EventTypes.TimerEvent, self.HandleTimerEvent)
        self.SubscribeEvent(EventTypes.ShutdownEvent, self.HandleShutdownEvent)

        # all set... time to get to work!
        self.HandleEvents()
