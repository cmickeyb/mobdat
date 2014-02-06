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

@file    SocBuilder.py
@author  Mic Bowman
@date    2014-02-04

This file defines routines used to build profiles for people and places.

"""

import os, sys
import logging

# we need to import python modules from the $SUMO_HOME/tools directory
sys.path.append(os.path.join(os.environ.get("OPENSIM","/share/opensim"),"lib","python"))
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "lib")))

from mobdat.ValueTypes import MakeEnum, DaysOfTheWeek

## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
BusinessType = MakeEnum('Unknown', 'Factory', 'Service', 'Civic', 'Entertainment', 'School', 'Retail', 'Food')

## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class JobProfile :

    # -------------------------------------------------------
    def __init__(self, name, salary, flexible, schedule, demand = 0) :
        self.ProfileName = name
        self.Salary = salary
        self.FlexibleHours = flexible
        self.Schedule = schedule
        self.Demand = demand

    # -------------------------------------------------------
    def Copy(self) :
        return JobProfile(self.ProfileName, self.Salary, self.FlexibleHours, self.Schedule, self.Demand)

    # -------------------------------------------------------
    def Dump(self) :
        result = self.__dict__.copy()
        result['Schedule'] = self.Schedule.Dump()
        return result

## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class ServiceProfile :

    # -------------------------------------------------------
    def __init__(self, bizhours, capacity, servicetime) :
        self.Schedule = bizhours
        self.CustomerCapacity = capacity
        self.ServiceTime = servicetime

    # -------------------------------------------------------
    def Dump(self) :
        result = self.__dict__.copy()
        result['Schedule'] = self.Schedule.Dump()
        return result

## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class BusinessProfile :

    # -------------------------------------------------------
    def __init__(self, name, biztype) :
        """
        The business profile class captures the structure of a 
        generic business pattern. The profile can be used to
        create specific businesses that match the pattern.
        
        name -- name of the profile
        biztype -- BusinessType enum
        """

        self.ProfileName = name
        self.BusinessType = biztype

        self.ServiceProfile = None
        self.JobList = []

    # -------------------------------------------------------
    def PeakEmployeeCount(self, day = DaysOfTheWeek.Mon) :
        """
        Compute the peak hourly employee count over the
        course of a day.

        day -- DaysOfTheWeek enum
        """
        
        # this is the *ugliest* worst performing version of this computation
        # i can imagine. just dont feel the need to do anything more clever
        # right now
        peak = 0
        for hour in range(0, 24) :
            count = 0
            for jp in self.JobList :
                count += demand if jp.Schedule.ScheduledAtTime(day, hour) else 0

            peak = count if peak < count else peak

        return peak


    # -------------------------------------------------------
    def PeakServiceCount(self, day = DaysOfTheWeek.Mon) :
        """
        Compute the peak number of customers expected during the
        day. Given that the duration of visits impacts this, the
        number is really a conservative guess.

        day -- DaysOfTheWeek enum
        """
        
        # this is the *ugliest* worst performing version of this computation
        # i can imagine. just dont feel the need to do anything more clever
        # right now
        peak = 0
        for hour in range(0, 24) :
            count = self.ServiceProfile.Schedule.ScheduledAtTime(day, hour)
            peak = count if peak < count else peak

        return peak

    # -------------------------------------------------------
    def Generate(self, name, location) :
        """
        Create a business object from the profile and place it in the
        specified location.
        
        name -- name of the business
        location -- the pod in which the business is located
        """

        return Business(name, self, location)
        
        
    # -------------------------------------------------------
    def Dump(self) :
        result = self.__dict__.copy()

        if self.ServiceProfile :
            result['ServiceProfile'] = self.ServiceProfile.Dump()
            
        result['JobList'] = []
        for j in self.JobList :
            result['JobList'].append(j.Dump())

        return result

## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class Business :

    # -------------------------------------------------------
    def __init__(self, name, profile, location) :
        """
        The Business class captures data about a specific business
        that operates in the simulation.

        name -- name of the business
        profile -- a BusinessProfile
        location -- a Pod
        """

        self.Name = name
        self.Profile = profile
        self.Location = location
        self.PeakEmployeeCount = self.Profile.PeakEmployeeCount()
        self.PeakCustomerCount = self.Profile.PeakCustomerCount()

        self.Location.AddBusiness(self, self.PeakEmployeeCount)

    # -------------------------------------------------------
    def Dump(self) :
        result = dict()
        result["Name"] = self.Name
        result["Profile"] = self.Profile.ProfileName
        result["Location"] = self.Location.LocationName
        return result

## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class BusinessData :
    def __init__(self) :
        self.BusinessProfiles = []
        self.CompanyList = []

    def Dump(self) :
        result = dict()
        result['CompanyList'] = []
        for c in self.CompanyList :
            result['CompanyList'].append(c.Dump())

        result['BusinessProfiles'] = []
        for p in self.BusinessProfiles :
            result['BusinessProfiles'].append(p.Dump())

        return result