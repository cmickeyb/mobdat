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
import subprocess

sys.path.append(os.path.join(os.environ.get("SUMO_HOME"), "tools"))
sys.path.append(os.path.join(os.environ.get("OPENSIM","/share/opensim"),"lib","python"))
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "lib")))

import math, random, heapq
import BaseConnector, EventRouter, EventHandler, EventTypes

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class Traveler :
    def __init__(self, person) :
        self.Person = person
        self.CurrentLocation = self.Person.Residence

        self.CommonTrips = {}

    # def NextTrip(self) :
    #     if self.CurrentLocation == self.Person.Residence :
            

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class Trip :
    VehicleNumber = 0

    def __init__(self, stime, vtype, traveler, source, destination) :
        self.StartTime = stime
        self.VehicleType = vtype
        self.Traveler = traveler
        self.Source = source
        self.Destination = destination

        Trip.VehicleNumber += 1
        self.VehicleName = "car%i" % Trip.VehicleNumber

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class SocialConnector(EventHandler.EventHandler, BaseConnector.BaseConnector) :
           
    # -----------------------------------------------------------------
    def __init__(self, evrouter, settings, dbbindings, netsettings) :
        EventHandler.EventHandler.__init__(self, evrouter)
        BaseConnector.BaseConnector.__init__(self, settings, dbbindings, netsettings)

        self.__Logger = logging.getLogger(__name__)

        self.VehicleNumber = 1
        self.VehicleMap = {}
        self.VehicleTypeMap = {}

        self.EventQ = []

        self.Travelers = {}
        self._CreateTravelers()

        self.CurrentStep = 0

    # -----------------------------------------------------------------
    def AddTripToEventQueue(self, trip) :
        heapq.heappush(self.EventQ, [trip.StartTime, trip])

    # -----------------------------------------------------------------
    def _CreateTravelers(self) :
        for person in self.PerInfo.PersonList :
            self.Travelers[person.Name] = Traveler(person)

    # -----------------------------------------------------------------
    def _GenerateTripStatsEvent(self, trip) :
        pname = trip.Person.Name
        sname = trip.Source.Name
        dname = trip.Destination.Name
        duration = self.GetWorldTime(self.CurrentStep) - trip.StartTime

        event = EventTypes.TripLengthStatsEvent(self.CurrentStep, duration, pname, sname, dname)
        self.PublishEvent(event)

    # -----------------------------------------------------------------
    def _GenerateAddVehicleEvent(self, trip) :
        """
        _GenerateAddVehicleEvent -- generate an AddVehicle event to initiate trip simulation

        trip -- Trip object initialized with traveler, vehicle and destination information
        """

        vname = str(trip.VehicleName)
        vtype = str(trip.VehicleType)
        rname = str(trip.Source.DestinationName)
        tname = str(trip.Destination.SourceName)

        # save the trip so that when the vehicle arrives we can get the trip
        # that caused the car to be created
        self.VehicleMap[vname] = trip

        event = EventTypes.EventAddVehicle(vname, vtype, rname, tname)
        self.PublishEvent(event)

    # -----------------------------------------------------------------
    def HandleDeleteObjectEvent(self, event) :
        vname = event.ObjectIdentity
        
        trip = self.VehicleMap[vname]
        del self.VehicleMap[vname]

        self._GenerateTripStatsEvent(trip)

        traveler = trip.Traveler
        traveler.CurrentLocation = trip.Destination

        self.AddTripToEventQueue(traveler.GetNextTrip())

    # -----------------------------------------------------------------
    def HandleTimerEvent(self, event) :
        self.CurrentStep = event.CurrentStep

        currenttime = self.GetWorldTime(event.CurrentStep)

        while self.EventQ :
            if self.EventQ[0][0] > currenttime : break
            self._GenerateAddVehicleEvent(heapq.heappop(self.EventQ))

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

