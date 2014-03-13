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

import os, sys, warnings, copy

# we need to import python modules from the $SUMO_HOME/tools directory
sys.path.append(os.path.join(os.environ.get("OPENSIM","/share/opensim"),"lib","python"))
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "lib")))

from mobdat.common.BusinessInfo import BusinessInfo, WeeklySchedule
from mobdat.common.Business import *
from mobdat.common.Location import *

## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class BusinessBuilder(BusinessInfo) :

    # -----------------------------------------------------------------
    def __init__(self, netinfo) :
        BusinessInfo.__init__(self, netinfo)

    # -----------------------------------------------------------------
    def AddJobProfile(self, name, salary, flexible, hours) :
        self.JobProfiles[name] = JobProfile(name, salary, flexible, hours)

    # -----------------------------------------------------------------
    def AddBusinessProfile(self, profile, joblist) :        
        # need to make a copy of the joblist so we can customize the
        # demand, that's the unique characteristic
        for jobname, demand in joblist.iteritems() :
            profile.JobList.append(self.JobProfiles[jobname].Copy(demand))

        self.BusinessProfiles[profile.ProfileName] = profile

    # -----------------------------------------------------------------
    def AddFactory(self, name, joblist) :
        bizprofile = BusinessProfile(name, BusinessType.Factory)

        self.AddBusinessProfile(bizprofile, joblist)

    # -----------------------------------------------------------------
    def AddRetail(self, name, joblist, bizhours, customers, stime = 0.5) :
        bizprofile = BusinessProfile(name, BusinessType.Service)
        bizprofile.ServiceProfile = ServiceProfile(WeeklySchedule.WorkWeekSchedule(bizhours[0], bizhours[1]), customers, stime)

        self.AddBusinessProfile(bizprofile, joblist)

    # -----------------------------------------------------------------
    def AddRestaurant(self, name, joblist, bizhours, customers, stime = 1.5) :
        bizprofile = BusinessProfile(name, BusinessType.Food)
        bizprofile.ServiceProfile = ServiceProfile(WeeklySchedule.FullWeekSchedule(bizhours[0], bizhours[1]), customers, stime)

        self.AddBusinessProfile(bizprofile, joblist)

    # -----------------------------------------------------------------
    def AddSchool(self, name, joblist, students) :
        bizprofile = BusinessProfile(name, BusinessType.School)
        bizprofile.ServiceProfile = ServiceProfile(WeeklySchedule.WorkWeekSchedule(8.0, 15.0), students, 7.0)

        self.AddBusinessProfile(bizprofile, joblist)

    # -----------------------------------------------------------------
    def AddBusinessLocationProfile(self, name, employees, customers, types) :
        self.BusinessLocationProfiles[name] = BusinessLocationProfile(name, employees, customers, types)

    # -----------------------------------------------------------------
    def AddBusinessLocation(self, capsule, profile) :
        self.BusinessLocations.append(BusinessLocation(capsule, profile))

    # -----------------------------------------------------------------
    def PlaceBusiness(self, business) :
        bestloc = None
        bestfit = 0
        for location in self.BusinessLocations :
            fitness = location.Fitness(business)
            if fitness > bestfit :
                bestfit = fitness
                bestloc = location

        if bestloc :
            bestloc.AddBusiness(business)
            business.Location = bestloc
            self.BusinessList[business.Name] = business

        return bestloc
