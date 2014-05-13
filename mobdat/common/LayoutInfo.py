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

@file    LayoutInfo.py
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

from mobdat.common import Graph, Decoration
from mobdat.common import LayoutNodes, LayoutEdges, LayoutDecoration

import json, re

logger = logging.getLogger(__name__)

## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class LayoutInfo(Graph.Graph) :

    # -----------------------------------------------------------------
    @staticmethod
    def LoadFromFile(filename) :
        with open(filename, 'r') as fp :
            netdata = json.load(fp)

        graph = LayoutInfo()
        graph.Load(netdata)

        return graph

    # -----------------------------------------------------------------
    def __init__(self) :
        Graph.Graph.__init__(self)

        for dtype in LayoutDecoration.CommonDecorations :
            self.AddDecorationHandler(dtype)

    # =================================================================
    # =================================================================

    # -----------------------------------------------------------------
    def AddIntersectionType(self, itype) :
        """
        Args:
            itype -- object of type LayoutNodes.IntersectionType
        """
        self.AddNode(itype)
        
    # -----------------------------------------------------------------
    def AddIntersection(self, intersection) :
        """
        Args:
            intersection -- object of type LayoutNodes.Intersection
        """
        self.AddNode(intersection)
        
    # -----------------------------------------------------------------
    def AddEndPoint(self, endpoint) :
        """
        Args:
            endpoint -- object of type LayoutNodes.Intersection
        """
        self.AddNode(endpoint)
        
    # -----------------------------------------------------------------
    def AddBusinessLocationProfile(self, profile) :
        """
        Args:
            profile -- object of type LayoutNodes.BusinessLocationProfile
        """
        self.AddNode(profile)

    # -----------------------------------------------------------------
    def AddResidentialLocationProfile(self, profile) :
        """
        Args:
            profile -- object of type LayoutNodes.ResidentialLocationProfile
        """
        self.AddNode(profile)

    # -----------------------------------------------------------------
    def AddBusinessLocation(self, location) :
        """
        Args:
            location -- object of type LayoutNodes.BusinessLocation
        """
        self.AddNode(location)

    # -----------------------------------------------------------------
    def AddResidentialLocation(self, location) :
        """
        Args:
            location -- object of type LayoutNodes.ResidentialLocation
        """
        self.AddNode(location)

    # -----------------------------------------------------------------
    def AddRoadType(self, roadtype) :
        """
        Args:
            roadtype -- object of type LayoutNodes.RoadType
        """
        self.AddNode(roadtype)

    # -----------------------------------------------------------------
    def AddRoad(self, road) :
        """
        Args:
            profile -- object of type LayoutEdges.Road
        """
        self.AddEdge(road)

    # =================================================================
    # =================================================================

    # -----------------------------------------------------------------
    def FindNodesInRange(self, x, y, dist) :
        result = []
        sqdist = int(dist) * int(dist)
        for n in self.Nodes.itervalues() :
            cdist = (n.Coord.X - x)**2 + (n.Coord.Y - y)**2
            if cdist < sqdist :
                result.append(n)

        return result

    # -----------------------------------------------------------------
    def FindClosestNode(self, node) :
        cnode = None
        cdist = 0

        for n in self.Nodes.itervalues() :
            if cnode== None :
                cnode = n
                cdist = (cnode.X - node.X)**2 + (cnode.Y - node.Y)**2
                continue
            dist = (n.X - node.X)**2 + (n.Y - node.Y)**2
            if (dist < cdist) :
                cnode = n
                cdist = dist
            
        return cnode

