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

import math, random, json, heapq
import BaseConnector, EventRouter, EventHandler, EventTypes
from mobdat.common import NetworkInfo, Decoration

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class Person :
    Count = 0
    NameFormat = "person{0}"

    def __init__(self, resnodes, biznodes, vehicles) :
        Person.Count = Person.Count + 1
        self.Name = Person.NameFormat.format(Person.Count)

        # pick a residence
        index = random.randint(0,len(resnodes) - 1)
        self.Home = resnodes[index]
        resnodes[index].Capacity = resnodes[index].Capacity - 1
        if resnodes[index].Capacity <= 0 :
            del resnodes[index]

        # pick a business
        index = random.randint(0,len(biznodes) - 1)
        self.Work = biznodes[index]
        biznodes[index].Capacity = biznodes[index].Capacity - 1
        if biznodes[index].Capacity <= 0 :
            del biznodes[index]

        self.VehicleType = random.choice(vehicles)
        self.CurrentLocation = self.Home

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class Trip :
    def __init__(self, stime, vname, person, source, destination) :
        self.StartTime = stime
        self.VehicleName = vname
        self.Person = person
        self.Source = source
        self.Destination = destination

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class SocialConnector(EventHandler.EventHandler, BaseConnector.BaseConnector) :
           
    # -----------------------------------------------------------------
    def __init__(self, evrouter, settings, netinfo, netsettings) :
        EventHandler.EventHandler.__init__(self, evrouter)
        BaseConnector.BaseConnector.__init__(self, settings)

        self.__Logger = logging.getLogger(__name__)

        # Save network information
        self.NetInfo = netinfo
        self.NetSettings = netsettings

        self.VehicleNumber = 1
        self.VehicleMap = {}
        self.VehicleTypeMap = {}
        self.NodeTypeMap = {}

        self.InjectionRate = settings["SocialConnector"].get("InjectionRate",1.0)
        self.PeopleCount = settings["SocialConnector"].get("PeopleCount",300)
        self.WaitMean = settings["SocialConnector"].get("WaitMean",300.0)
        self.WaitSigma = settings["SocialConnector"].get("WaitSigma",50.0)

        self._CreateVehicleTypeMap()
        self._CreateNodeTypeMap()
        self._CreatePeople()

        self.CurrentStep = 0

    # -----------------------------------------------------------------
    def _CreateVehicleTypeMap(self) :
        for vtype in self.NetSettings.VehicleTypes.itervalues() :

            for ntype in vtype.SourceIntersectionTypes :
                if ntype not in self.VehicleTypeMap :
                    self.VehicleTypeMap[ntype] = []

                # put vtype.Rate copies in the map so we can just use random.choice
                # to pick a vehicle when we need it
                count = vtype.Rate
                while count > 0 :
                    self.VehicleTypeMap[ntype].append(vtype)
                    count = count - 1

    # -----------------------------------------------------------------
    def _CreateNodeTypeMap(self) :
        for node in self.NetInfo.Nodes.itervalues() :
            if Decoration.EndPointDecoration.DecorationName not in node.Decorations :
                continue

            ntname = node.NodeType.Name
            if ntname not in self.NodeTypeMap :
                self.NodeTypeMap[ntname] = []

            self.NodeTypeMap[ntname].append(node)

        # make sure the people are more or less distributed evenly through the residences
        rescapacity = 1 + int(self.PeopleCount / len(self.NodeTypeMap['residence']))
        for node in self.NodeTypeMap['residence'] :
            node.Capacity = rescapacity

        # even distribution in the businesses is a little less important, will make this
        # more interesting in a bit
        buscapacity = 1 + int(self.PeopleCount / len(self.NodeTypeMap['business']))
        for node in self.NodeTypeMap['business'] :
            node.Capacity = 2 * buscapacity

    # -----------------------------------------------------------------
    def _CreatePeople(self) :
        
        self.EventQ = []

        rlist = self.NodeTypeMap['residence']
        blist = self.NodeTypeMap['business']
        vlist = self.VehicleTypeMap['residence']

        for i in range(0,self.PeopleCount - 1) :
            person = Person(rlist, blist, vlist)
            waittime = int(random.uniform(0, self.WaitMean * 2.0))

            heapq.heappush(self.EventQ,[waittime, person])

    # -----------------------------------------------------------------
    def _GenerateTripStatsEvent(self, trip) :
        pname = trip.Person.Name
        sname = trip.Source.Name
        dname = trip.Destination.Name
        duration = self.CurrentStep - trip.StartTime
        event = EventTypes.TripLengthStatsEvent(self.CurrentStep, duration, pname, sname, dname)
        self.PublishEvent(event)

    # -----------------------------------------------------------------
    def _GenerateVehicle(self, person, dnode) :
        self.VehicleNumber += 1
        vname = "car%i" % (self.VehicleNumber)
        vtype = str(person.VehicleType.Name)
        rname = str(person.CurrentLocation.EndPoint.DestinationName)
        tname = str(dnode.EndPoint.SourceName)

        self.VehicleMap[vname] = Trip(self.CurrentStep, vname, person, person.CurrentLocation, dnode)

        event = EventTypes.EventAddVehicle(vname, vtype, rname, tname)
        self.PublishEvent(event)

    # -----------------------------------------------------------------
    def GenerateVehicles(self, currentstep) :
        while self.EventQ :
            head = self.EventQ[0]
            if head[0] > currentstep :
                break

            waittime, person = heapq.heappop(self.EventQ)

            # pick a location, generally the person moves between home and work
            # though sometimes the person moves to a random residence or business
            p = random.uniform(0,1)
            if p < 0.5 :
                dest = person.Work if person.CurrentLocation == person.Home else person.Home
            elif p < 0.75 :
                dest = random.choice(self.NodeTypeMap['residence'])
            else :
                dest = random.choice(self.NodeTypeMap['business'])

            self._GenerateVehicle(person, dest)
            
    # -----------------------------------------------------------------
    def HandleDeleteObjectEvent(self, event) :
        vname = event.ObjectIdentity
        
        trip = self.VehicleMap[vname]
        del self.VehicleMap[vname]

        self._GenerateTripStatsEvent(trip)

        person = trip.Person
        person.CurrentLocation = trip.Destination

        waittime = self.CurrentStep + int(random.gauss(self.WaitMean,self.WaitSigma))
        heapq.heappush(self.EventQ, [waittime, person])

    # -----------------------------------------------------------------
    # Returns True if the simulation can continue
    def HandleTimerEvent(self, event) :
        self.CurrentStep = event.CurrentStep
        self.GenerateVehicles(self.CurrentStep)

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

