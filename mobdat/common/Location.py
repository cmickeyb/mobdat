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

import random

## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
def restrict (val, minval, maxval):
    if val < minval: return minval
    if val > maxval: return maxval
    return val

## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class LocationProfile :

    # -----------------------------------------------------------------
    def __init__(self, name) :
        self.ProfileName = name

    # -----------------------------------------------------------------
    def Dump(self) :
        result = dict()
        result['ProfileName'] = self.ProfileName

        return result
        

## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class BusinessLocationProfile(LocationProfile) :

    # -----------------------------------------------------------------
    @staticmethod
    def Load(info) :
        profile = BusinessLocationProfile(info['ProfileName'])
        profile.EmployeesPerNode = info['EmployeesPerNode']
        profile.CustomersPerNode = info['CustomersPerNode']
        profile.PreferredBusinessTypes = info['PreferredBusinessTypes']  # should this be a copy?

        return profile

    # -----------------------------------------------------------------
    def __init__(self, name, employees = 20, customers = 50, types = {}) :
        LocationProfile.__init__(self, name)

        self.EmployeesPerNode = employees
        self.CustomersPerNode = customers
        self.PreferredBusinessTypes = types

    # -----------------------------------------------------------------
    def Fitness(self, business) :
        btype = business.Profile.BusinessType
        return self.PreferredBusinessTypes[btype] if btype in self.PreferredBusinessTypes else 0.0

    # -----------------------------------------------------------------
    def Dump(self) :
        result = LocationProfile.Dump(self)

        result['EmployeesPerNode'] = self.EmployeesPerNode
        result['CustomersPerNode'] = self.CustomersPerNode
        result['PreferredBusinessTypes'] = self.PreferredBusinessTypes        

        return result

## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class ResidentialLocationProfile(LocationProfile) :

    # -----------------------------------------------------------------
    @staticmethod
    def Load(info) :
        profile = ResidentialLocationProfile(info['ProfileName'])
        profile.ResidentsPerNode = info['ResidentsPerNode']

        return profile

    # -----------------------------------------------------------------
    def __init__(self, name, residents = 5) :
        LocationProfile.__init__(self, name)

        self.ResidentsPerNode = residents

    # -----------------------------------------------------------------
    def Fitness(self, resident) :
        return 1

    # -----------------------------------------------------------------
    def Dump(self) :
        result = LocationProfile.Dump(self)

        result['ResidentsPerNode'] = self.ResidentsPerNode

        return result

## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class Location :

    # -----------------------------------------------------------------
    def __init__(self, capsule, profile) :
        self.Capsule = capsule
        self.LocationProfile = profile

    # -----------------------------------------------------------------
    def Dump(self) :
        result = dict()
        result['Capsule'] = self.Capsule.Name
        result['LocationProfile'] = self.LocationProfile.ProfileName

        return result

## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class BusinessLocation(Location) :

    # -----------------------------------------------------------------
    @staticmethod
    def Load(info, locinfo, bizinfo) :
        capsule = locinfo.CapsuleMap[info['Capsule']]
        profile = bizinfo.BusinessLocationProfiles[info['LocationProfile']]
        location = BusinessLocation(capsule, profile)

        return location

    # -----------------------------------------------------------------
    def __init__(self, capsule, profile) :
        Location.__init__(self, capsule, profile)

        self.Residents = []
        self.PeakEmployeeCount = 0
        self.PeakCustomerCount = 0
        self.EmployeeCapacity = len(self.Capsule.Members) * self.LocationProfile.EmployeesPerNode
        self.CustomerCapacity = len(self.Capsule.Members) * self.LocationProfile.CustomersPerNode

    # -----------------------------------------------------------------
    @property
    def SourceName(self) :
        node = random.choice(self.Capsule.Members)
        return node.EndPoint.SourceName

    # -----------------------------------------------------------------
    @property
    def DestinationName(self) :
        node = random.choice(self.Capsule.Members)
        return node.EndPoint.DestinationName

    # -----------------------------------------------------------------
    def Fitness(self, business) :
        ecount = self.PeakEmployeeCount + business.PeakEmployeeCount
        ccount = self.PeakCustomerCount + business.PeakCustomerCount

        if ecount >= self.EmployeeCapacity : return 0
        if ccount >= self.CustomerCapacity : return 0

        invweight = (ecount / self.EmployeeCapacity + ccount / self.CustomerCapacity) / 2.0
        fitness = restrict(random.gauss(1.0 - invweight, 0.1), 0, 1.0) * self.LocationProfile.Fitness(business) 
        return fitness

    # -----------------------------------------------------------------
    def AddBusiness(self, business) :
        self.PeakEmployeeCount += business.PeakEmployeeCount
        self.PeakCustomerCount += business.PeakCustomerCount
        self.Residents.append(business)

    # -----------------------------------------------------------------
    def Dump(self) :
        result = Location.Dump(self)
        return result

## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class Residence :
    # -----------------------------------------------------------------
    def __init__(self, capsule, node) :
        self.Capsule = capsule
        self.Node = node
        self.Residents = []

    # -----------------------------------------------------------------
    @property
    def SourceName(self) :
        return self.Node.EndPoint.SourceName

    # -----------------------------------------------------------------
    @property
    def DestinationName(self) :
        return self.Node.EndPoint.DestinationName

## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class ResidentialLocation(Location) :

    # -----------------------------------------------------------------
    @staticmethod
    def Load(info, locinfo, perinfo) :
        capsule = locinfo.CapsuleMap[info['Capsule']]
        profile = perinfo.ResidentialLocationProfiles[info['LocationProfile']]
        location = ResidentialLocation(capsule, profile)

        return location

    # -----------------------------------------------------------------
    def __init__(self, capsule, profile) :
        Location.__init__(self, capsule, profile)

        self.ResidentCount = 0
        self.ResidentCapacity = len(self.Capsule.Members) * self.LocationProfile.ResidentsPerNode

        self.ResidenceList = {}
        for node in self.Capsule.Members :
            self.ResidenceList[node.Name] = Residence(self.Capsule, node)

    # -----------------------------------------------------------------
    def Fitness(self, person) :
        if self.ResidentCount >= self.ResidentCapacity : return 0

        invweight = self.ResidentCount / self.ResidentCapacity
        return restrict(random.gauss(1.0 - invweight, 0.1), 0, 1.0) * self.LocationProfile.Fitness(person)

    # -----------------------------------------------------------------
    def AddPerson(self, person) :
        bestcnt = self.LocationProfile.ResidentsPerNode + 1
        bestfit = None

        for residence in self.ResidenceList.itervalues() :
            if len(residence.Residents) < bestcnt :
                bestcnt = len(residence.Residents)
                bestfit = residence

        if bestfit :
            self.ResidentCount += 1
            bestfit.Residents.append(person)

        return bestfit

    # -----------------------------------------------------------------
    def AddPersonToNode(self, person, nodename) :
        """
        AddPersonToNode -- add a person to a specific node

        person -- an object of type Person
        nodename -- the string name of a node in the capsule
        """

        self.ResidenceList[nodename].Residents.append(person)
        self.ResidentCount += 1

        return self.ResidenceList[nodename]

    # -----------------------------------------------------------------
    def Dump(self) :
        result = Location.Dump(self)
        return result
