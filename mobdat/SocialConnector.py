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

import os, sys, warnings
import subprocess

sys.path.append(os.path.join(os.environ.get("SUMO_HOME"), "tools"))
sys.path.append(os.path.join(os.environ.get("OPENSIM","/share/opensim"),"lib","python"))
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "lib")))

import math, random, json, heapq
import EventRouter, EventHandler, EventTypes


# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class VehicleType :
    
    def __init__(self, vinfo) :
        self.Name = vinfo["Name"]
        self.Rate = vinfo["Rate"]
        self.SourceNodeTypes = vinfo["SourceNodeTypes"]
        self.DestinationNodeTypes = vinfo["DestinationNodeTypes"]

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class InjectionNode :
    def __init__(self, info) :
        try :
            self.Name = info["Name"]
            self.Type = info["Type"]
            self.InEdge = info["InEdge"]
            self.OutRoute = info["OutRoute"]
            self.Available = True
        except :
            warnings.warn('failed to extract injection point data; %s' % (sys.exc_info()[0]))
            sys.exit(-1)

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class Person :
    Count = 0
    NameFormat = "person{0}"

    def __init__(self, resnodes, biznodes, vehicles) :
        Person.Count = Person.Count + 1
        self.Name = Person.NameFormat.format(Person.Count)
        self.Home = random.choice(resnodes)
        self.Work = random.choice(biznodes)
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
class SocialConnector(EventHandler.EventHandler) :
           
    # -----------------------------------------------------------------
    def __init__(self, evrouter, settings) :
        EventHandler.EventHandler.__init__(self, evrouter)

        self.VehicleNumber = 1
        self.VehicleMap = {}

        self.FinalStep = settings["General"]["TimeSteps"] - 200
        self.InjectionRate = settings["SocialConnector"].get("InjectionRate",1.0)
        self.PeopleCount = settings["SocialConnector"].get("PeopleCount",300)
        self.WaitMean = settings["SocialConnector"].get("WaitMean",300.0)
        self.WaitSigma = settings["SocialConnector"].get("WaitSigma",50.0)

        self._CreateVehicleTypeMap(settings["VehicleTypes"])
        self._CreateNodeTypeMap(settings["SocialConnector"]["NodeDataFile"])
        self._CreatePeople()

        self.CurrentStep = 0

    # -----------------------------------------------------------------
    def _CreateVehicleTypeMap(self, vtypes) :
        self.VehicleTypeMap = {}

        for vinfo in vtypes :
            vtype = VehicleType(vinfo)
            
            for ntype in vtype.SourceNodeTypes :
                if ntype not in self.VehicleTypeMap :
                    self.VehicleTypeMap[ntype] = []

                # put vtype.Rate copies in the map so we can just use random.choice
                # to pick a vehicle when we need it
                count = vtype.Rate
                while count > 0 :
                    self.VehicleTypeMap[ntype].append(vtype)
                    count = count - 1

    # -----------------------------------------------------------------
    def _CreateNodeTypeMap(self, nfile) :
        self.NodeTypeMap = {}
        self.NodeNameMap = {}

        with open(nfile, 'r') as fp :
            nlist = json.load(fp)
            for ninfo in nlist :
                node = InjectionNode(ninfo)
                self.NodeNameMap[node.Name] = node
                if node.Type not in self.NodeTypeMap :
                    self.NodeTypeMap[node.Type] = []
                self.NodeTypeMap[node.Type].append(node)

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
        rname = str(person.CurrentLocation.OutRoute)
        tname = str(dnode.InEdge)

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
        if self.FinalStep > self.CurrentStep :
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

