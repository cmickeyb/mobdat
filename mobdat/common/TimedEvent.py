#!/usr/bin/python
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

@file    TimedEvent.py
@author  Mic Bowman
@date    2014-03-31

This package defines modules for the mobdat simulation environment

"""

import os, sys, traceback
import logging

# we need to import python modules from the $SUMO_HOME/tools directory
sys.path.append(os.path.join(os.environ.get("OPENSIM","/share/opensim"),"lib","python"))
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "..")))
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "lib")))

from mobdat.common.Utilities import GenName
from mobdat.common.IntervalVariable import *
from mobdat.common.Constraint import *
from mobdat.common.TravelTimeEstimator import TravelTimeEstimator

logger = logging.getLogger(__name__)

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class TripEvent :
    def __init__(self, stime, splace, dplace) :
        self.StartTime = stime
        self.SrcName = splace.Details
        self.DstName = dplace.Details

    def __str__(self) :
        return 'travel from {0} to {1} starting at {2}'.format(self.SrcName, self.DstName, self.StartTime)

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class PlaceEvent :
    # -----------------------------------------------------------------
    def __init__(self, details, stimevar, etimevar, duration = 0.01, id = None) :
        self.Details = details
        self.EventStart = stimevar
        self.EventEnd = etimevar
        self.Duration = max(duration, 0.01)
        self.EventID = id or GenName('PLACE')

        self.Arrival = None
        self.Departure = None

    # -----------------------------------------------------------------
    def Split(self) :
        raise AttributeError("Event {0} of type {1} is not splittable".format(self.EventID, self.__class__.__name__))

    # -----------------------------------------------------------------
    def NextPlace(self) :
        return self.Departure.DstPlace if self.Departure else None

    # -----------------------------------------------------------------
    def PrevPlace(self) :
        return self.Arrival.SrcPlace if self.Arrival else None

    # -----------------------------------------------------------------
    def AddVariables(self, vstore) :
        vstore[self.EventStart.ID] = self.EventStart
        vstore[self.EventEnd.ID] = self.EventEnd

        if self.Departure :
            self.Departure.AddVariables(vstore)

    # -----------------------------------------------------------------
    def AddConstraints(self, cstore) :
        constraint = OrderConstraint(self.EventStart.ID, self.EventEnd.ID, self.Duration)
        cstore.append(constraint)

        if self.Departure :
            self.Departure.AddConstraints(cstore)

    # -----------------------------------------------------------------
    def DumpToLog(self) :
        logger.warn("[{0:10s}]: {1:8s} from {2} to {3}".format(self.EventID, self.Details, str(self.EventStart), str(self.EventEnd)))
        if self.Departure :
            self.Departure.DumpToLog()

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class HomeEvent(PlaceEvent) :

    # -----------------------------------------------------------------
    @staticmethod
    def Create(details, base, sinterval, einterval, minduration = 0.01) :
        svar = MinimumIntervalVariable(base + sinterval[0], base + sinterval[1])
        evar = MaximumIntervalVariable(base + einterval[0], base + einterval[1])

        return HomeEvent(details, svar, evar, minduration)

    # -----------------------------------------------------------------
    def __init__(self, details, stimevar, etimevar, duration = 0.01, id = None) :
        PlaceEvent.__init__(self, details, stimevar, etimevar, duration, id)

    # -----------------------------------------------------------------
    def Split(self) :
        svar = self.EventStart.Copy()
        evar = self.EventEnd.Copy()

        return self.__class__(self.Details, svar, evar, self.Duration)
    
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class WorkEvent(PlaceEvent) :

    # -----------------------------------------------------------------
    @staticmethod
    def Create(details, base, sinterval, einterval, minduration = 8.0, minsplit = 1.0) :
        svar = GaussianIntervalVariable(base + sinterval[0], base + sinterval[1])
        evar = GaussianIntervalVariable(base + einterval[0], base + einterval[1])

        work = WorkEvent(details, svar, evar, minduration)
        work.MinimumSplitDuration = minsplit

        return work
    
    # -----------------------------------------------------------------
    def __init__(self, details, stimevar, etimevar, duration = 0.01, id = None) :
        PlaceEvent.__init__(self, details, stimevar, etimevar, duration, id)

        self.MinimumSplitDuration = duration
        self.AggregateID = GenName('AGGREGATE')
        self.AggregateHead = True

    # -----------------------------------------------------------------
    def Split(self) :
        svar = self.EventStart.Copy()
        evar = self.EventEnd.Copy()

        event = self.__class__(self.Details, svar, evar, self.Duration)

        # propogate aggregate information
        event.MinimumSplitDuration = self.MinimumSplitDuration
        event.AggregateID = self.AggregateID
        event.AggregateHead = False

        return event

    # -----------------------------------------------------------------
    def AddVariables(self, vstore) :
        vstore[self.EventStart.ID] = self.EventStart
        vstore[self.EventEnd.ID] = self.EventEnd

        if self.Departure :
            self.Departure.AddVariables(vstore)

    # -----------------------------------------------------------------
    def _FindAggregateDuration(self) :
        evar = self.EventEnd
        total = self.Duration

        accum = 0
        travel = self.Departure
        while travel :
            accum += travel.Duration
            if travel.DstPlace.__class__ == self.__class__  and travel.DstPlace.AggregateID == self.AggregateID :
                evar = travel.DstPlace.EventEnd
                total += accum
                accum = 0
            else :
                accum += travel.DstPlace.Duration

            travel = travel.DstPlace.Departure
            
        return (evar, total)

    # -----------------------------------------------------------------
    def AddConstraints(self, cstore) :
        constraint = OrderConstraint(self.EventStart.ID, self.EventEnd.ID, self.MinimumSplitDuration)
        cstore.append(constraint)

        if self.AggregateHead :
            (evar, total) = self._FindAggregateDuration()
            constraint = OrderConstraint(self.EventStart.ID, evar.ID, total)
            cstore.append(constraint)

        if self.Departure :
            self.Departure.AddConstraints(cstore)

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class TravelEvent :
    DefaultDuration = 0.5

    # -----------------------------------------------------------------
    def __init__(self, srcplace, dstplace, estimator = None, id = None) :
        self.SrcPlace = srcplace
        self.DstPlace = dstplace
        self.Duration = estimator.ComputeTravelTime(srcplace.Details, dstplace.Details) if estimator else self.DefaultDuration
        self.EventID = id or GenName('TRAVEL')

    # -----------------------------------------------------------------
    def AddVariables(self, vstore) :
        if self.DstPlace :
            self.DstPlace.AddVariables(vstore)

    # -----------------------------------------------------------------
    def AddConstraints(self, cstore) :
        if self.DstPlace :
            self.DstPlace.AddConstraints(cstore)

            constraint = OrderConstraint(self.SrcPlace.EventEnd.ID, self.DstPlace.EventStart.ID, self.Duration)
            cstore.append(constraint)

    # -----------------------------------------------------------------
    def DumpToLog(self) :
        logger.warn("[{0:10s}]: travel from {1} to {2}".format(self.EventID, self.SrcPlace.Details, self.DstPlace.Details))
        if self.DstPlace :
            self.DstPlace.DumpToLog()

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class IntervalVariableStore(dict) :
    
    # -----------------------------------------------------------------
    def __init__(self, *args, **kwargs) :
        dict.__init__(self, *args, **kwargs)

    # -----------------------------------------------------------------
    def Copy(self) :
        newlist = IntervalVariableStore()
        for tvar in self.itervalues() :
            newlist[tvar.ID] = tvar.Copy(tvar.ID)

        return newlist

    # -----------------------------------------------------------------
    def StoreIsValid(self) :
        """ Determine if the store is in a consistent state
        
        Returns:
            True if all variables are still valid
        """
        for var in self.itervalues() :
            if not var.IsValid() :
                logger.debug('variable {0} is inconsistent; {1}'.format(var.ID, str(var)))
                return False

        return True

    # -----------------------------------------------------------------
    def StoreIsFixed(self) :
        """ Determine if all variables in the store have fixed their values
        
        Returns:
            True if all variables are fixed
        """
        for var in self.itervalues() :
            if not var.IsFixed() : return False

        return True

    # -----------------------------------------------------------------
    def FindFreeVariables(self) :
        """ Find the time variables with values that have not been
        set. Ignore invalid variables.
        
        Returns:
            A possibly empty list of variable identifiers
        """
        variables = []
        for var in self.itervalues() :
            if not var.IsFixed() : variables.append(var)
            
        return sorted(variables, key= lambda var : var.Priority, reverse=True)
        
    # -----------------------------------------------------------------
    def DumpToLog(self) :
        for tvar in sorted(self.values(), key= lambda tvar : tvar.IntervalStart) :
            logger.warn("{0:5s} {1}".format(tvar.ID, str(tvar)))
    

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class ConstraintStore(list) :

    # -----------------------------------------------------------------
    def __init__(self, *args) :
        list.__init__(self, args)

        self.LastPickedVariable = None

    # -----------------------------------------------------------------
    def DumpToLog(self, varstore) :
        for constraint in self :
            constraint.DumpToLog(varstore)

    # -----------------------------------------------------------------
    def ApplyConstraints(self, varstore) :
        """ Apply the list of constraints repeatedly until the variable
        space stabilizes. With float ranges there is some danger of this
        never stopping though that is unlikely.

        Returns:
            True if all constraints applied, False if there was a conflict
        """

        changed = True
        while changed :
            if not varstore.StoreIsValid() :
                return False

            changed = False
            for constraint in self :
                changed = constraint.Apply(varstore) or changed

        return varstore.StoreIsValid()

    # -----------------------------------------------------------------
    def SolveConstraints(self, varstore) :
        """ Apply constraints repeatedly until all variables have been given a value

        Args:
            varstore -- store of IntervalVariables over which constraints will be applied

        Returns:
            True if the variable store is valid after all variables have been given a value
        """
        if not self.ApplyConstraints(varstore) :
            logger.debug("resolution failed, no variable picked")
            return False

        variables = varstore.FindFreeVariables()
        for var in variables :
            var.PickValue()
            self.LastPickedVariable = var.ID

            # print "================================================================="
            # print "Pick variable {0} and set value to {1}".format(var.ID, var.IntervalStart)
            # print "================================================================="

            if not self.ApplyConstraints(varstore) :
                logger.debug("resolution failed, last picked variable is %s",self.LastPickedVariable)
                return False

        return True
        
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class TimedEventList :
    # -----------------------------------------------------------------
    def __init__(self, baseev, estimator = None) :
        """
        Args:
            baseev -- initialized PlaceEvent object that sets limits on time scope
        """
        self.Events = {}
        self.TravelTimeEstimator = estimator or TravelTimeEstimator()

        baseid = self.AddPlaceEvent(baseev)

        self.BaseEvent = self.Events[baseid]

    # -----------------------------------------------------------------
    @property
    def LastEvent(self) :
        event = self.BaseEvent
        while event.Departure :
            event = event.Departure.DstPlace

        return event

    # -----------------------------------------------------------------
    def FindEvents(self, pred) :
        result = []

        event = self.BaseEvent
        if pred(event) : result.append(event)
        
        while event.Departure :
            event = event.Departure.DstPlace
            if pred(event) : result.append(event)

        return result

    # -----------------------------------------------------------------
    def PrevPlaceID(self, eventid) :
        ev = self.Events[eventid].PrevPlace()
        return ev.EventID if ev else None

    # -----------------------------------------------------------------
    def NextPlaceID(self, eventid) :
        ev = self.Events[eventid].NextPlace()
        return ev.EventID if ev else None

    # -----------------------------------------------------------------
    def MoreTripEvents(self) :
        return self.BaseEvent.NextPlace()

    # -----------------------------------------------------------------
    def PopTripEvent(self) :
        stime = self.BaseEvent.EventEnd
        splace = self.BaseEvent
        dplace = self.BaseEvent.NextPlace()

        if not dplace :
            return None

        self.BaseEvent = dplace
        return TripEvent(stime, splace, dplace)

    # -----------------------------------------------------------------
    def AddPlaceEvent(self, event) :
        """ Create a PlaceEvent object from the parameters and save it in the list of events
        
        Args:
            event -- initialized PlaceEvent object
        Returns:
            The identifier of the newly created event
        """

        self.Events[event.EventID] = event
        return event.EventID

    # -----------------------------------------------------------------
    def InsertAfterPlaceEvent(self, id1, id2) :
        """Insert PlaceEvent id2 after the event id1. Create a travel event to move
        from the current location to the new one.

        Args:
            id1 -- string event identifier
            id2 -- string event identifier
        """

        ev1 = self.Events[id1]
        ev2 = self.Events[id2]

        if ev1.Departure :
            ev2.Departure = TravelEvent(ev2, ev1.Departure.DstPlace, estimator = self.TravelTimeEstimator)

        ev1.Departure = TravelEvent(ev1, ev2, estimator = self.TravelTimeEstimator)
        ev2.Arrival = ev1.Departure

        t1 = max(ev1.EventStart.IntervalStart, ev2.EventStart.IntervalStart)
        t2 = max(ev1.EventStart.IntervalEnd, ev2.EventStart.IntervalEnd)

        ev1.EventEnd = MaximumIntervalVariable(t1, t2, ev1.EventEnd.ID)

        return (id1, id2)

    # -----------------------------------------------------------------
    def InsertWithinPlaceEvent(self, idprev, idnew) :
        """Split event idprev and insert idnew into the middle. Create travel events to
        move from the current location to the new location and then back to the current location.
        The assumption is that self.EventStart.IntervalStart < place.EventStart.IntervalStart and
        place.EventEnd.IntervalEnd < self.EventEnd.IntervalEnd

        Args:
            idprev -- string event identifier
            idnew -- string event identifier
        """
        evprev = self.Events[idprev]
        evnew = self.Events[idnew]

        # this is really wrong, there should be a constraint across the two intervals
        # that ensures that the duration is consistent...
        # oldduration = evprev.Duration
        # if oldduration > 0.01 :
        #     evprev.Duration = oldduration / 2.0

        evnext = evprev.Split()
        idnext = self.AddPlaceEvent(evnext)

        # connect the next events destination to the previous events destination
        if evprev.Departure :
            evnext.Departure = TravelEvent(evnext, evprev.Departure.DstPlace, estimator = self.TravelTimeEstimator)

        # connect the previous event to the new event
        evnew.Arrival = evprev.Departure = TravelEvent(evprev, evnew, estimator = self.TravelTimeEstimator)

        # connect the new event to the next event
        evnext.Arrival = evnew.Departure = TravelEvent(evnew, evnext, estimator = self.TravelTimeEstimator)

        # abut the start of the next event to the new event
        evnext.EventStart = MinimumIntervalVariable(evnew.EventEnd.IntervalStart, evprev.EventEnd.IntervalEnd)

        # abut the end of the previous event to the new event
        evprev.EventEnd = MaximumIntervalVariable(evprev.EventStart.IntervalStart, evnew.EventStart.IntervalEnd)

        return (idprev, idnew, idnext)

    # -----------------------------------------------------------------
    def SolveConstraints(self) :
        # create the variable store for the events
        vstore = IntervalVariableStore()
        self.BaseEvent.AddVariables(vstore)

        # create all the constraints for the events
        cstore = ConstraintStore()
        self.BaseEvent.AddConstraints(cstore)

        # and now solve the whole mess
        return cstore.SolveConstraints(vstore)

    # -----------------------------------------------------------------
    def DumpToLogIntervalVariables(self) :
        vstore = IntervalVariableStore()
        self.BaseEvent.AddVariables(vstore)
        vstore.DumpToLog()

    # -----------------------------------------------------------------
    def DumpToLog(self) :
        self.BaseEvent.DumpToLog()

## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
if __name__ == '__main__' :

    ## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    ## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    def AddWorkEvent(evlist, event, days) :
        workEV = WorkEvent.Create('work', days * 24.0, (6.0, 9.0), (14.0, 17.0), 9.0)
        workID = evlist.AddPlaceEvent(workEV)
        evlist.InsertWithinPlaceEvent(event, workID)

        return workID

    ## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    ## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    def AddCoffeeBeforeWorkEvent(evlist, workevent, days) :
        """Add a PlaceEvent for coffee before a work event. This moves the
        coffee event as close as possible to the work event.
        """

        scoffee = MaximumIntervalVariable(days * 24.0 + 0.0, days * 24.0 + 24.0)
        ecoffee = MaximumIntervalVariable(days * 24.0 + 0.0, days * 24.0 + 24.0)
        idc = evlist.AddPlaceEvent(PlaceEvent('coffee', scoffee, ecoffee, 0.2))

        evlist.InsertAfterPlaceEvent(evlist.PrevPlaceID(workevent), idc)

        return idc

    ## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    ## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    def AddLunchToWorkEvent(evlist, workevent, days) :
        slunch = GaussianIntervalVariable(days * 24.0 + 11.5, days * 24.0 + 13.0)
        elunch = GaussianIntervalVariable(days * 24.0 + 12.5, days * 24.0 + 14.0)
        idl = evlist.AddPlaceEvent(PlaceEvent('lunch', slunch, elunch, 0.75))

        evlist.InsertWithinPlaceEvent(workevent, idl)

        return idl

    ## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    ## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    def AddRestaurantAfterWorkEvent(evlist, workevent, day) :
        sdinner = MinimumIntervalVariable(day * 24.0 + 0.0, day * 24.0 + 24.0)
        edinner = MinimumIntervalVariable(day * 24.0 + 0.0, day * 24.0 + 24.0)
        idr = evlist.AddPlaceEvent(PlaceEvent('dinner', sdinner, edinner, 1.5))

        evlist.InsertAfterPlaceEvent(workevent, idr)

        return idr

    ## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    ## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    def AddShoppingTrip(evlist, day, maxcount = 4, prevevent = None) :
        # happens between 7am and 10pm
        svar = GaussianIntervalVariable(day * 24.0 + 7.0, day * 24.0 + 22.0)
        evar = GaussianIntervalVariable(day * 24.0 + 7.0, day * 24.0 + 22.0)

        ids = evlist.AddPlaceEvent(PlaceEvent('shopping', svar, evar, 0.75))
        if prevevent :
            evlist.InsertAfterPlaceEvent(prevevent, ids)
        else :
            evlist.InsertWithinPlaceEvent(evlist.LastEvent.EventID, ids)
        
        stops = int(random.triangular(0, 4, 1))
        while stops > 0 :
            stops = stops - 1

            svar = MinimumIntervalVariable(day * 24.0 + 7.0, day * 24.0 + 22.0)
            evar = MinimumIntervalVariable(day * 24.0 + 7.0, day * 24.0 + 22.0)
            idnew = evlist.AddPlaceEvent(PlaceEvent('shopping', svar, evar, 0.5))
            evlist.InsertAfterPlaceEvent(ids, idnew)
            ids = idnew

    ## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    ## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    def BuildOneDay(evlist, day) :
        lastev = evlist.LastEvent.EventID
        workev = AddWorkEvent(evlist, lastev, day)

        if random.uniform(0.0, 1.0) > 0.6 :
            workev = evlist.FindEvents(lambda ev : ev.Details == 'work')[-1].EventID
            AddCoffeeBeforeWorkEvent(evlist, workev, day)

        if random.uniform(0.0, 1.0) > 0.8 :
            workev = evlist.FindEvents(lambda ev : ev.Details == 'work')[-1].EventID
            AddLunchToWorkEvent(evlist, workev, day)
        
        if random.uniform(0.0, 1.0) > 0.8 :
            workev = evlist.FindEvents(lambda ev : ev.Details == 'work')[-1].EventID
            dinnerev = AddRestaurantAfterWorkEvent(evlist, workev, day)
            if random.uniform(0.0, 1.0) > 0.7 :
                AddShoppingTrip(evlist, day, maxcount = 2, prevevent = dinnerev)
        else :
            if random.uniform(0.0, 1.0) > 0.9 :
                AddShoppingTrip(evlist, day)

    # -----------------------------------------------------------------
    clog = logging.StreamHandler()
    clog.setFormatter(logging.Formatter('>>> [%(name)s] %(message)s'))
    clog.setLevel(logging.DEBUG)
    logging.getLogger().addHandler(clog)


    for day in range(0, 1000) :
        homeev = HomeEvent.Create('home', 0.0, (0.0, 0.0), (24.0 * 1000.0, 24.0 * 1000.0))
        evlist = TimedEventList(homeev)

        print '---------- day = {0:4} ----------'.format(day)
        BuildOneDay(evlist, 0.0)
        # BuildOneDay(evlist, day)

        resolved = False
        try :
            resolved = evlist.SolveConstraints()
        except :
            logger.error('internal inconsistency detected; %s', traceback.format_exc(10))
            evlist.DumpToLog()
            sys.exit(1)

        if not resolved :
            logger.error('resolution failed for day %s', day)
            evlist.DumpToLog()
            sys.exit(1)

        while evlist.MoreTripEvents() :
            trip = evlist.PopTripEvent()
            print str(trip)

    # evlist.DumpToLog()

