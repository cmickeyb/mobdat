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

from mobdat.common.Decoration import *
from mobdat.common.LayoutDecoration import *
from mobdat.common import Graph

import uuid, re
import json

logger = logging.getLogger(__name__)

## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class IntersectionType(Graph.Collection) :
    """
    The IntersectionType class is used to specify parameters for rendering
    intersections in Sumo and OpenSim.
    """

    # -----------------------------------------------------------------
    def __init__(self, name, itype, render) :
        """
        Args:
            name -- string
            itype -- string, indicates the stop light type for the intersection
            render -- boolean, flag to indicate that opensim should render the object
        """
        Graph.Collection.__init__(self, name = name)

        self.AddDecoration(IntersectionTypeDecoration(name, itype, render))

## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class Intersection(Graph.Node) :

    # -----------------------------------------------------------------
    def __init__(self, name, itype, x, y) :
        """
        Args:
            name -- string
            itype -- object of type Layout.IntersectionType
            x, y -- integer coordinates
        """
        Graph.Node.__init__(self, name)
        
        self.AddDecoration(CoordDecoration(x, y))
        itype.AddMember(self)

    # -----------------------------------------------------------------
    @property
    def X(self) :
        return self.Coord.X

    # -----------------------------------------------------------------
    @property
    def Y(self) :
        return self.Coord.Y

## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class EndPoint(Graph.Node) :

    # -----------------------------------------------------------------
    def __init__(self, name, itype, x, y) :
        """
        Args:
            name -- string
            itype -- object of type Layout.IntersectionType
            x, y -- integer coordinates
        """
        Graph.Node.__init__(self, name)
        
        self.AddDecoration(CoordDecoration(x, y))
        itype.AddMember(self)

    # -----------------------------------------------------------------
    @property
    def X(self) :
        return self.Coord.X

    # -----------------------------------------------------------------
    @property
    def Y(self) :
        return self.Coord.Y

## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class BusinessLocation(Graph.Collection) :

    # -----------------------------------------------------------------
    def __init__(self, name, profile) :
        """
        Args:
            name -- string
            profile -- object of type BusinessLocationProfile
        """
        Graph.Collection.__init__(self, name = name)
        
        profile.AddMember(self)

    # -----------------------------------------------------------------
    def AddEndpointToLocation(self, endpoint) :
        """
        Args:
            endpoint -- object of type LayoutInfo.EndPoint
        """
        self.AddMember(endpoint)

## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class ResidentialLocation(Graph.Collection) :

    # -----------------------------------------------------------------
    def __init__(self, name, profile) :
        """
        Args:
            name -- string
            profile -- object of type ResidentialLocationProfile
        """
        Graph.Collection.__init__(self, name = name)
        
        profile.AddMember(self)

    # -----------------------------------------------------------------
    def AddEndpointToLocation(self, endpoint) :
        """
        Args:
            endpoint -- object of type LayoutInfo.EndPoint
        """
        self.AddMember(endpoint)


## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class BusinessLocationProfile(Graph.Collection) :

    # -----------------------------------------------------------------
    def __init__(self, name, employees, customers, types) :
        """
        Args:
            name -- string
            employees -- integer, max number of employees per node
            customers -- integer, max number of customers per node
            types -- dict mapping Business.BusinessTypes to count
        """
        Graph.Collection.__init__(self, name = name)
        
        self.AddDecoration(BusinessLocationProfileDecoration(employees, customers, types))

## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class ResidentialLocationProfile(Graph.Collection) :

    # -----------------------------------------------------------------
    def __init__(self, name, residents) :
        """
        Args:
            residents -- integer, max number of residents per node
        """
        Graph.Collection.__init__(self, name = name)
        
        self.AddDecoration(ResidentialLocationProfileDecoration(residents))

## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class RoadType(Graph.Collection) :
    """
    The RoadType class is used to specify parameters for rendering roads
    in Sumo and OpenSim.
    """

    # -----------------------------------------------------------------
    def __init__(self, name, lanes, pri, speed, wid, sig, render, center) :
        """
        Args:
            name -- string
            lanes -- integer, number of lanes in the road
            pri -- integer, priority for stop lights
            speed -- float, maximum speed allowed on the road
            sig -- string, signature
            render -- boolean, flag to indicate whether opensim should render
            center -- boolean, flag to indicate the coordinate origin 
        """
        Graph.Collection.__init__(self, name = name)

        self.AddDecoration(RoadTypeDecoration(name, lanes, pri, speed, wid, sig, render, center))

## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class Road(Graph.Edge) :
    def __init__(self, name, snode, enode, etype) :
        """
        Args:
            snode -- object of type Intersection
            enode -- object of type Intersection
            etype -- object of type LayoutInfo.RoadType (Graph.Collection)
            name -- string
        """
        Graph.Edge.__init__(self, snode, enode, name)

        self.AddDecoration(EdgeTypeDecoration('Road'))
        etype.AddMember(self)


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

        for dtype in CommonDecorations :
            self.AddDecorationHandler(dtype)

    # =================================================================
    # =================================================================

    # -----------------------------------------------------------------
    def AddIntersectionType(self, itype) :
        """
        Args:
            itype -- object of type LayoutInfo.IntersectionType
        """
        self.AddCollection(itype)
        
    # -----------------------------------------------------------------
    def AddIntersection(self, intersection) :
        """
        Args:
            intersection -- object of type LayoutInfo.Intersection
        """
        self.AddNode(intersection)
        
    # -----------------------------------------------------------------
    def AddEndPoint(self, endpoint) :
        """
        Args:
            endpoint -- object of type LayoutInfo.Intersection
        """
        self.AddNode(endpoint)
        
    # -----------------------------------------------------------------
    def AddBusinessLocationProfile(self, profile) :
        """
        Args:
            profile -- object of type LayoutInfo.BusinessLocationProfile
        """
        self.AddCollection(profile)

    # -----------------------------------------------------------------
    def AddResidentialLocationProfile(self, profile) :
        """
        Args:
            profile -- object of type LayoutInfo.ResidentialLocationProfile
        """
        self.AddCollection(profile)

    # -----------------------------------------------------------------
    def AddBusinessLocation(self, location) :
        """
        Args:
            location -- object of type LayoutInfo.BusinessLocation
        """
        self.AddCollection(location)

    # -----------------------------------------------------------------
    def AddResidentialLocation(self, location) :
        """
        Args:
            location -- object of type LayoutInfo.ResidentialLocation
        """
        self.AddCollection(location)

    # -----------------------------------------------------------------
    def AddRoadType(self, roadtype) :
        """
        Args:
            roadtype -- object of type LayoutInfo.RoadType
        """
        self.AddCollection(roadtype)

    # -----------------------------------------------------------------
    def AddRoad(self, road) :
        """
        Args:
            profile -- object of type LayoutInfo.Road
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

