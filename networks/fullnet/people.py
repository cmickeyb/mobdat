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
from mobdat.common.graph import Generator, Propagator, SocialEdges, SocialNodes

import random, math

logger = logging.getLogger('people')

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
wprof = world.AddPersonProfile('worker')
sprof = world.AddPersonProfile('student')
hprof = world.AddPersonProfile('homemaker')

pmap = {}
pmap['worker'] = wprof
pmap['student'] = sprof
pmap['homemaker'] = hprof

for vtype in laysettings.VehicleTypes.itervalues() :
    for ptype in vtype.ProfileTypes :
        pmap[ptype].VehicleType.AddVehicleType(vtype.Name, vtype.Rate)

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

# -----------------------------------------------------------------
def IrwinHallDistribution(mean) :
    count = 5
    v = math.fsum([random.random() for n in range(0, count)]) / float(count)
    # v is now distributed across the range 0 to 1
    if v < 0.5 :
        return v * mean / 0.5
    else :
        return mean + (v - 0.5) * (1 - mean) / 0.5

# -----------------------------------------------------------------
RulePreferences = {
    'CoffeeBeforeWork' : 0.6,
    'LunchDuringWork' : 0.75,
    'RestaurantAfterWork' : 0.8,
    'ShoppingTrip' : 0.8
    }

def SetRulePreferences(person) :
    global RulePreferences

    for key, val in RulePreferences.iteritems() :
        person.Preference.SetWeight('rule_' + key, IrwinHallDistribution(val))

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
        world.SetResidence(person, endpoint)

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
                world.SetEmployer(person, biz)

                SocialNodes.Person.SetJob(person, job)
                SocialNodes.Person.SetVehicle(person, wprof.VehicleType.PickVehicleType())
                SetRulePreferences(person)

                location = PlacePerson(person)
                if not location :
                    logger.warn('ran out of residences after %d people', people)
                    return

    logger.info('created %d people', people)

PlacePeople()

# -----------------------------------------------------------------
def ConnectPeople(people, edgefactor, quadrants, edgeweight = 0.5) :
    """
    Args:
        people -- list of SocialNodes.People objects
        edgefactor -- relative number of edges between people
        quadrants -- vector integers that distributes the density of small world effects
    """

    global world
    weightgen = Generator.GaussianWeightGenerator(edgeweight)
    Generator.RMAT(world, people, edgefactor, quadrants, weightgen = weightgen, edgetype = SocialEdges.ConnectedTo)

# Connect the world
ConnectPeople(world.FindNodes(nodetype = 'Person'), 5, (4, 5, 6, 7), 0.5)

# Connect people who work at the same business
for name, biz in world.IterNodes(nodetype = 'Business') :
    employees = []
    for edge in biz.IterInputEdges(edgetype = 'EmployedBy') :
        employees.append(edge.StartNode)

    ConnectPeople(employees, 5, (4, 5, 6, 7), 0.8)

# Connect people who live in the same area
# TBD

# -----------------------------------------------------------------
bizcache = {}
def PropagateBusinessPreference(people, biztype, bizclass, seedsize = (5, 15)) :
    global bizcache, world

    if (biztype, bizclass) not in bizcache :
        bizcache[(biztype, bizclass)] = SocialDecoration.BusinessProfileDecoration.FindByType(world, biztype, bizclass)

    bizlist = bizcache[(biztype, bizclass)]

    incr = len(people) / 100.0

    for biz in bizlist :
        logger.info('generating preferences for {0}'.format(biz.Name))
        seedcount = random.randint(int(incr * seedsize[0]), int(incr * seedsize[1]))
        seeds = random.sample(people, seedcount)

        Propagator.PropagateAveragePreference(seeds, biz.Name, random.uniform(0.7, 0.9), 0.03)

people = world.FindNodes(nodetype = 'Person')
PropagateBusinessPreference(people, SocialDecoration.BusinessType.Food, 'coffee')
PropagateBusinessPreference(people, SocialDecoration.BusinessType.Food, 'fastfood')
PropagateBusinessPreference(people, SocialDecoration.BusinessType.Food, 'small-restaurant')
PropagateBusinessPreference(people, SocialDecoration.BusinessType.Food, 'large-restaurant')
PropagateBusinessPreference(people, SocialDecoration.BusinessType.Service, None)

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
logger.info("Loaded fullnet people builder extension file")
