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

@file    LayoutNodes.py
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
from mobdat.common import LayoutDecoration

logger = logging.getLogger(__name__)

## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class IntersectionType(Graph.Node) :
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
        Graph.Node.__init__(self, name = name)

        self.AddDecoration(LayoutDecoration.IntersectionTypeDecoration(name, itype, render))

## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class Intersection(Graph.Node) :
    WEST  = 0
    NORTH = 1
    EAST  = 2
    SOUTH = 3

    # -----------------------------------------------------------------
    def __init__(self, name, itype, x, y) :
        """
        Args:
            name -- string
            itype -- object of type Layout.IntersectionType
            x, y -- integer coordinates
        """
        Graph.Node.__init__(self, name = name)
        
        self.AddDecoration(LayoutDecoration.CoordDecoration(x, y))
        itype.AddMember(self)

    # -----------------------------------------------------------------
    @property
    def X(self) :
        return self.Coord.X

    # -----------------------------------------------------------------
    @property
    def Y(self) :
        return self.Coord.Y

    # -----------------------------------------------------------------
    def _EdgeMapPosition(self, node) :
        deltax = node.X - self.X
        deltay = node.Y - self.Y
        # west
        if deltax < 0 and deltay == 0 :
            return self.WEST
        # north
        elif deltax == 0 and deltay > 0 :
            return self.NORTH
        # east
        elif deltax > 0 and deltay == 0 :
            return self.EAST
        # south
        elif deltax == 0 and deltay < 0 :
            return self.SOUTH

        # this means that self & node are at the same location
        return -1 

    # -----------------------------------------------------------------
    def WestEdge(self) :
        emap = self.OutputEdgeMap()
        return emap[self.WEST]

    # -----------------------------------------------------------------
    def NorthEdge(self) :
        emap = self.OutputEdgeMap()
        return emap[self.NORTH]

    # -----------------------------------------------------------------
    def EastEdge(self) :
        emap = self.OutputEdgeMap()
        return emap[self.EAST]

    # -----------------------------------------------------------------
    def SouthEdge(self) :
        emap = self.OutputEdgeMap()
        return emap[self.SOUTH]

    # -----------------------------------------------------------------
    def OutputEdgeMap(self) :
        edgemap = [None, None, None, None]
        for e in self.IterOutputEdges('Road') :
            position = self._EdgeMapPosition(e.EndNode)
            edgemap[position] = e

        return edgemap

    # -----------------------------------------------------------------
    def InputEdgeMap(self) :
        edgemap = [None, None, None, None]
        for e in self.IterInputEdges('Road') :
            position = self._EdgeMapPosition(e.StartNode)
            edgemap[position] = e

        return edgemap

    # -----------------------------------------------------------------
    # signature returned is west, north, east, south
    # -----------------------------------------------------------------
    def Signature(self) :
        osignature = []
        for e in self.OutputEdgeMap() :
            sig = e.RoadType.Signature if e else '0L'
            osignature.append(sig)

        isignature = []
        for e in self.InputEdgeMap() :
            sig = e.RoadType.Signature if e else '0L'
            isignature.append(sig)

        signature = []
        for i in range(0,4) :
            signature.append("{0}/{1}".format(osignature[i], isignature[i]))

        return signature

## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
##class EndPoint(Graph.Node) :
class EndPoint(Intersection) :

    # -----------------------------------------------------------------
    def __init__(self, name, itype, x, y) :
        """
        Args:
            name -- string
            itype -- object of type Layout.IntersectionType
            x, y -- integer coordinates
        """
        Intersection.__init__(self, name, itype, x, y)
        self.AddDecoration(LayoutDecoration.EndPointDecoration())

## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class BusinessLocation(Graph.Node) :

    # -----------------------------------------------------------------
    def __init__(self, name, profile) :
        """
        Args:
            name -- string
            profile -- object of type BusinessLocationProfile
        """
        Graph.Node.__init__(self, name = name)
        
        self.AddDecoration(LayoutDecoration.BusinessLocationDecoration())
        profile.AddMember(self)

    # -----------------------------------------------------------------
    def AddEndpointToLocation(self, endpoint) :
        """
        Args:
            endpoint -- object of type LayoutNodes.EndPoint
        """
        self.AddMember(endpoint)

## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class ResidentialLocation(Graph.Node) :

    # -----------------------------------------------------------------
    def __init__(self, name, profile) :
        """
        Args:
            name -- string
            profile -- object of type ResidentialLocationProfile
        """
        Graph.Node.__init__(self, name = name)
        
        self.AddDecoration(LayoutDecoration.ResidentialLocationDecoration())
        profile.AddMember(self)

    # -----------------------------------------------------------------
    def AddEndpointToLocation(self, endpoint) :
        """
        Args:
            endpoint -- object of type LayoutNodes.EndPoint
        """
        self.AddMember(endpoint)


## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class BusinessLocationProfile(Graph.Node) :

    # -----------------------------------------------------------------
    def __init__(self, name, employees, customers, types) :
        """
        Args:
            name -- string
            employees -- integer, max number of employees per node
            customers -- integer, max number of customers per node
            types -- dict mapping Business.BusinessTypes to count
        """
        Graph.Node.__init__(self, name = name)
        
        self.AddDecoration(LayoutDecoration.BusinessLocationProfileDecoration(employees, customers, types))

## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class ResidentialLocationProfile(Graph.Node) :

    # -----------------------------------------------------------------
    def __init__(self, name, residents) :
        """
        Args:
            residents -- integer, max number of residents per node
        """
        Graph.Node.__init__(self, name = name)
        
        self.AddDecoration(LayoutDecoration.ResidentialLocationProfileDecoration(residents))

## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class RoadType(Graph.Node) :
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
        Graph.Node.__init__(self, name = name)

        self.AddDecoration(LayoutDecoration.RoadTypeDecoration(name, lanes, pri, speed, wid, sig, render, center))
