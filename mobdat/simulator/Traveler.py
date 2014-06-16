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

@file    Traveler.py
@author  Mic Bowman
@date    2014-04-02

This module defines the SocialConnector class. This class implements
the social (people) aspects of the mobdat simulation.

"""

import os, sys
import logging

sys.path.append(os.path.join(os.environ.get("SUMO_HOME"), "tools"))
sys.path.append(os.path.join(os.environ.get("OPENSIM","/share/opensim"),"lib","python"))
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "lib")))

import random
import Trip

from mobdat.common import TravelTimeEstimator, TimedEvent, IntervalVariable
from mobdat.common import SocialDecoration

logger = logging.getLogger(__name__)

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class EventController :

    # -----------------------------------------------------------------
    def __init__(self) :
        self.CoffeeBeforeWork = 0.6
        self.LunchDuringWork = 0.5
        self.RestaurantAfterWork = 0.8
        self.ShoppingTrip = 0.8

    # -----------------------------------------------------------------
    def FireCoffeeBeforeWork(self, schedule) :
        return schedule.StartTime > 3.0 and schedule.StartTime < 10.0 and random.uniform(0.0, 1.0) > self.CoffeeBeforeWork

    # -----------------------------------------------------------------
    def FireLunchAtWork(self, schedule) :
        return schedule.StartTime < 11.0 and 14.5 < schedule.EndTime and random.uniform(0.0, 1.0) > self.LunchDuringWork


# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class Traveler :
    BusinessCache = {}

    # -----------------------------------------------------------------
    def __init__(self, person, connector) :
        """
        Args:
            person -- Graph.Node (NodeType == Person) or SocialNodes.Person
            connector -- SocialConnector
        """
        self.Connector = connector
        self.World = self.Connector.World

        self.Person = person
        self.Employer = self.Person.EmployedBy
        self.Job = self.Person.JobDescription

        self.InitializeLocationNameMap()
        self.TravelEstimator = TravelTimeEstimator.TravelTimeEstimator()

        self.Controller = EventController()
        self.BuildDailyEvents()
        self.ScheduleNextTrip()

    # -----------------------------------------------------------------
    def FindBusinessByType(self, biztype, bizclass) :
        if (biztype, bizclass) not in self.BusinessCache :
            predicate = SocialDecoration.BusinessProfileDecoration.BusinessTypePred(biztype, bizclass)
            self.BusinessCache[(biztype, bizclass)] = self.World.FindNodes(nodetype = 'Business', predicate = predicate)

        return random.choice(self.BusinessCache[(biztype, bizclass)])
    
    # -----------------------------------------------------------------
    def InitializeLocationNameMap(self) :
        self.LocationNameMap = {}
        self.LocationNameMap['home'] = self.Person
        self.LocationNameMap['work'] = self.Employer
        self.LocationNameMap['coffee'] = self.FindBusinessByType(SocialDecoration.BusinessType.Food, 'coffee')
        self.LocationNameMap['lunch'] = self.FindBusinessByType(SocialDecoration.BusinessType.Food, 'fastfood')

    # -----------------------------------------------------------------
    def ResolveLocationName(self, name) :
        return self.LocationNameMap[name].ResidesAt

    # -----------------------------------------------------------------
    def BuildDailyEvents(self, addextras = True) :
        homeev = TimedEvent.HomeEvent.Create('home', 0.0, (0.0, 0.0), (24.0 * 1000.0, 24.0 * 1000.0))
        evlist = TimedEvent.TimedEventList(homeev, estimator = self.TravelEstimator)

        worldday = int(self.Connector.WorldTime / 24.0)
        worldtime = worldday * 24.0

        jobdeviation = 2.0 if self.Job.FlexibleHours else 0.2

        lastev = evlist.LastEvent.EventID

        schedule = self.Job.Schedule.NextScheduledEvent(worldtime)
        if schedule.Day == worldday :
            workev = AddWorkEvent(evlist, lastev, schedule, deviation = jobdeviation)

            if addextras :
                if self.Controller.FireCoffeeBeforeWork(schedule) :
                    AddCoffeeBeforeWorkEvent(evlist, workev, worldtime)

                if self.Controller.FireLunchAtWork(schedule) :
                    AddLunchToWorkEvent(evlist, workev, worldtime)

        # attempt to solve the constraints, if it doesn't work, then try
        # again with just work
        if not evlist.SolveConstraints() :
            if addextras :
                self.BuildDailyEvents(False)
                return
            else :
                logger.warn('Failed to resolve schedule constraints for traveler %s', self.Person.Name)
                evlist.DumpToLog()
                return

        self.EventList = evlist

    # -----------------------------------------------------------------
    def ScheduleNextTrip(self) :
        if not self.EventList.MoreTripEvents() :
            self.BuildDailyEvents()

        while self.EventList.MoreTripEvents() :
            tripev = self.EventList.PopTripEvent()
            starttime = float(tripev.StartTime)

            # this just allows us to start in the middle of the day, traveler at work
            # will start at work rather than starting at home
            if starttime > self.Connector.WorldTime :
                source = self.ResolveLocationName(tripev.SrcName)
                destination = self.ResolveLocationName(tripev.DstName)
                self.Connector.AddTripToEventQueue(Trip.Trip(self, starttime, source, destination))

                logger.info('Scheduled trip from %s to %s', source.Name, destination.Name)
                return

        logger.info('No trip events for %s', self.Person.Name)

    # -----------------------------------------------------------------
    def TripCompleted(self, trip) :
        """
        TripCompleted -- event handler called by the connector when the trip is completed

        Args:
            trip -- initialized Trip object
        """
        self.TravelEstimator.SaveTravelTime(trip.Source, trip.Destination, self.Connector.WorldTime - trip.ActualStartTime)
        self.ScheduleNextTrip()

    # -----------------------------------------------------------------
    def TripStarted(self, trip) :
        pass

## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
def AddWorkEvent(evlist, event, schedule, deviation = 2.0) :
    duration = schedule.WorldEndTime - schedule.WorldStartTime
    sinterval = (schedule.WorldStartTime - deviation, schedule.WorldStartTime + deviation)
    einterval = (schedule.WorldEndTime - deviation, schedule.WorldEndTime + deviation)

    workEV = TimedEvent.WorkEvent.Create('work', 0.0, sinterval, einterval, duration)
    workID = evlist.AddPlaceEvent(workEV)
    evlist.InsertWithinPlaceEvent(event, workID)

    return workID

## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
def AddCoffeeBeforeWorkEvent(evlist, workevent, days) :
    """Add a PlaceEvent for coffee before a work event. This moves the
    coffee event as close as possible to the work event.
    """

    scoffee = IntervalVariable.MaximumIntervalVariable(days * 24.0 + 0.0, days * 24.0 + 24.0)
    ecoffee = IntervalVariable.MaximumIntervalVariable(days * 24.0 + 0.0, days * 24.0 + 24.0)
    idc = evlist.AddPlaceEvent(TimedEvent.PlaceEvent('coffee', scoffee, ecoffee, 0.2))

    evlist.InsertAfterPlaceEvent(evlist.PrevPlaceID(workevent), idc)

    return idc

## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
def AddLunchToWorkEvent(evlist, workevent, days) :
    slunch = IntervalVariable.GaussianIntervalVariable(days * 24.0 + 11.5, days * 24.0 + 13.0)
    elunch = IntervalVariable.GaussianIntervalVariable(days * 24.0 + 12.5, days * 24.0 + 14.0)
    idl = evlist.AddPlaceEvent(TimedEvent.PlaceEvent('lunch', slunch, elunch, 0.75))

    evlist.InsertWithinPlaceEvent(workevent, idl)

    return idl

## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
def AddRestaurantAfterWorkEvent(evlist, workevent, day) :
    sdinner = IntervalVariable.MinimumIntervalVariable(day * 24.0 + 0.0, day * 24.0 + 24.0)
    edinner = IntervalVariable.MinimumIntervalVariable(day * 24.0 + 0.0, day * 24.0 + 24.0)
    idr = evlist.AddPlaceEvent(TimedEvent.PlaceEvent('dinner', sdinner, edinner, 1.5))

    evlist.InsertAfterPlaceEvent(workevent, idr)

    return idr

## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
def AddShoppingTrip(evlist, day, maxcount = 4, prevevent = None) :
    # happens between 7am and 10pm
    svar = IntervalVariable.GaussianIntervalVariable(day * 24.0 + 7.0, day * 24.0 + 22.0)
    evar = IntervalVariable.GaussianIntervalVariable(day * 24.0 + 7.0, day * 24.0 + 22.0)

    ids = evlist.AddPlaceEvent(TimedEvent.PlaceEvent('shopping', svar, evar, 0.75))
    if prevevent :
        evlist.InsertAfterPlaceEvent(prevevent, ids)
    else :
        evlist.InsertWithinPlaceEvent(evlist.LastEvent.EventID, ids)

    stops = int(random.triangular(0, 4, 1))
    while stops > 0 :
        stops = stops - 1

        svar = IntervalVariable.MinimumIntervalVariable(day * 24.0 + 7.0, day * 24.0 + 22.0)
        evar = IntervalVariable.MinimumIntervalVariable(day * 24.0 + 7.0, day * 24.0 + 22.0)
        idnew = evlist.AddPlaceEvent(TimedEvent.PlaceEvent('shopping', svar, evar, 0.5))
        evlist.InsertAfterPlaceEvent(ids, idnew)
        ids = idnew
