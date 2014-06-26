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

@file    Propagator.py
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

logger = logging.getLogger(__name__)

# -----------------------------------------------------------------
def PropagateAveragePreference(seeds, preference, seedweight, minweight) :
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

