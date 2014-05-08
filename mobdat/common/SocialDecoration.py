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

@file    SocialDecoration.py
@author  Mic Bowman
@date    2013-12-03

This file defines routines used to build features of a mobdat traffic
network such as building a grid of roads. 

"""

import os, sys

# we need to import python modules from the $SUMO_HOME/tools directory
sys.path.append(os.path.join(os.environ.get("OPENSIM","/share/opensim"),"lib","python"))
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "lib")))

from mobdat.common.Business import Business, BusinessProfile, JobProfile
from mobdat.common.Person import Person, PersonProfile
from mobdat.common.Decoration import Decoration

from mobdat.common.ValueTypes import MakeEnum, DaysOfTheWeek
from mobdat.common.Schedule import WeeklySchedule
from mobdat.common.Decoration import Decoration

## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
BusinessType = MakeEnum('Unknown', 'Factory', 'Service', 'Civic', 'Entertainment', 'School', 'Retail', 'Food')

## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class JobDescription :

    # -------------------------------------------------------
    @staticmethod
    def Load(pinfo) :
        profilename = pinfo['Name']
        salary = pinfo['Salary']
        flexible = pinfo['FlexibleHours']
        schedule = WeeklySchedule(pinfo['Schedule'])

        return JobProfile(profilename, salary, flexible, schedule)

    # -------------------------------------------------------
    def __init__(self, name, salary, flexible, schedule) :
        self.Name = name
        self.Salary = salary
        self.FlexibleHours = flexible
        self.Schedule = schedule

    # -------------------------------------------------------
    def Copy(self) :
        return JobProfile(self.Name, self.Salary, self.FlexibleHours, self.Schedule)

    # -------------------------------------------------------
    def Dump(self) :
        result = dict()
        result['Name'] = self.Name
        result['Salary'] = self.Salary
        result['FlexibleHours'] = self.FlexibleHours
        result['Schedule'] = self.Schedule.Dump()

        return result


## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class EmploymentProfileDecoration(Decoration) :
    DecorationName = 'EmploymentProfile' 

    # -------------------------------------------------------
    @staticmethod
    def Load(pinfo) :
        joblist = dict()
        for jobinfo in pinfo['JobList'] :
            joblist[JobDescription.Load(jobinfo['Job'])] = jobinfo['Demand']

        return EmploymentProfileDecoration(joblist)

    # -------------------------------------------------------
    def __init__(self, joblist) :
        """
        Args:
            joblist -- dictionary mapping JobDescription --> Demand
        """

        Decoration.__init__(self)

        self.JobList = dict()
        for job, demand in joblist.iteritems() :
            self.JobList[job.Copy()] = demand

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
            for job, demand in self.JobList.iteritems() :
                count += demand if job.Schedule.ScheduledAtTime(day, hour) else 0

            peak = count if peak < count else peak

        return peak

    # -------------------------------------------------------
    def Dump(self) :
        result = Decoration.Dump(self)

        result['JobList'] = []
        for job, demand in self.JobList.iteritems() :
            result['JobList'].append({ 'Job' : job.Dump(), 'Demand' : demand})

        return result

## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class ServiceProfileDecoration(Decoration) :
    DecorationName = 'ServiceProfile'

    # -------------------------------------------------------
    @staticmethod
    def Load(pinfo) :
        bizhours = WeeklySchedule(pinfo['Schedule'])
        capacity = pinfo['CustomerCapacity']
        servicetime = pinfo['ServiceTime']

        return ServiceProfile(bizhours, capacity, servicetime)

    # -------------------------------------------------------
    def __init__(self, bizhours, capacity, servicetime) :
        """
        Args:
            bizhours -- object of type WeeklySchedule
            capacity -- integer maximum customer capacity
            servicetime -- float mean time to service a customer
        """
        Decoration.__init__(self)

        self.Schedule = bizhours
        self.CustomerCapacity = capacity
        self.ServiceTime = servicetime

    # -------------------------------------------------------
    def PeakServiceCount(self, days = None) :
        """
        Compute the peak number of customers expected during the
        day. Given that the duration of visits impacts this, the
        number is really a conservative guess.

        days -- list of DaysOfTheWeek 
        """
        
        if not days :
            days = range(DaysOfTheWeek.Mon, DaysOfTheWeek.Sun + 1)

        # this is the *ugliest* worst performing version of this computation
        # i can imagine. just dont feel the need to do anything more clever
        # right now, note that since capacity is a constant its even dumber
        # since we know it will either be capacity or 0
        peak = 0
        for day in days :
            for hour in range(0, 24) :
                if self.Schedule.ScheduledAtTime(day, hour) :
                    count = self.CustomerCapacity
                    peak = count if peak < count else peak

        return peak

    # -------------------------------------------------------
    def Dump(self) :
        result = Decoration.Dump(self)
        result['CustomerCapacity'] = self.CustomerCapacity
        result['ServiceTime'] = self.ServiceTime
        result['Schedule'] = self.Schedule.Dump()

        return result

## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class BusinessProfileDecoration(Decoration) :
    DecorationName = 'BusinessProfile'
    
    # -------------------------------------------------------
    @staticmethod
    def Load(pinfo) :
        return BusinessProfileDecration(pinfo['BusinessType'])

    # -------------------------------------------------------
    def __init__(self, biztype) :
        """
        The business profile class captures the structure of a 
        generic business pattern. The profile can be used to
        create specific businesses that match the pattern.
        
        biztype -- BusinessType enum
        """

        self.BusinessType = biztype

    # -------------------------------------------------------
    def Dump(self) :
        result = Decoration.Dump(self)
        result['BusinessType'] = self.BusinessType

        return result

## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class PersonProfileDecoration(Decoration) :
    DecorationName = 'PersonProfile'
    
    # -----------------------------------------------------------------
    @staticmethod
    def Load(graph, info) :
        profile = PersonProfile.Load(info['PersonProfile'])
        return PersonProfileDecoration(profile)

    # -----------------------------------------------------------------
    def __init__(self, profile) :
        """
        Args:
            profile -- an object of type Person.PersonProfile
        """
        Decoration.__init__(self)
        self.PersonProfile = profile

    # -----------------------------------------------------------------
    def __getattr__(self, name) :
        return getattr(self.PersonProfile, name)

    # -----------------------------------------------------------------
    def Dump(self) :
        result = Decoration.Dump(self)
        result['PersonProfile'] = self.PersonProfile.Dump()
        
        return result
    
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class PersonDecoration(Decoration) :
    DecorationName = 'Person'
    
    # -----------------------------------------------------------------
    @staticmethod
    def Load(graph, info) :
        employer = Person.Load(info['Person'])
        return PersonDecoration(employer)

    # -----------------------------------------------------------------
    def __init__(self, person) :
        """
        Args:
            person -- an object of type Person.Person
        """
        Decoration.__init__(self)
        self.Person = person

    # -----------------------------------------------------------------
    def __getattr__(self, name) :
        return getattr(self.Person, name)

    # -----------------------------------------------------------------
    def Dump(self) :
        result = Decoration.Dump(self)
        result['Person'] = self.Person.Dump()
        
        return result
    
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class ResidenceDecoration(Decoration) :
    DecorationName = 'Residence'
    
    # -----------------------------------------------------------------
    @staticmethod
    def Load(graph, info) :
        return ResidenceDecoration(info['LocationName'], info['EndPointName'])

    # -----------------------------------------------------------------
    def __init__(self, location, endpoint) :
        """
        Args:
            location -- LayoutInfo.ResidentialLocation
            endpoint -- LayoutInfo.EndPoint
        """
        Decoration.__init__(self)
        self.LocationName = location.Name
        self.EndPointName = endpoint.Name

    # -----------------------------------------------------------------
    def __getattr__(self, name) :
            return self.Residence.__dict__[name]

    # -----------------------------------------------------------------
    def Dump(self) :
        result = Decoration.Dump(self)
        result['LocationName'] = self.LocationName
        result['EndPointName'] = self.EndPointName
        
        return result
    
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
CommonDecorations = [ EmploymentProfileDecoration, ServiceProfileDecoration, BusinessProfileDecoration,
                      PersonProfileDecoration, PersonDecoration, ResidenceDecoration ]

