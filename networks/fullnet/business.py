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

@file    fullnet/social.py
@author  Mic Bowman
@date    2014-02-04

This file contains the programmatic specification of the fullnet 
social framework including people and businesses.

"""

import os, sys

from mobdat.common.Schedule import WeeklySchedule
from mobdat.common.Utilities import GenName
from mobdat.common.Decoration import *

import random

# -----------------------------------------------------------------
# -----------------------------------------------------------------
socinfo.AddJobDescription('shift1',    30000,  False, WeeklySchedule.WorkWeekSchedule(4.0, 12.0))
socinfo.AddJobDescription('shift2',    30000,  False, WeeklySchedule.WorkWeekSchedule(12.0, 20.00))
socinfo.AddJobDescription('shift3',    30000,  False, WeeklySchedule.WorkWeekSchedule(20.0, 4.0))

socinfo.AddJobDescription('parttime1', 15000,  False, WeeklySchedule.WorkWeekSchedule(8.0, 12.0))
socinfo.AddJobDescription('parttime2', 15000,  False, WeeklySchedule.WorkWeekSchedule(12.0, 16.0))
socinfo.AddJobDescription('parttime3', 15000,  False, WeeklySchedule.WorkWeekSchedule(16.0, 20.0))
socinfo.AddJobDescription('parttime4', 15000,  False, WeeklySchedule.WorkWeekSchedule(20.0, 24.0))

socinfo.AddJobDescription('worker',    30000,  True,  WeeklySchedule.WorkWeekSchedule(8.0, 17.0))
socinfo.AddJobDescription('seniorwrk', 60000,  True,  WeeklySchedule.WorkWeekSchedule(8.0, 17.0))
socinfo.AddJobDescription('manager',   60000,  True,  WeeklySchedule.WorkWeekSchedule(8.0, 17.0))
socinfo.AddJobDescription('seniormgr', 90000,  True,  WeeklySchedule.WorkWeekSchedule(7.0, 18.0))
socinfo.AddJobDescription('exec',      120000, True,  WeeklySchedule.WorkWeekSchedule(6.0, 18.0))

socinfo.AddJobDescription('student',       0,  False, WeeklySchedule.WorkWeekSchedule(8.0, 15.0))
socinfo.AddJobDescription('teacher',   40000,  False, WeeklySchedule.WorkWeekSchedule(7.5, 15.5))
socinfo.AddJobDescription('admin',     30000,  False, WeeklySchedule.WorkWeekSchedule(7.5, 15.5))
socinfo.AddJobDescription('principal', 80000,  True,  WeeklySchedule.WorkWeekSchedule(7.0, 16.5))
 
socinfo.AddJobDescription('barrista1', 20000,  False, WeeklySchedule.WorkWeekSchedule(6.0, 10.0))
socinfo.AddJobDescription('barrista2', 20000,  False, WeeklySchedule.WorkWeekSchedule(10.0, 14.0))
socinfo.AddJobDescription('barrista3', 20000,  False, WeeklySchedule.WorkWeekSchedule(14.0, 18.0))
socinfo.AddJobDescription('barrista4', 20000,  False, WeeklySchedule.WorkWeekSchedule(18.0, 22.0))
socinfo.AddJobDescription('barrista4', 20000,  False, WeeklySchedule.WorkWeekSchedule(18.0, 22.0))
socinfo.AddJobDescription('storemgr1', 50000,  False, WeeklySchedule.WorkWeekSchedule(6.0, 14.0))
socinfo.AddJobDescription('storemgr2', 50000,  False, WeeklySchedule.WorkWeekSchedule(14.0, 22.0))

# -----------------------------------------------------------------
# -----------------------------------------------------------------
socinfo.AddFactoryProfile("small-factory", {'worker' : 20, 'manager' : 2, 'seniormgr' : 1})
socinfo.AddFactoryProfile("large-factory", {'shift1' : 30, 'shift2' : 30, 'shift3' : 30, 'worker' : 20, 'manager' : 20, 'seniormgr' : 5, 'exec' : 2})

socinfo.AddRetailProfile("bank-branch", {'worker' : 8, 'seniorwrk' : 5, 'seniormgr' : 3, 'exec' : 1}, (9.0, 16.0), 20, 0.25)
socinfo.AddRetailProfile("bank-central", {'worker' : 20, 'seniorwrk' : 20, 'seniormgr' : 5, 'exec' : 1}, (9.0, 16.0), 20, 0.50)
socinfo.AddRetailProfile("small-service", {'parttime1' : 5, 'parttime2' : 5, 'parttime3' : 5, 'manager' : 3, 'exec' : 1}, (9.0, 21.00), 20, 0.5)
socinfo.AddRetailProfile("large-service", {'parttime1' : 15, 'parttime2' : 15, 'parttime3' : 15, 'manager' : 10, 'seniormgr' : 4, 'exec' : 1}, (9.0, 21.00), 60, 1.0)

socinfo.AddRestaurantProfile("coffee", { 'barrista1' : 3, 'barrista2' : 3, 'barrista3' : 2, 'barrista4' : 2, 'storemgr1' : 1, 'storemgr2' : 1}, (6.0, 22.0), 10, 0.25)
socinfo.AddRestaurantProfile("fastfood", {'parttime1' : 5, 'parttime2' : 8, 'parttime3' : 8, 'parttime4' : 5, 'manager' : 2}, (8.0, 24.0), 30, 0.5)
socinfo.AddRestaurantProfile("small-restaurant", {'parttime2' : 4, 'parttime3' : 6, 'parttime4' : 4, 'manager' : 2}, (12.0, 24.0), 20, 1.5)
socinfo.AddRestaurantProfile("large-restaurant", {'parttime2' : 8, 'parttime3' : 12, 'parttime4' : 12, 'manager' : 3}, (12.0, 24.0), 40, 1.5)

# students as customers or students as employees... who knows
#socinfo.AddSchool("elem-school", { 'student' : 200, 'teacher' : 10, 'admin' : 2, 'principal' : 1})
#socinfo.AddSchool("middle-school", { 'student' : 300, 'teacher' : 20, 'admin' : 4, 'principal' : 2})
#socinfo.AddSchool("high-school", { 'student' : 400, 'teacher' : 30, 'admin' : 8, 'principal' : 4})

socinfo.AddSchoolProfile("elem-school", { 'teacher' : 10, 'admin' : 2, 'principal' : 1}, 200)
socinfo.AddSchoolProfile("middle-school", { 'teacher' : 20, 'admin' : 4, 'principal' : 2}, 300)
socinfo.AddSchoolProfile("high-school", { 'teacher' : 30, 'admin' : 8, 'principal' : 4}, 400)

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
def PlaceBusinesses() :
    global layinfo, socinfo

    profiles = {}
    for profname, profile in socinfo.Collections.iteritems() :
        if profile.NodeType.Name == 'BusinessProfile' :
            print profname
            profiles[profname] = profile

    while len(profiles) > 0 :
        # this is a uniform distribution of businesses from the options
        pname = random.choice(profiles.keys())
        profile = profiles[pname]

        name = GenName(pname)
        business = socinfo.AddBusiness(name, profile)

        location = socinfo.PlaceBusiness(business, locinfo)

        # if we could not place the business, then all locations
        # have fitness of 0... so don't try again
        if not location :
            del profiles[pname]

PlaceBusinesses()

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
def CountJobs() :
    global socinfo
    JobCount = {}

    for biz in socinfo.BusinessList.itervalues() :
        bprof = biz.Profile
        for job in bprof.JobList :
            if job.ProfileName not in JobCount :
                JobCount[job.ProfileName] = 0
            JobCount[job.ProfileName] += job.Demand

    people = 0
    names = sorted(JobCount.keys())
    for name in names :
        count = JobCount[name]
        print "{:10} {:5}".format(name, count)
        people += count

    print "Total Jobs: " + str(people)

CountJobs()

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
print "Loaded fullnet business builder extension file"
