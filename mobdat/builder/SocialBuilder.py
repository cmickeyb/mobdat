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

@file    SocialBuilder.py
@author  Mic Bowman
@date    2014-02-04

This file defines routines used to build profiles for people and places.

"""

import os, sys, warnings, copy

# we need to import python modules from the $SUMO_HOME/tools directory
sys.path.append(os.path.join(os.environ.get("OPENSIM","/share/opensim"),"lib","python"))
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "..")))
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "lib")))

from mobdat.common.Location import *
from mobdat.common.Schedule import WeeklySchedule
from mobdat.common import SocialInfo, Decoration, SocialDecoration, Business

## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class SocialBuilder(SocialInfo.SocialInfo) :

    # -----------------------------------------------------------------
    def __init__(self) :
        SocialInfo.SocialInfo.__init__(self)

        self.JobProfiles = {}
        self.BusinessProfile = {}

    # -----------------------------------------------------------------
    def AddResidence(self, residence) :
        """
        Args:
            residence -- object of type Business.BusinessProfile
        """
        res = SocialInfo.Collection(name = name)
        res.AddDecoration(Decoration.NodeTypeDecoration('residence'))

        self.AddCollection(res)
        return res

    # -----------------------------------------------------------------
    def AddPerson(self, name, employer, profile, jobprofile, residence) :
        person = SocialInfo.Node(name)
        person.AddDecoration(Decoration.NodeTypeDecoration('person'))
        person.AddDecoration(SocialDecoration.JobProfileDecoration(jobprofile))
        person.AddDecoration(SocialDecoration.ResidenceDecoration(residence))

        self.AddNode(person)

        employer.AddMember(person)
        return person

    # -----------------------------------------------------------------
    def AddJobProfile(self, name, salary, flexible, hours) :
        """
        AddJobProfile -- add a job profile that 
        Args:
            name -- unique string name for the job
            salary -- number, salary in dollars
            flexible -- boolean, flag to specify that hours are flexible
            hours -- object of type WeeklySchedule
        """
        self.JobProfiles[name] = Business.JobProfile(name, salary, flexible, hours)
        return self.JobProfiles[name]

    # -----------------------------------------------------------------
    def _ExpandJobList(self, joblist) :
        """
        Args:
            joblist -- dictionary that maps job profile names to demand

        Returns: 
            a list of Business.JobProfile objects with demand initialized
        """

        jobs = []
        for jobname, demand in joblist.iteritems() :
            jobs.append(self.JobProfiles[jobname].Copy(demand))

        return jobs

    # -----------------------------------------------------------------
    def AddBusinessProfile(self, profile) :
        """
        Args:
            name -- unique string name for the employer
            profile -- object of type Business.BusinessProfile
        """
        if profile.ProfileName in self.Collections :
            return self.Collections[profile.ProfileName]

        bizprof = SocialInfo.Collection(name = profile.ProfileName)
        bizprof.AddDecoration(Decoration.NodeTypeDecoration('business-profile'))
        bizprof.AddDecoration(SocialDecoration.BusinessProfileDecoration(profile))

        self.AddCollection(bizprof)
        return bizprof

    # -----------------------------------------------------------------
    def AddFactoryProfile(self, name, joblist) :
        jobs = self._ExpandJobList(joblist)

        return self.AddBusinessProfile(Business.BusinessProfile(name, Business.BusinessType.Factory, jobs))

    # -----------------------------------------------------------------
    def AddRetailProfile(self, name, joblist, bizhours, customers, stime = 0.5) :
        jobs = self._ExpandJobList(joblist)
        sprofile = Business.ServiceProfile(WeeklySchedule.WorkWeekSchedule(bizhours[0], bizhours[1]), customers, stime)

        return self.AddBusinessProfile(Business.BusinessProfile(name, Business.BusinessType.Service, jobs, sprofile))

    # -----------------------------------------------------------------
    def AddRestaurantProfile(self, name, joblist, bizhours, customers, stime = 1.5) :
        jobs = self._ExpandJobList(joblist)
        sprofile = Business.ServiceProfile(WeeklySchedule.WorkWeekSchedule(bizhours[0], bizhours[1]), customers, stime)

        return self.AddBusinessProfile(Business.BusinessProfile(name, Business.BusinessType.Food, jobs, sprofile))

    # -----------------------------------------------------------------
    def AddSchoolProfile(self, name, joblist, students) :
        jobs = self._ExpandJobList(joblist)
        sprofile = Business.ServiceProfile(WeeklySchedule.WorkWeekSchedule(8.0, 15.0), students, 7.0)

        return self.AddBusinessProfile(Business.BusinessProfile(name, Business.BusinessType.School, jobs, sprofile))

    # -----------------------------------------------------------------
    def AddBusiness(self, business, profile) :
        """
        Args:
            business -- object of type Business.Business
            profile -- object of type SocialInfo.Collection
        """

        biz = SocialInfo.Collection(name = business.Name)
        biz.AddDecoration(Decoration.NodeTypeDecoration('business'))
        biz.AddDecoration(SocialDecoration.BusinessDecoration(business))

        self.AddCollection(biz)

        profile.AddMember(biz)
        return biz


## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
if __name__ == '__main__' :
    builder = SocialBuilder()

    jp1 = builder.AddJobProfile('shift1',    30000,  False, WeeklySchedule.WorkWeekSchedule(4.0, 12.0))
    jp2 = builder.AddJobProfile('shift2',    30000,  False, WeeklySchedule.WorkWeekSchedule(12.0, 20.00))
    jp3 = builder.AddJobProfile('shift3',    30000,  False, WeeklySchedule.WorkWeekSchedule(20.0, 4.0))

    builder.AddJobProfile('parttime1', 15000,  False, WeeklySchedule.WorkWeekSchedule(8.0, 12.0))
    builder.AddJobProfile('parttime2', 15000,  False, WeeklySchedule.WorkWeekSchedule(12.0, 16.0))
    builder.AddJobProfile('parttime3', 15000,  False, WeeklySchedule.WorkWeekSchedule(16.0, 20.0))
    builder.AddJobProfile('parttime4', 15000,  False, WeeklySchedule.WorkWeekSchedule(20.0, 24.0))

    builder.AddJobProfile('worker',    30000,  True,  WeeklySchedule.WorkWeekSchedule(8.0, 17.0))
    builder.AddJobProfile('seniorwrk', 60000,  True,  WeeklySchedule.WorkWeekSchedule(8.0, 17.0))
    builder.AddJobProfile('manager',   60000,  True,  WeeklySchedule.WorkWeekSchedule(8.0, 17.0))
    builder.AddJobProfile('seniormgr', 90000,  True,  WeeklySchedule.WorkWeekSchedule(7.0, 18.0))
    builder.AddJobProfile('exec',      120000, True,  WeeklySchedule.WorkWeekSchedule(6.0, 18.0))

    builder.AddJobProfile('student',       0,  False, WeeklySchedule.WorkWeekSchedule(8.0, 15.0))
    builder.AddJobProfile('teacher',   40000,  False, WeeklySchedule.WorkWeekSchedule(7.5, 15.5))
    builder.AddJobProfile('admin',     30000,  False, WeeklySchedule.WorkWeekSchedule(7.5, 15.5))
    builder.AddJobProfile('principal', 80000,  True,  WeeklySchedule.WorkWeekSchedule(7.0, 16.5))

    builder.AddJobProfile('barrista1', 20000,  False, WeeklySchedule.WorkWeekSchedule(6.0, 10.0))
    builder.AddJobProfile('barrista2', 20000,  False, WeeklySchedule.WorkWeekSchedule(10.0, 14.0))
    builder.AddJobProfile('barrista3', 20000,  False, WeeklySchedule.WorkWeekSchedule(14.0, 18.0))
    builder.AddJobProfile('barrista4', 20000,  False, WeeklySchedule.WorkWeekSchedule(18.0, 22.0))
    builder.AddJobProfile('barrista4', 20000,  False, WeeklySchedule.WorkWeekSchedule(18.0, 22.0))
    builder.AddJobProfile('storemgr1', 50000,  False, WeeklySchedule.WorkWeekSchedule(6.0, 14.0))
    builder.AddJobProfile('storemgr2', 50000,  False, WeeklySchedule.WorkWeekSchedule(14.0, 22.0))

    # -----------------------------------------------------------------
    # -----------------------------------------------------------------
    bp = builder.AddFactoryProfile("small-factory", {'worker' : 20, 'manager' : 2, 'seniormgr' : 1})
    builder.AddFactoryProfile("large-factory", {'shift1' : 30, 'shift2' : 30, 'worker' : 20, 'manager' : 20, 'seniormgr' : 5, 'exec' : 2})

    builder.AddRetailProfile("bank-branch", {'worker' : 8, 'seniorwrk' : 5, 'seniormgr' : 3, 'exec' : 1}, (9.0, 16.0), 20, 0.25)
    builder.AddRetailProfile("bank-central", {'worker' : 20, 'seniorwrk' : 20, 'seniormgr' : 5, 'exec' : 1}, (9.0, 16.0), 20, 0.50)
    builder.AddRetailProfile("small-service", {'parttime1' : 5, 'parttime2' : 5, 'parttime3' : 5, 'manager' : 3}, (9.0, 21.00), 20, 0.5)
    builder.AddRetailProfile("large-service", {'parttime1' : 15, 'parttime2' : 15, 'manager' : 10}, (9.0, 21.00), 60, 1.0)

    builder.AddRestaurantProfile("coffee", { 'barrista1' : 3, 'barrista2' : 3, 'barrista3' : 2, 'storemgr2' : 1}, (6.0, 22.0), 10, 0.25)
    builder.AddRestaurantProfile("fastfood", {'parttime1' : 5, 'parttime2' : 8, 'parttime3' : 8, 'manager' : 2}, (8.0, 24.0), 30, 0.5)
    builder.AddRestaurantProfile("small-restaurant", {'parttime2' : 4, 'parttime3' : 6, 'parttime4' : 4, 'manager' : 2}, (12.0, 24.0), 20, 1.5)
    builder.AddRestaurantProfile("large-restaurant", {'parttime2' : 8, 'parttime3' : 12, 'parttime4' : 12, 'manager' : 3}, (12.0, 24.0), 40, 1.5)

    builder.AddSchoolProfile("elem-school", { 'teacher' : 10, 'admin' : 2, 'principal' : 1}, 200)
    builder.AddSchoolProfile("middle-school", { 'teacher' : 20, 'admin' : 4, 'principal' : 2}, 300)
    builder.AddSchoolProfile("high-school", { 'teacher' : 30, 'admin' : 8, 'principal' : 4}, 400)

    # -----------------------------------------------------------------
    # -----------------------------------------------------------------
    emp1 = builder.AddBusiness(Business.Business('biz1'), bp)
    per1 = builder.AddPerson('per1', emp1, None, jp1, 'res1')
    per2 = builder.AddPerson('per2', emp1, None, jp2, 'res1')
    per3 = builder.AddPerson('per3', emp1, None, jp1, 'res2')

    print '---------- BEFORE ----------'
    # print emp1.Dump()
    # print emp1.BusinessProfile.Dump()

    print per3.JobProfile.ProfileName
    print per3.Business.Name
    print emp1.BusinessProfile.ProfileName
    print emp1.BusinessProfile.PeakEmployeeCount()

    nbuilder = SocialInfo.SocialInfo()
    nbuilder.Load( builder.Dump())

    print '---------- AFTER ----------'
    emp1a = nbuilder.Collections['biz1']
    per3a = nbuilder.Nodes['per1']

    # print emp1a.Dump()
    # print emp1a.BusinessProfile.Dump()

    print per3a.JobProfile.ProfileName
    print per3a.Business.Name
    print emp1a.BusinessProfile.ProfileName
    print emp1a.BusinessProfile.PeakEmployeeCount()
