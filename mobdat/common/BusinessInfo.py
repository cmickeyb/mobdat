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

@file    BusinessInfo.py
@author  Mic Bowman
@date    2013-12-03

This file defines routines used to build features of a mobdat traffic
network such as building a grid of roads. 

"""

import os, sys
import logging

# we need to import python modules from the $SUMO_HOME/tools directory
sys.path.append(os.path.join(os.environ.get("OPENSIM","/share/opensim"),"lib","python"))
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "..")))
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "lib")))

from mobdat.common.ValueTypes import DaysOfTheWeek
from Decoration import *
import json

logger = logging.getLogger(__name__)

## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class WeeklySchedule :
    # -----------------------------------------------------------------
    @staticmethod
    def WorkWeekSchedule(stime, etime) :
        sched = [[] for x in range(DaysOfTheWeek.Mon, DaysOfTheWeek.Sun + 1)]

        # work week
        for d in range(DaysOfTheWeek.Mon, DaysOfTheWeek.Sat) :
            sched[d].append((stime,etime))

        return WeeklySchedule(sched)

    # -----------------------------------------------------------------
    @staticmethod
    def FullWeekSchedule(stime, etime) :
        sched = [[] for x in range(DaysOfTheWeek.Mon, DaysOfTheWeek.Sun + 1)]

        # work week
        for d in range(DaysOfTheWeek.Mon, DaysOfTheWeek.Sun + 1) :
            sched[d].append((stime,etime))

        return WeeklySchedule(sched)

    # -----------------------------------------------------------------
    @staticmethod
    def SpecialSchedule(**keywords) :
        sched = [[] for x in range(DaysOfTheWeek.Mon, DaysOfTheWeek.Sun + 1)]

        for key in keywords :
            if isinstance(keywords[key], tuple) :
                sched[DaysOfTheWeek.__dict__[key]].append(keywords[key])
            elif isinstance(keywords[key], list) :
                sched[DaysOfTheWeek.__dict__[key]].extend(keywords[key])

        return WeeklySchedule(sched)

    # -----------------------------------------------------------------
    def __init__(self, schedule) :
        for d in range(DaysOfTheWeek.Mon, DaysOfTheWeek.Sun + 1) :
            self.__dict__[DaysOfTheWeek.KeyName[d]] = schedule[d]

    # -----------------------------------------------------------------
    def ScheduleForDay(self, day) :
        day = day % (DaysOfTheWeek.Sun + 1)
        return sorted(self.__dict__[DaysOfTheWeek.KeyName[day]], key= lambda sched: sched[0])

    # -----------------------------------------------------------------
    def ScheduledAtTime(self, day, time) :
        time = time % 24
        for sched in self.ScheduleForDay(day) :
            if sched[0] <= time and time <= sched[1] :
                return True

        return False

    # -----------------------------------------------------------------
    def Dump(self) :
        result = []
        for d in range(DaysOfTheWeek.Mon, DaysOfTheWeek.Sun + 1) :
            result.append(self.ScheduleForDay(d))
        return result

## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class BusinessInfo :

    # -----------------------------------------------------------------
    @staticmethod
    def LoadFromFile(netinfo, filename) :
        with open(filename, 'r') as fp :
            bizdata = json.load(fp)

        bizinfo = BusinessInfo(netinfo)
        bizinfo.Load(bizdata)

        return bizinfo

    # -----------------------------------------------------------------
    def __init__(self, netinfo) :
        self.JobProfiles = {}

        self.BusinessProfiles = {}
        self.BusinessList = {}

        self.BusinessLocationProfiles = {}
        self.BusinessLocations = {}

    # -----------------------------------------------------------------
    def Load(self, bizdata) :
        for lpinfo in bizdata['BusinessLocationProfiles'] :
            locprofile = BusinessLocationProfile.Load(lpinfo)
            self.BusinessLocationProfiles[locprofile.ProfileName] = locprofile

        for linfo in bizdata['BusinessLocations'] :
            location = BusinessLocation.Load(linfo)
            self.BusinessLocations[location.Capsule.Name] = location

        for pinfo in bizdata['BusinessProfiles'] :
            profile = BusinessProfile.Load(pinfo)
            self.BusinessProfiles[profile.ProfileName] = profile

        for binfo in bizdata['BusinessList'] :
            business = Business.Load(binfo)
            self.BusinessList[business.Name] = business

    # -----------------------------------------------------------------
    def Dump(self) :
        result = dict()

        result['BusinessLocationProfiles'] = []
        for blp in self.BusinessLocationProfiles.itervalues() :
            result['BusinessLocationProfiles'].append(blp.Dump())

        result['BusinessLocations'] = []
        for bl in self.BusinessLocations :
            result['BusinessLocations'].append(bl.Dump())

        result['BusinessProfiles'] = []
        for p in self.BusinessProfiles.itervalues() :
            result['BusinessProfiles'].append(p.Dump())

        result['BusinessList'] = []
        for c in self.BusinessList.itervalues() :
            result['BusinessList'].append(c.Dump())

        return result
