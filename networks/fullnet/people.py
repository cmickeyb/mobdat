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
from mobdat.common.graph import Generators, SocialEdges

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
                person.SetJob(job)
                world.SetEmployer(person, biz)

                person.SetVehicle(wprof.VehicleType.PickVehicleType())

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
    weightgen = Generators.GaussianWeightGenerator(edgeweight)
    Generators.Generators.RMAT(world, people, edgefactor, quadrants, weightgen = weightgen, edgetype = SocialEdges.ConnectedTo)

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
def PropagatePreference(seeds, preference, seedweight, minweight) :
    nodequeue = set()

    # set the initial weights for the seed nodes, add adjacent nodes
    # to the queue to be processed
    for seed in seeds :
        seed.Preference.SetWeight(preference, seedweight)
        for edge in seed.IterOutputEdges(edgetype = 'ConnectedTo') :
            nodequeue.add(edge.EndNode)

    # process the queue, this is a little dangerous because of the
    # potential for lack of convergence or at least the potential
    # for convergence taking a very long time
    totalprocessed = 0
    while len(nodequeue) > 0 :
        totalprocessed += 1
        node = nodequeue.pop()
        oldweight = node.Preference.GetWeight(preference, 0.0)

        # compute the weight for this node as the weighted average
        # of all the nodes that point to it
        count = 0
        aggregate = 0
        for edge in node.IterInputEdges(edgetype = 'ConnectedTo') :
            count += 1
            aggregate += edge.StartNode.Preference.GetWeight(preference, 0.0) * edge.Weight.Weight

        newweight = aggregate / count
        if abs(oldweight - newweight) > minweight :
            node.Preference.SetWeight(preference, newweight)
            # logger.debug('propogate preference {0} to person {1} with weight {2:1.4f}'.format(preference, node.Name, newweight))

            for edge in node.IterOutputEdges(edgetype = 'ConnectedTo') :
                nodequeue.add(edge.EndNode)

    logger.info('total nodes process {0} for preference {1}'.format(totalprocessed, preference))

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

        PropagatePreference(seeds, biz.Name, random.uniform(0.7, 0.9), 0.03)

people = world.FindNodes(nodetype = 'Person')
PropagateBusinessPreference(people, SocialDecoration.BusinessType.Food, 'coffee')
PropagateBusinessPreference(people, SocialDecoration.BusinessType.Food, 'fastfood')
PropagateBusinessPreference(people, SocialDecoration.BusinessType.Food, 'small-restaurant')
PropagateBusinessPreference(people, SocialDecoration.BusinessType.Food, 'large-restaurant')
PropagateBusinessPreference(people, SocialDecoration.BusinessType.Service, None)

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
logger.info("Loaded fullnet people builder extension file")
