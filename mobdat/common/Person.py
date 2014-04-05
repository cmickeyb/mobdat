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

from mobdat.common.Business import JobProfile
import random

## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class PersonProfile :

    # -----------------------------------------------------------------
    @staticmethod
    def Load(info) :
        name = info['ProfileName']
        profile = PersonProfile(name)

        for name, rate in info['VehicleTypes'].iteritems() :
            profile.AddVehicleType(name, rate)

        return profile

    # -----------------------------------------------------------------
    def __init__(self, name) :
        self.ProfileName = name
        self.VehicleTypes = {}
        self.VehicleTypeList = None

    # -----------------------------------------------------------------
    def AddVehicleType(self, name, rate) :
        self.VehicleTypes[name] = rate
        self.VehicleTypeList = None  # so we'll rebuild the map when needed

    # -----------------------------------------------------------------
    def PickVehicleType(self) :
        if not self.VehicleTypeList :
            self.VehicleTypeList = []
            for name, rate in self.VehicleTypes.iteritems() :
                self.VehicleTypeList.extend([name for x in range(rate)])

        return random.choice(self.VehicleTypeList)

    # -----------------------------------------------------------------
    def Dump(self) :
        result = dict()
        result['ProfileName'] = self.ProfileName
        result['VehicleTypes'] = self.VehicleTypes

        return result
        
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class Person :

    # -----------------------------------------------------------------
    @staticmethod
    def Load(info, locinfo, bizinfo, perinfo) :
        name = info['Name']
        profile = perinfo.PersonProfiles[info['ProfileName']]
        employer = bizinfo.BusinessList[info['Employer']]
        job = JobProfile.Load(info['Job'])
        vtype = info['VehicleType']

        person = Person(name, profile, employer, job, vtype = vtype)

        rezlocation = locinfo.ResidentialLocations[info['Residence']['CapsuleName']]
        person.Residence = rezlocation.AddPersonToNode(person, info['Residence']['NodeName'])

        return person

    # -----------------------------------------------------------------
    def __init__(self, name, profile, employer, job, vtype = None, residence = None) :
        self.Name = name
        self.Profile = profile
        self.Employer = employer
        self.Job = job
        self.VehicleType = vtype or profile.PickVehicleType()
        self.Residence = residence

    # -----------------------------------------------------------------
    def Dump(self) :
        result = dict()
        result['Name'] = self.Name
        result['ProfileName'] = self.Profile.ProfileName
        result['Employer'] = self.Employer.Name
        result['Job'] = self.Job.Dump()
        result['Residence'] = { 'CapsuleName' : self.Residence.Capsule.Name, 'NodeName' : self.Residence.Node.Name }
        result['VehicleType'] = self.VehicleType

        return result
