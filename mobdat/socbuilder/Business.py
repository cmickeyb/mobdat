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

## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)

# -----------------------------------------------------------------
# -----------------------------------------------------------------
class JobProfile :
    def __init__(self, name, salary, flexible, workday, demand = 0) :
        self.ProfileName = name
        self.Salary = salary
        self.FlexibleHours = flexible
        self.StartOfWorkDay = workday[0]
        self.EndOfWorkDay = workday[1]
        self.Demand = demand

    def Copy(self) :
        hours = (self.StartOfWorkDay, self.EndOfWorkDay)
        return JobProfile(self.ProfileName, self.Salary, self.FlexibleHours, hours, self.Demand)

    def Dump(self) :
        return self.__dict__

# -----------------------------------------------------------------
# -----------------------------------------------------------------
class ServiceProfile :
    def __init__(self, bizhours, capacity, servicetime) :
        self.OpenTime = bizhours[0]
        self.CloseTime = bizhours[1]
        self.CustomerCapacity = capacity
        self.ServiceTime = servicetime

    def Dump(self) :
        return self.__dict__

# -----------------------------------------------------------------
# -----------------------------------------------------------------
class BusinessProfile :
    BusinessType = enum('Unknown', 'Factory', 'Service', 'Civic', 'Entertainment', 'School', 'Retail', 'Food')

    def __init__(self, bizname, biztype) :
        self.BusinessName = bizname
        self.BusinessType = biztype

        self.ServiceProfile = None
        self.JobList = []

    def Dump(self) :
        result = dict()
        result['BusinessName'] = self.BusinessName
        result['BusinessType'] = self.BusinessType
        result['JobList'] = []

        if self.ServiceProfile :
            result['ServiceProfile'] = self.ServiceProfile.Dump()

        for j in self.JobList :
            result['JobList'].append(j.Dump())

        return result

# -----------------------------------------------------------------
# -----------------------------------------------------------------
class BusinessData :
    def __init__(self) :
        self.CompanyList = []

    def Dump(self) :
        result = dict()
        result['CompanyList'] = []
        for c in self.CompanyList :
            result['CompanyList'].append(c.Dump())
            
        return result
