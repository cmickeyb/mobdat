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

import os, sys
import logging

# we need to import python modules from the $SUMO_HOME/tools directory
sys.path.append(os.path.join(os.environ.get("OPENSIM","/share/opensim"),"lib","python"))
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "..")))
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "lib")))

from mobdat.common.Utilities import GenName
from mobdat.common.TimeVariable import *
from mobdat.common.Constraint import *


# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class PlaceEvent :
    # -----------------------------------------------------------------
    def __init__(self, details, stimevar, etimevar, duration = 0.01, id = None) :
        self.Details = details
        self.STime = stimevar
        self.ETime = etimevar
        self.Duration = max(duration, 0.01)
        self.EventID = id or GenName('PLACE')

        self.Arrival = None
        self.Departure = None

    # -----------------------------------------------------------------
    def InsertAfterEvent(self, place) :
        """Insert a PlaceEvent after the current event. Create a travel event to move
        from the current location to the new one.

        Args:
            place -- a PlaceEvent, assumes that departure is not already set
        """

        if self.Departure :
            place.Departure = TravelEvent(place, self.Departure.DstPlace)

        self.Departure = TravelEvent(self, place)
        self.ETime = MaximumTimeVariable(place.STime.STime, place.STime.ETime)

    # -----------------------------------------------------------------
    def InsertWithinEvent(self, place) :
        """Insert a PlaceEvent in the middle of the current event. Create travel events to
        move from the current location to the new location and then back to the current location.
        The assumption is that self.STime.STime < place.STime.STime and
        place.ETime.ETime < self.ETime.ETime

        Args:
            place -- an initialized PlaceEvent
        """

        clone = self.Copy(GenName('PLACE'))

        place.Departure = TravelEvent(place, clone)
        if self.Departure :
            clone.Departure = TravelEvent(clone, self.Departure.DstPlace)
        clone.STime = MinimumTimeVariable(place.ETime.STime, self.ETime.ETime)

        self.Departure = TravelEvent(self, place)
        self.ETime = MaximumTimeVariable(self.STime.STime, place.STime.ETime)

    # -----------------------------------------------------------------
    def AddConstraints(self, cstore) :
        constraint = OrderConstraint(self.STime.ID, self.ETime.ID, self.Duration)
        cstore.AddConstraint(constraint)

        if self.Departure :
            self.Departure.AddConstraints(cstore)

    # -----------------------------------------------------------------
    def Dump(self) :
        print ">>> [{0}]: {1}, {2}, {3}, {4}".format(self.EventID, self.Details, str(self.STime), str(self.ETime), self.Duration)
        if self.Departure :
            self.Departure.Dump()


# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class TravelEvent :
    # -----------------------------------------------------------------
    def __init__(self, srcplace, dstplace, id = None) :
        self.SrcPlace = srcplace
        self.DstPlace = dstplace
        self.EventID = id or GenName('TRAVEL')

    # -----------------------------------------------------------------
    @property
    def Duration(self) :
        return 0.5

    # -----------------------------------------------------------------
    def AddConstraints(self, cstore) :
        if self.DstPlace :
            self.DstPlace.AddConstraints(cstore)

            constraint = OrderConstraint(self.SrcPlace.ETime.ID, self.DstPlace.STime.ID, self.Duration)
            cstore.AddConstraint(constraint)

    # -----------------------------------------------------------------
    def Dump(self) :
        print "=== [{0}]: {1}".format(self.EventID, self.Duration)
        if self.DstPlace :
            self.DstPlace.Dump()

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class TimeVariableStore(dict) :
    
    # -----------------------------------------------------------------
    def __init__(self, *args, **kwargs) :
        dict.__init__(self, *args, **kwargs)

    # -----------------------------------------------------------------
    def Copy(self) :
        newlist = TimeVariableStore()
        for tvar in self.itervalues() :
            newlist[tvar.ID] = tvar.Copy()

        return newlist

    # -----------------------------------------------------------------
    def StoreIsValid(self) :
        """ Determine if the store is in a consistent state
        
        Returns:
            True if all variables are still valid
        """
        for var in self.itervalues() :
            if not var.IsValid() : return False

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
        
    

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class ConstraintStore :

    # -----------------------------------------------------------------
    def __init__(self) :
        self.ConstraintList = {}

    # -----------------------------------------------------------------
    def AddConstraint(self, constraint) :
        """ Add a constraint to the list of those to apply to the time intervals

        Args:
            constraint -- a Constraint object
        """
        self.ConstraintList[constraint.ConstraintID] = constraint

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
            changed = False
            for constraint in self.ConstraintList.itervalues() :
                changed = constraint.Apply(varstore) or changed

        return varstore.StoreIsValid()

    # -----------------------------------------------------------------
    def SolveConstraints(self, varstore) :
        """ Apply constraints repeatedly until all variables have been given a value

        Args:
            varstore -- store of TimeVariables over which constraints will be applied

        Returns:
            True if the variable store is valid after all variables have been given a value
        """
        if not self.ApplyConstraints(varstore) : return False

        variables = varstore.FindFreeVariables()
        for var in variables :
            var.PickValue()
            if not self.ApplyConstraints(varstore) : return False

        return True
        

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class xxTimedEventList :
    # -----------------------------------------------------------------
    def __init__(self, baseevent) :
        self.BaseEvent = baseevent
        self.TimeVariableStore = TimeVariableStore()

    # -----------------------------------------------------------------
    def Dump(self) :
        for tvar in sorted(self.TimeVariableStore.values(), key= lambda tvar : tvar.STime) :
            print str(tvar)

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class TimedEventList :
    # -----------------------------------------------------------------
    def __init__(self, details, lifespan) :
        self.Events = {}
        self.TimeVariableStore = TimeVariableStore()

        baseid = self.AddPlaceEvent(details, TimeVariable(0.0), TimeVariable(lifespan))
        self.BaseEvent = self.Events[baseid]

    # -----------------------------------------------------------------
    def AddPlaceEvent(self, details, svar, evar, duration = 0.01, id = None) :
        self.TimeVariableStore[svar.ID] = svar
        self.TimeVariableStore[evar.ID] = evar

        event = PlaceEvent(details, svar, evar, duration, id)
        self.Events[event.EventID] = event

        return event.EventID

    # -----------------------------------------------------------------
    def InsertAfterPlaceEvent(self, id1, id2) :
        ev1 = self.Events[id1]
        ev2 = self.Events[id2]

        if ev1.Departure :
            ev2.Departure = TravelEvent(ev2, ev1.Departure.DstPlace)

        ev1.Departure = TravelEvent(ev1, ev2)
        ev1.ETime = MaximumTimeVariable(ev2.STime.STime, ev2.STime.ETime)
        self.TimeVariableStore[ev1.ETime.ID] = ev1.ETime

    # -----------------------------------------------------------------
    def InsertWithinPlaceEvent(self, id1, id2) :
        ev1 = self.Events[id1]
        ev2 = self.Events[id2]

        idc = self.AddPlaceEvent(ev1.Details, ev1.STime.Copy(GenName('TV')), ev1.ETime.Copy(GenName('TV')), ev1.Duration)
        clone = self.Events[idc]

        ev2.Departure = TravelEvent(ev2, clone)
        if ev1.Departure :
            clone.Departure = TravelEvent(clone, ev1.Departure.DstPlace)
        clone.STime = MinimumTimeVariable(ev2.ETime.STime, ev1.ETime.ETime)
        self.TimeVariableStore[clone.STime.ID] = clone.STime

        ev1.Departure = TravelEvent(ev1, ev2)
        ev1.ETime = MaximumTimeVariable(ev1.STime.STime, ev2.STime.ETime)
        self.TimeVariableStore[ev1.ETime.ID] = ev1.ETime

    # -----------------------------------------------------------------
    def SolveConstraints(self) :
        cstore = ConstraintStore()
        self.BaseEvent.AddConstraints(cstore)
        cstore.SolveConstraints(self.TimeVariableStore)

    # -----------------------------------------------------------------
    def Dump(self) :
        for tvar in sorted(self.TimeVariableStore.values(), key= lambda tvar : tvar.STime) :
            print str(tvar)


## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
if __name__ == '__main__' :
    evlist = TimedEventList('home', 7*24.0)

    idw = evlist.AddPlaceEvent('work', GaussianTimeVariable(7.0, 9.0), GaussianTimeVariable(16.0, 18.0), 9.0)
    idc = evlist.AddPlaceEvent('coffee', MaximumTimeVariable(0.0, 24.0), MinimumTimeVariable(0.0, 24.0), 0.2)

    evlist.InsertWithinPlaceEvent(evlist.BaseEvent.EventID, idw)
    evlist.InsertAfterPlaceEvent(evlist.BaseEvent.EventID, idc)

    evlist.SolveConstraints()
    evlist.Dump()

    # h1 = PlaceEvent('home', TimeVariable(0.0, 0.0), TimeVariable(7*24.0, 7*24.0))
    # h1.InsertWithinEvent(PlaceEvent('work', GaussianTimeVariable(7.0, 9.0), GaussianTimeVariable(16.0, 18.0), 9.0))
    # h1.InsertAfterEvent(PlaceEvent('coffee', MaximumTimeVariable(0.0, 24.0), MinimumTimeVariable(0.0, 24.0), 0.2))

    # evlist = TimedEventList()
    # h1.AddToTimedEventList(evlist)

    # evlist.SolveConstraints()
    # h1.Dump()

