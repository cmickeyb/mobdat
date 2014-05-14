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

@file    fullnet/people.py
@author  Mic Bowman
@date    2014-02-04

This file contains the programmatic specification of the fullnet 
social framework including people and businesses.

"""

import os, sys
import logging

sys.path.append(os.path.join(os.environ.get("SUMO_HOME"), "tools"))
sys.path.append(os.path.join(os.environ.get("OPENSIM","/share/opensim"),"lib","python"))
#sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), "..")))
#sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "lib")))

from mobdat.common.Utilities import GenName

import random

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
wprof = world.AddPersonProfile('worker')
sprof = world.AddPersonProfile('student')
hprof = world.AddPersonProfile('homemaker')

# for vtype in laysettings.VehicleTypes.itervalues() :
#     print vtype.Name
#     for ptype in vtype.ProfileTypes :
#         world.PersonProfiles[ptype].AddVehicleType(vtype.Name, vtype.Rate)

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

# -----------------------------------------------------------------
ResidentialNodes = None

def PlacePerson(person) :
    global ResidentialNodes
    if not ResidentialNodes :
        ResidentialNodes = world.FindNodes(nodetype = 'ResidentialLocation')

    bestloc = None
    bestfit = 0
    for location in ResidentialNodes :
        fitness = location.ResidentialLocation.Fitness(person)
        if fitness > bestfit :
            bestfit = fitness
            bestloc = location

    if bestloc :
        endpoint = bestloc.ResidentialLocation.AddResident(person)
        person.SetResidence(endpoint)

    return bestloc

# -----------------------------------------------------------------
def PlacePeople() :
    global world

    profile = world.FindNodeByName('worker')

    bizlist = {}
    for name, biz in world.IterNodes(nodetype = 'Business') :
        bizlist[name] = biz

    people = 0
    for name, biz in bizlist.iteritems() :
        bprof = biz.EmploymentProfile
        for job, demand in bprof.JobList.iteritems() :
            for p in range(0, demand) :
                people += 1
                name = GenName(wprof.Name)
                person = world.AddPerson(name, wprof)
                person.SetJob(job)
                world.SetEmployer(person, biz)

                location = PlacePerson(person)
                if not location :
                    print 'ran out of residences after %s people' % people
                    return


    print 'created %s people' % people

PlacePeople()

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
print "Loaded fullnet people builder extension file"
