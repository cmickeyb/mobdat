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
from mobdat.socbuilder.Business import BusinessType, BusinessProfile, JobProfile, ServiceProfile
from mobdat.socbuilder.SocBuilder import WeeklySchedule
# -----------------------------------------------------------------
# -----------------------------------------------------------------
JobProfiles = {}
def AddJobProfile(name, salary, flexible, hours) :
    global JobProfiles
    JobProfiles[name] = JobProfile(name, salary, flexible, hours)

AddJobProfile('shift1',    30000,  False, WeeklySchedule.WorkWeekSchedule(4.0, 12.0))
AddJobProfile('shift2',    30000,  False, WeeklySchedule.WorkWeekSchedule(12.0, 20.00))
AddJobProfile('shift3',    30000,  False, WeeklySchedule.WorkWeekSchedule(20.0, 4.0))

AddJobProfile('parttime1', 15000,  False, WeeklySchedule.WorkWeekSchedule(8.0, 12.0))
AddJobProfile('parttime2', 15000,  False, WeeklySchedule.WorkWeekSchedule(12.0, 16.0))
AddJobProfile('parttime3', 15000,  False, WeeklySchedule.WorkWeekSchedule(16.0, 20.0))
AddJobProfile('parttime4', 15000,  False, WeeklySchedule.WorkWeekSchedule(20.0, 24.0))

AddJobProfile('worker',    30000,  True,  WeeklySchedule.WorkWeekSchedule(8.0, 17.0))
AddJobProfile('seniorwrk', 60000,  True,  WeeklySchedule.WorkWeekSchedule(8.0, 17.0))
AddJobProfile('manager',   60000,  True,  WeeklySchedule.WorkWeekSchedule(8.0, 17.0))
AddJobProfile('seniormgr', 90000,  True,  WeeklySchedule.WorkWeekSchedule(7.0, 18.0))
AddJobProfile('exec',      120000, True,  WeeklySchedule.WorkWeekSchedule(6.0, 18.0))

AddJobProfile('student',       0,  False, WeeklySchedule.WorkWeekSchedule(8.0, 15.0))
AddJobProfile('teacher',   40000,  False, WeeklySchedule.WorkWeekSchedule(7.5, 15.5))
AddJobProfile('admin',     30000,  False, WeeklySchedule.WorkWeekSchedule(7.5, 15.5))
AddJobProfile('principal', 80000,  True,  WeeklySchedule.WorkWeekSchedule(7.0, 16.5))
 
AddJobProfile('barrista1', 20000,  False, WeeklySchedule.WorkWeekSchedule(6.0, 10.0))
AddJobProfile('barrista2', 20000,  False, WeeklySchedule.WorkWeekSchedule(10.0, 14.0))
AddJobProfile('barrista3', 20000,  False, WeeklySchedule.WorkWeekSchedule(14.0, 18.0))
AddJobProfile('barrista4', 20000,  False, WeeklySchedule.WorkWeekSchedule(18.0, 22.0))
AddJobProfile('barrista4', 20000,  False, WeeklySchedule.WorkWeekSchedule(18.0, 22.0))
AddJobProfile('storemgr1', 50000,  False, WeeklySchedule.WorkWeekSchedule(6.0, 14.0))
AddJobProfile('storemgr2', 50000,  False, WeeklySchedule.WorkWeekSchedule(14.0, 22.0))

# -----------------------------------------------------------------
# -----------------------------------------------------------------
def AddCompanyProfile(company, joblist) :
    global bizdata, JobProfiles

    for j in joblist :
        jp = JobProfiles[j].Copy()
        jp.Demand = joblist[j]
        company.JobList.append(jp)

    bizdata.BusinessProfiles.append(company)

def AddFactory(name, joblist) :
    company = BusinessProfile(name, BusinessType.Factory)
    AddCompanyProfile(company, joblist)

def AddService(name, joblist, bizhours, customers, stime = 0.5) :
    company = BusinessProfile(name, BusinessType.Service)
    company.ServiceProfile = ServiceProfile(WeeklySchedule.WorkWeekSchedule(bizhours[0], bizhours[1]), customers, stime)
    
    AddCompanyProfile(company, joblist)

def AddFood(name, joblist, bizhours, customers, stime = 1.5) :
    company = BusinessProfile(name, BusinessType.Food)
    company.ServiceProfile = ServiceProfile(WeeklySchedule.FullWeekSchedule(bizhours[0], bizhours[1]), customers, stime)
    
    AddCompanyProfile(company, joblist)

def AddSchool(name, joblist) :
    company = BusinessProfile(name, BusinessType.School)
    AddCompanyProfile(company, joblist)

# -----------------------------------------------------------------
# -----------------------------------------------------------------
AddFactory("small-factory", {'worker' : 20, 'manager' : 2, 'seniormgr' : 1})
AddFactory("large-factory", {'shift1' : 30, 'shift2' : 30, 'shift3' : 30, 'worker' : 20, 'manager' : 20, 'seniormgr' : 5, 'exec' : 2})

AddService("bank-branch", {'worker' : 8, 'seniorwrk' : 5, 'seniormgr' : 3, 'exec' : 1}, (9.0, 16.0), 20, 0.25)
AddService("bank-central", {'worker' : 20, 'seniorwrk' : 20, 'seniormgr' : 5, 'exec' : 1}, (9.0, 16.0), 20, 0.50)
AddService("small-service", {'parttime1' : 5, 'parttime2' : 5, 'parttime3' : 5, 'manager' : 3, 'exec' : 1}, (9.0, 21.00), 20, 0.5)
AddService("large-service", {'parttime1' : 15, 'parttime2' : 15, 'parttime3' : 15, 'manager' : 10, 'seniormgr' : 4, 'exec' : 1}, (9.0, 21.00), 60, 1.0)

AddFood("coffee", { 'barrista1' : 3, 'barrista2' : 3, 'barrista3' : 2, 'barrista4' : 2, 'storemgr1' : 1, 'storemgr2' : 1}, (6.0, 22.0), 10, 0.25)
AddFood("fastfood", {'parttime1' : 5, 'parttime2' : 8, 'parttime3' : 8, 'parttime4' : 5, 'manager' : 2}, (8.0, 24.0), 30, 0.5)
AddFood("small-restaurant", {'parttime2' : 4, 'parttime3' : 6, 'parttime4' : 4, 'manager' : 2}, (12.0, 24.0), 20, 1.5)
AddFood("large-restaurant", {'parttime2' : 8, 'parttime3' : 12, 'parttime4' : 12, 'manager' : 3}, (12.0, 24.0), 40, 1.5)

AddSchool("elem-school", { 'student' : 200, 'teacher' : 10, 'admin' : 2, 'principal' : 1})
AddSchool("middle-school", { 'student' : 300, 'teacher' : 20, 'admin' : 4, 'principal' : 2})
AddSchool("high-school", { 'student' : 400, 'teacher' : 30, 'admin' : 8, 'principal' : 4})
