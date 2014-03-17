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

from mobdat.common.BusinessInfo import WeeklySchedule
from mobdat.common.Business import BusinessType, Business
from mobdat.common.Location import BusinessLocation, BusinessLocationProfile
from mobdat.common.Person import Person
from mobdat.common.Decoration import *

import random

# -----------------------------------------------------------------
# -----------------------------------------------------------------
CapsuleTypeMap = {}
for collection in netinfo.Collections.itervalues() :
    if CapsuleTypeDecoration.DecorationName not in collection.Decorations :
        continue

    typename = collection.CapsuleType.Name
    if typename not in CapsuleTypeMap :
        CapsuleTypeMap[typename] = []

    CapsuleTypeMap[typename].append(collection)

# -----------------------------------------------------------------
# -----------------------------------------------------------------
bizinfo.AddJobProfile('shift1',    30000,  False, WeeklySchedule.WorkWeekSchedule(4.0, 12.0))
bizinfo.AddJobProfile('shift2',    30000,  False, WeeklySchedule.WorkWeekSchedule(12.0, 20.00))
bizinfo.AddJobProfile('shift3',    30000,  False, WeeklySchedule.WorkWeekSchedule(20.0, 4.0))

bizinfo.AddJobProfile('parttime1', 15000,  False, WeeklySchedule.WorkWeekSchedule(8.0, 12.0))
bizinfo.AddJobProfile('parttime2', 15000,  False, WeeklySchedule.WorkWeekSchedule(12.0, 16.0))
bizinfo.AddJobProfile('parttime3', 15000,  False, WeeklySchedule.WorkWeekSchedule(16.0, 20.0))
bizinfo.AddJobProfile('parttime4', 15000,  False, WeeklySchedule.WorkWeekSchedule(20.0, 24.0))

bizinfo.AddJobProfile('worker',    30000,  True,  WeeklySchedule.WorkWeekSchedule(8.0, 17.0))
bizinfo.AddJobProfile('seniorwrk', 60000,  True,  WeeklySchedule.WorkWeekSchedule(8.0, 17.0))
bizinfo.AddJobProfile('manager',   60000,  True,  WeeklySchedule.WorkWeekSchedule(8.0, 17.0))
bizinfo.AddJobProfile('seniormgr', 90000,  True,  WeeklySchedule.WorkWeekSchedule(7.0, 18.0))
bizinfo.AddJobProfile('exec',      120000, True,  WeeklySchedule.WorkWeekSchedule(6.0, 18.0))

bizinfo.AddJobProfile('student',       0,  False, WeeklySchedule.WorkWeekSchedule(8.0, 15.0))
bizinfo.AddJobProfile('teacher',   40000,  False, WeeklySchedule.WorkWeekSchedule(7.5, 15.5))
bizinfo.AddJobProfile('admin',     30000,  False, WeeklySchedule.WorkWeekSchedule(7.5, 15.5))
bizinfo.AddJobProfile('principal', 80000,  True,  WeeklySchedule.WorkWeekSchedule(7.0, 16.5))
 
bizinfo.AddJobProfile('barrista1', 20000,  False, WeeklySchedule.WorkWeekSchedule(6.0, 10.0))
bizinfo.AddJobProfile('barrista2', 20000,  False, WeeklySchedule.WorkWeekSchedule(10.0, 14.0))
bizinfo.AddJobProfile('barrista3', 20000,  False, WeeklySchedule.WorkWeekSchedule(14.0, 18.0))
bizinfo.AddJobProfile('barrista4', 20000,  False, WeeklySchedule.WorkWeekSchedule(18.0, 22.0))
bizinfo.AddJobProfile('barrista4', 20000,  False, WeeklySchedule.WorkWeekSchedule(18.0, 22.0))
bizinfo.AddJobProfile('storemgr1', 50000,  False, WeeklySchedule.WorkWeekSchedule(6.0, 14.0))
bizinfo.AddJobProfile('storemgr2', 50000,  False, WeeklySchedule.WorkWeekSchedule(14.0, 22.0))

# -----------------------------------------------------------------
# -----------------------------------------------------------------
bizinfo.AddFactory("small-factory", {'worker' : 20, 'manager' : 2, 'seniormgr' : 1})
bizinfo.AddFactory("large-factory", {'shift1' : 30, 'shift2' : 30, 'shift3' : 30, 'worker' : 20, 'manager' : 20, 'seniormgr' : 5, 'exec' : 2})

bizinfo.AddRetail("bank-branch", {'worker' : 8, 'seniorwrk' : 5, 'seniormgr' : 3, 'exec' : 1}, (9.0, 16.0), 20, 0.25)
bizinfo.AddRetail("bank-central", {'worker' : 20, 'seniorwrk' : 20, 'seniormgr' : 5, 'exec' : 1}, (9.0, 16.0), 20, 0.50)
bizinfo.AddRetail("small-service", {'parttime1' : 5, 'parttime2' : 5, 'parttime3' : 5, 'manager' : 3, 'exec' : 1}, (9.0, 21.00), 20, 0.5)
bizinfo.AddRetail("large-service", {'parttime1' : 15, 'parttime2' : 15, 'parttime3' : 15, 'manager' : 10, 'seniormgr' : 4, 'exec' : 1}, (9.0, 21.00), 60, 1.0)

bizinfo.AddRestaurant("coffee", { 'barrista1' : 3, 'barrista2' : 3, 'barrista3' : 2, 'barrista4' : 2, 'storemgr1' : 1, 'storemgr2' : 1}, (6.0, 22.0), 10, 0.25)
bizinfo.AddRestaurant("fastfood", {'parttime1' : 5, 'parttime2' : 8, 'parttime3' : 8, 'parttime4' : 5, 'manager' : 2}, (8.0, 24.0), 30, 0.5)
bizinfo.AddRestaurant("small-restaurant", {'parttime2' : 4, 'parttime3' : 6, 'parttime4' : 4, 'manager' : 2}, (12.0, 24.0), 20, 1.5)
bizinfo.AddRestaurant("large-restaurant", {'parttime2' : 8, 'parttime3' : 12, 'parttime4' : 12, 'manager' : 3}, (12.0, 24.0), 40, 1.5)

# students as customers or students as employees... who knows
#bizinfo.AddSchool("elem-school", { 'student' : 200, 'teacher' : 10, 'admin' : 2, 'principal' : 1})
#bizinfo.AddSchool("middle-school", { 'student' : 300, 'teacher' : 20, 'admin' : 4, 'principal' : 2})
#bizinfo.AddSchool("high-school", { 'student' : 400, 'teacher' : 30, 'admin' : 8, 'principal' : 4})

bizinfo.AddSchool("elem-school", { 'teacher' : 10, 'admin' : 2, 'principal' : 1}, 200)
bizinfo.AddSchool("middle-school", { 'teacher' : 20, 'admin' : 4, 'principal' : 2}, 300)
bizinfo.AddSchool("high-school", { 'teacher' : 30, 'admin' : 8, 'principal' : 4}, 400)

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
bizinfo.AddBusinessLocationProfile('plaza', 75, 25,  { BusinessType.Factory : 1.0, BusinessType.Service : 0.5, BusinessType.Food : 0.25 })
bizinfo.AddBusinessLocationProfile('mall',  20, 75,  { BusinessType.Factory : 0.1, BusinessType.Service : 1.0, BusinessType.Food : 1.0 })
bizinfo.AddBusinessLocationProfile('civic', 20, 150, { BusinessType.School : 1.0, BusinessType.Civic : 1.0 })

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
for capsuletype in ['plaza', 'mall', 'civic'] :
    for bcapsule in CapsuleTypeMap.get(capsuletype, []) :
        bizinfo.AddBusinessLocation(bcapsule, bizinfo.BusinessLocationProfiles[capsuletype])

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
NameCounts = {}
def GenName(prefix) :
    if prefix not in NameCounts :
        NameCounts[prefix] = 0
    NameCounts[prefix] += 1
    return prefix + str(NameCounts[prefix])

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
def PlaceBusinesses() :
    global bizinfo

    profiles = {}
    for profname, profile in bizinfo.BusinessProfiles.iteritems() :
        profiles[profname] = profile

    while len(profiles) > 0 :
        # this is a uniform distribution of businesses from the options
        pname = random.choice(profiles.keys())
        profile = profiles[pname]

        name = GenName(profile.ProfileName)
        business = Business(name, profile)

        location = bizinfo.PlaceBusiness(business)

        # if we could not place the business, then all locations
        # have fitness of 0... so don't try again
        if not location :
            del profiles[pname]

PlaceBusinesses()


# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
perinfo.AddResidentialLocationProfile('worker', 25)

for rcapsule in CapsuleTypeMap['residence'] :
    perinfo.AddResidentialLocation(rcapsule, perinfo.ResidentialLocationProfiles['worker'])

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

perinfo.AddPersonProfile('worker')
perinfo.AddPersonProfile('student')
perinfo.AddPersonProfile('homemaker')

def PlacePeople() :
    global bizinfo, perinfo

    profile = perinfo.PersonProfiles['worker']

    for biz in bizinfo.BusinessList.itervalues() :
        bprof = biz.Profile
        for job in bprof.JobList :
            for p in range(0, job.Demand) :
                name = GenName(profile.ProfileName)
                person = Person(name, profile, biz, job)
                location = perinfo.PlacePerson(person)
                if not location :
                    print 'ran out of residences after worker %s' % name
                    return

PlacePeople()

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
def CountJobs() :
    global bizinfo
    JobCount = {}

    for biz in bizinfo.BusinessList.itervalues() :
        bprof = biz.Profile
        for job in bprof.JobList :
            if job.ProfileName not in JobCount :
                JobCount[job.ProfileName] = 0
            JobCount[job.ProfileName] += job.Demand

    people = 0
    names = sorted(JobCount.keys())
    for name in names :
        count = JobCount[name]
        print "%s \t %s" % (name, count)
        people += count

    print "Total Jobs: " + str(people)

CountJobs()

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
print "Loaded fullnet social extension file"
