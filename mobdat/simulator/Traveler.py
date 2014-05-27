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

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class Traveler :

    # -----------------------------------------------------------------
    def __init__(self, person, connector) :
        self.Person = person
        self.Residence = self.Person.ResidesAt
        self.Employer = self.Person.EmployedBy
        self.EmployerLocation = self.Employer.ResidesAt
        self.Job = self.Person.JobDescription

        self.EstimatedTimeToWork = random.uniform(0.25, 0.75)
        self.CurrentLocation = self.Residence
        self.CurrentEvent = None

        nexttrip = self.NextTrip(connector.WorldTime)
        connector.AddTripToEventQueue(nexttrip)

    # -----------------------------------------------------------------
    def NextTrip(self, worldtime) :
        if self.CurrentLocation == self.Residence :
            self.CurrentEvent = self.Job.Schedule.NextScheduledEvent(worldtime + self.EstimatedTimeToWork)
            stime = self.CurrentEvent.WorldStartTime - self.EstimatedTimeToWork
            if self.Job.FlexibleHours :
                stime = random.gauss(stime, 0.5)
            stime = max(worldtime, stime)

            return Trip.Trip(self, stime, self.Residence.ResidentialLocation, self.EmployerLocation.BusinessLocation)
        else:
            etime = self.CurrentEvent.WorldEndTime
            if self.Job.FlexibleHours :
                etime = random.gauss(etime, 0.5)
            etime = max(worldtime, etime)

            return Trip.Trip(self, etime, self.EmployerLocation.BusinessLocation, self.Residence.ResidentialLocation)

    # -----------------------------------------------------------------
    def TripCompleted(self, trip, connector) :
        # if this is a trip to work, update the estimated start time, dont want to be late to work
        if trip.Destination == self.EmployerLocation :
            offset = connector.WorldTime - self.CurrentEvent.WorldStartTime # positive means traveler is late for work
            self.EstimatedTimeToWork = (4.0 * self.EstimatedTimeToWork - offset) / 5.0

        self.CurrentLocation = trip.Destination

        nexttrip = self.NextTrip(connector.WorldTime)
        connector.AddTripToEventQueue(nexttrip)

    # -----------------------------------------------------------------
    def TripStarted(self, trip, connector) :
        pass

