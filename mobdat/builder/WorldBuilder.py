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

@file    LayoutBuilder.py
@author  Mic Bowman
@date    2013-12-03

This file defines routines used to build features of a mobdat traffic
network such as building a grid of roads. 

"""

import os, sys, copy
import logging

# we need to import python modules from the $SUMO_HOME/tools directory
sys.path.append(os.path.join(os.environ.get("OPENSIM","/share/opensim"),"lib","python"))
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "lib")))

from mobdat.common import WorldInfo
from mobdat.common import LayoutNodes, LayoutEdges, LayoutDecoration
from mobdat.common import SocialNodes, SocialEdges, SocialDecoration

from mobdat.common.Utilities import GenName, GenNameFromCoordinates
from mobdat.common import Graph

import re, json

logger = logging.getLogger(__name__)

## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class ResidentialGenerator :

    # -----------------------------------------------------------------
    def __init__(self, etype, itype, dtype, rtype, driveway = 10, bspace = 20, spacing = 20, both = True) :
        self.RoadType = etype
        self.IntersectionType = itype
        self.DrivewayType = dtype
        self.ResidentialType = rtype
        self.DrivewayLength = driveway
        self.DrivewayBuffer = bspace
        self.Spacing = spacing
        self.BothSides = both

## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class WorldBuilder(WorldInfo.WorldInfo) :

    # -----------------------------------------------------------------
    @staticmethod
    def LoadFromFile(filename) :
        with open(filename, 'r') as fp :
            data = json.load(fp)

        graph = WorldBuilder()
        graph.Load(data)

        return graph

    # -----------------------------------------------------------------
    def __init__(self) :
        WorldInfo.WorldInfo.__init__(self)

    # =================================================================
    # =================================================================

    # -----------------------------------------------------------------
    def AddPersonProfile(self, name) :
        """
        Args: 
            name -- string name of the person
        """
        profile = SocialNodes.PersonProfile(name)
        WorldInfo.WorldInfo.AddPersonProfile(self, profile)

        return profile

    # -----------------------------------------------------------------
    def AddPerson(self, name, profile) :
        """
        Args: 
            name -- string name of the person
            profile -- object of type SocialNodes.PersonProfile
            employer -- object of type SocialNodes.Business
            job -- object of type SocialDecoration.JobDescription
            residence -- 
        """
        person = SocialNodes.Person(name, profile)
        WorldInfo.WorldInfo.AddPerson(self, person)

        return person

    # =================================================================
    # =================================================================

    # -----------------------------------------------------------------
    def AddBusinessProfile(self, name, biztype, joblist) :
        """
        Args:
            name -- unique string name for the business profile
            biztype -- constant of type SocialDecoration.BusinessType
            joblist -- dictionary mapping type SocialDecoration.JobDescription --> Demand
            
        """
        bizprof = SocialNodes.BusinessProfile(name, biztype, joblist)
        WorldInfo.WorldInfo.AddBusinessProfile(self, bizprof)

        return bizprof

    # -----------------------------------------------------------------
    def AddBusiness(self, name, profile) :
        """
        Args:
            business -- string name of the business to create
            profile -- object of type SocialNodes.BusinessProfile
        """

        business = SocialNodes.Business(name, profile)
        WorldInfo.WorldInfo.AddBusiness(self, business)

        return business

    # =================================================================
    # =================================================================

    # -----------------------------------------------------------------
    def AddEndPoint(self, curx, cury, ntype, prefix) :
        name = GenNameFromCoordinates(curx, cury, prefix)
        node = LayoutNodes.EndPoint(name, ntype, curx, cury)
        WorldInfo.WorldInfo.AddEndPoint(self, node)

        return node

    # =================================================================
    # =================================================================

    # -----------------------------------------------------------------
    def AddBusinessLocationProfile(self, name, employees = 20, customers = 50, types = None) :
        node = LayoutNodes.BusinessLocationProfile(name, employees, customers, types)
        WorldInfo.WorldInfo.AddBusinessLocationProfile(self, node)

        return node

    # -----------------------------------------------------------------
    def AddBusinessLocation(self, profname, endpoints) :
        """
        Args:
            profname -- string name of the business location profile collection
            endpoints -- list of endpoint objects of type LayoutNodes.Endpoint
        """
        location = LayoutNodes.BusinessLocation(GenName('bizloc'), self.Nodes[profname])
        WorldInfo.WorldInfo.AddBusinessLocation(self, location)

        # business locations have one capsule containing all endpoints
        capsule = LayoutNodes.LocationCapsule(GenName('bizcap'))
        WorldInfo.WorldInfo.AddLocationCapsule(self, capsule)

        for endpoint in endpoints :
            capsule.AddEndPointToCapsule(endpoint)

        location.AddCapsuleToLocation(capsule)
        return location

    # =================================================================
    # =================================================================

    # -----------------------------------------------------------------
    def AddResidentialLocationProfile(self, name, residents = 5) :
        node = LayoutNodes.ResidentialLocationProfile(name, residents)
        WorldInfo.WorldInfo.AddResidentialLocationProfile(self, node)

        return node

    # -----------------------------------------------------------------
    def AddResidentialLocation(self, profname, endpoints) :
        """
        Args:
            profname -- string name of the business location profile collection
            endpoints -- list of endpoint objects of type LayoutNodes.Endpoint
        """
        location = LayoutNodes.ResidentialLocation(GenName('rezloc'), self.Nodes[profname])
        WorldInfo.WorldInfo.AddResidentialLocation(self, location)

        # residential locations have one endpoint per capsule
        for endpoint in endpoints :
            capsule = LayoutNodes.LocationCapsule(GenName('rezcap'))
            WorldInfo.WorldInfo.AddLocationCapsule(self, capsule)

            capsule.AddEndPointToCapsule(endpoint)
            location.AddCapsuleToLocation(capsule)

        return location

    # =================================================================
    # =================================================================

    # -----------------------------------------------------------------
    def AddIntersectionType(self, name, itype = 'priority', render = True) :
        node = LayoutNodes.IntersectionType(name, itype, render)
        WorldInfo.WorldInfo.AddIntersectionType(self, node)

        return node

    # -----------------------------------------------------------------
    def AddIntersection(self, curx, cury, itype, prefix) :
        name = GenNameFromCoordinates(curx, cury, prefix)
        node = LayoutNodes.Intersection(name, itype, curx, cury)
        WorldInfo.WorldInfo.AddIntersection(self, node)

        return node

    # =================================================================
    # =================================================================

    # -----------------------------------------------------------------
    def AddRoadType(self, name, lanes = 1, pri = 70, speed = 2.0, wid = 2.5, sig = '1L', render = True, center = False) :
        node = LayoutNodes.RoadType(name, lanes, pri, speed, wid, sig, render, center)
        WorldInfo.WorldInfo.AddRoadType(self, node)

        return node

    # -----------------------------------------------------------------
    def AddRoad(self, snode, enode, etype) :
        name = Graph.GenEdgeName(snode, enode)
        edge = LayoutEdges.Road(name, snode, enode, etype)
        WorldInfo.WorldInfo.AddRoad(self, edge)
        
        return edge

    # =================================================================
    # =================================================================

    # -----------------------------------------------------------------
    def SetIntersectionTypeByPattern(self, pattern, newtype) :
        for name, node in self.IterNodes(pattern, LayoutNodes.Intersection.__name__) :
            curtype = node.FindDecorationProvider(LayoutDecoration.IntersectionTypeDecoration.DecorationName)
            if curtype : curtype.DropMember(node)
                
            # and add it to the new collection
            newtype.AddMember(node)

        return True

    # -----------------------------------------------------------------
    def SetRoadTypeByPattern(self, pattern, newtype) :
        for name, edge in self.IterEdges(pattern = pattern, edgetype = LayoutEdges.Road.__name__) :
            curtype = edge.FindDecorationProvider(LayoutDecoration.RoadTypeDecoration.DecorationName)
            if curtype : curtype.DropMember(edge)
                
            # and add it to the new collection
            newtype.AddMember(edge)

        return True

    # =================================================================
    # =================================================================

    # -----------------------------------------------------------------
    def ConnectIntersections(self, node1, node2, etype) :
        self.AddRoad(node1, node2, etype)
        self.AddRoad(node2, node1, etype)

        return True

    # -----------------------------------------------------------------
    def AddIntersectionBetween(self, node1, node2, dist, ntype, prefix) :
        # assumes dist is positive and less than the distance between node1 and node2
        # assumes there is a direct link between node1 and node2

        edge1 = self.FindEdgeBetweenNodes(node1, node2)
        edge2 = self.FindEdgeBetweenNodes(node2, node1)
        if edge1 == None and edge2 == None:
            logger.warn("no edge found between %s and %s", node1.Name, node2.Name)

        curx = node1.X
        cury = node1.Y

        if node1.X == node2.X :
            cury = (node1.Y + dist) if node1.Y < node2.Y else (node1.Y - dist)
        elif node1.Y == node2.Y :
            curx = (node1.X + dist) if node1.X < node2.X else (node1.X - dist)
        else:
            logger.warn("expecting north/south or east/west nodes for split")
            return None

        nnode = self.AddIntersection(curx, cury, ntype, prefix)

        if edge1 :
            etype1 = edge1.FindDecorationProvider(LayoutDecoration.RoadTypeDecoration.DecorationName)
            self.DropEdge(edge1)
            self.AddRoad(node1,nnode,etype1)
            self.AddRoad(nnode,node2,etype1)

        if edge2 :
            etype2 = edge2.FindDecorationProvider(LayoutDecoration.RoadTypeDecoration.DecorationName)
            self.DropEdge(edge2)
            self.AddRoad(node2,nnode,etype2)
            self.AddRoad(nnode,node1,etype2)

        return nnode

    # =================================================================
    # =================================================================

    # -----------------------------------------------------------------
    def FindNodesInRange(self, x, y, dist) :
        result = []
        sqdist = int(dist) * int(dist)
        for name, node in self.IterNodes() :
            if not node.FindDecorationProvider('Coord') :
                continue

            cdist = (node.Coord.X - x)**2 + (node.Coord.Y - y)**2
            if cdist < sqdist :
                result.append(node)

        return result

    # -----------------------------------------------------------------
    def FindClosestNode(self, target) :
        cnode = None
        cdist = 0

        for name, node in self.IterNodes() :
            if not node.FindDecorationProvider('Coord') :
                continue

            if cnode == None :
                cnode = node
                cdist = (cnode.X - target.X)**2 + (cnode.Y - target.Y)**2
                continue

            dist = (node.X - target.X)**2 + (node.Y - target.Y)**2
            if (dist < cdist) :
                cnode = node
                cdist = dist
            
        return cnode

    # =================================================================
    # =================================================================

    # -----------------------------------------------------------------
    def GenerateGrid(self, x0, y0, x1, y1, stepx, stepy, ntype, etype, prefix = 'node') :
        lastlist = []

        curx = int(x0)
        while curx <= x1 :
            thislist = []

            cury = int(y0)
            while cury <= y1 :
                node = self.AddIntersection(curx, cury, ntype, prefix)
            
                if curx > x0 :
                    wnode = lastlist.pop(0)
                    self.ConnectIntersections(node, wnode, etype)

                if cury > y0 :
                    snode = thislist[len(thislist) - 1]
                    self.ConnectIntersections(node, snode, etype)

                thislist.append(node)
                cury += int(stepy)

            lastlist = thislist
            curx += int(stepx)

    # =================================================================
    # =================================================================

    # -----------------------------------------------------------------
    def GenerateResidential(self, node1, node2, rgen, prefix = 'res') :
        self.DropEdgeByName("%s=O=%s" % (node1.Name, node2.Name))
        self.DropEdgeByName("%s=O=%s" % (node2.Name, node1.Name))
        rgenp = copy.copy(rgen)

        if node1.X == node2.X :
            if node1.Y < node2.Y :
                return self._GenerateResidentialYAxis(node1,node2,rgen,prefix)
            else :
                # reverse direction, reverse sense of left and right
                rgenp.DrivewayLength = -rgenp.DrivewayLength
                return self._GenerateResidentialYAxis(node2,node1,rgen,prefix)
        else :
            if node1.X < node2.X :
                return self._GenerateResidentialXAxis(node1,node2,rgen,prefix)
            else :
                # reverse direction, reverse sense of left and right
                rgenp.DrivewayLength = -rgenp.DrivewayLength
                return self._GenerateResidentialXAxis(node2,node1,rgen,prefix)

    # -----------------------------------------------------------------
    def _GenerateResidentialYAxis(self, node1, node2, rgen, prefix) :
        lastnode = node1

        resnodes = []
        cury = node1.Y + rgen.DrivewayBuffer
        while cury + rgen.DrivewayBuffer <= node2.Y :
            # first node is the intersection with the existing road
            node = self.AddIntersection(node1.X, cury, rgen.IntersectionType, prefix)
            self.ConnectIntersections(node,lastnode,rgen.RoadType)
            
            # this is the first residential endpoint
            enode = self.AddEndPoint(node1.X + rgen.DrivewayLength, cury, rgen.ResidentialType, prefix)
            self.ConnectIntersections(node,enode,rgen.DrivewayType)
            resnodes.append(enode)

            # this is the optional second residential endpoint
            if rgen.BothSides :
                wnode = self.AddEndPoint(node1.X - rgen.DrivewayLength, cury, rgen.ResidentialType, prefix)
                self.ConnectIntersections(node,wnode,rgen.DrivewayType)
                resnodes.append(wnode)

            lastnode = node
            cury += rgen.Spacing

        self.ConnectIntersections(lastnode,node2,rgen.RoadType)
        return resnodes

    # -----------------------------------------------------------------
    def _GenerateResidentialXAxis(self, node1, node2, rgen, prefix) :
        lastnode = node1

        resnodes = []
        curx = node1.X + rgen.DrivewayBuffer
        while curx + rgen.DrivewayBuffer <= node2.X :
            # first node is the intersection with the existing road
            node = self.AddIntersection(curx, node1.Y, rgen.IntersectionType, prefix)
            self.ConnectIntersections(node,lastnode,rgen.RoadType)

            # this is the first residential endpoint
            nnode = self.AddEndPoint(curx, node1.Y + rgen.DrivewayLength, rgen.ResidentialType, prefix)
            self.ConnectIntersections(node,nnode,rgen.DrivewayType)
            resnodes.append(nnode)

            # this is the optional second residential endpoint
            if rgen.BothSides :
                snode = self.AddEndPoint(curx, node1.Y - rgen.DrivewayLength, rgen.ResidentialType, prefix)
                self.ConnectIntersections(node,snode,rgen.DrivewayType)
                resnodes.append(snode)

            lastnode = node
            curx += rgen.Spacing

        self.ConnectIntersections(lastnode,node2,rgen.RoadType)
        return resnodes

    # =================================================================
    # =================================================================

    # -----------------------------------------------------------------
    def BuildSimpleParkingLotNS(self, origin, itype, rgen, prefix = 'tile', slength = 30, elength = 70, offset = 25) :
        dist1 = slength
        dist2 = elength - slength

        # find the first split point
        edge = origin.NorthEdge()
        while (edge.EndNode.Y - edge.StartNode.Y <= dist1) :
            dist1 = dist1 - (edge.EndNode.Y - edge.StartNode.Y)
            edge = edge.EndNode.NorthEdge()

        # if the node already exists, don't overwrite the existing type
        cnode1 = edge.StartNode
        if dist1 > 0 :
            cnode1 = self.AddIntersectionBetween(edge.StartNode, edge.EndNode, dist1, itype, prefix)
        
        # find the second split point
        edge = cnode1.NorthEdge()
        while (edge.EndNode.Y - edge.StartNode.Y <= dist2) :
            dist2 = dist2 - (edge.EndNode.Y - edge.StartNode.Y)
            edge = edge.EndNode.NorthEdge()

        cnode2 = edge.StartNode
        if dist2 > 0 :
            cnode2 = self.AddIntersectionBetween(edge.StartNode, edge.EndNode, dist2, itype, prefix)

        # cnode1 and cnode2 are the connection nodes, now build a path between them
        dnode1 = self.AddIntersection(cnode1.X + offset, cnode1.Y, rgen.IntersectionType, prefix)
        dnode2 = self.AddIntersection(cnode2.X + offset, cnode2.Y, rgen.IntersectionType, prefix)

        self.ConnectIntersections(cnode1, dnode1, rgen.RoadType)
        self.ConnectIntersections(cnode2, dnode2, rgen.RoadType)
        return self._GenerateResidentialYAxis(dnode1, dnode2, rgen, prefix)

    # -----------------------------------------------------------------
    def BuildSimpleParkingLotSN(self, origin, itype, rgen, prefix = 'tile', slength = 30, elength = 70, offset = 25) :
        dist1 = slength
        dist2 = elength - slength

        # find the first split point
        edge = origin.SouthEdge()
        while (edge.StartNode.Y - edge.EndNode.Y <= dist1) :
            dist1 = dist1 - (edge.StartNode.Y - edge.EndNode.Y)
            edge = edge.StartNode.SouthEdge()

        # if the node already exists, don't overwrite the existing type
        cnode1 = edge.EndNode
        if dist1 > 0 :
            cnode1 = self.AddIntersectionBetween(edge.StartNode, edge.EndNode, dist1, itype, prefix)
        
        # find the second split point
        edge = cnode1.SouthEdge()
        while (edge.StartNode.Y - edge.EndNode.Y <= dist2) :
            dist2 = dist2 - (edge.StartNode.Y - edge.EndNode.Y)
            edge = edge.StartNode.SouthEdge()

        cnode2 = edge.EndNode
        if dist2 > 0 :
            cnode2 = self.AddIntersectionBetween(edge.StartNode, edge.EndNode, dist2, itype, prefix)

        # cnode1 and cnode2 are the connection nodes, now build a path between them
        dnode1 = self.AddIntersection(cnode1.X + offset, cnode1.Y, rgen.IntersectionType, prefix)
        dnode2 = self.AddIntersection(cnode2.X + offset, cnode2.Y, rgen.IntersectionType, prefix)

        self.ConnectIntersections(cnode1, dnode1, rgen.RoadType)
        self.ConnectIntersections(cnode2, dnode2, rgen.RoadType)
        return self._GenerateResidentialYAxis(dnode2, dnode1, rgen, prefix)

    # -----------------------------------------------------------------
    def BuildSimpleParkingLotEW(self, origin, itype, rgen, prefix = 'tile', slength = 30, elength = 70, offset = 25) :
        dist1 = slength
        dist2 = elength - slength

        # find the first split point
        edge = origin.EastEdge()
        while (edge.EndNode.X - edge.StartNode.X <= dist1) :
            dist1 = dist1 - (edge.EndNode.X - edge.StartNode.X)
            edge = edge.EndNode.EastEdge()

        # if the node already exists, don't overwrite the existing type
        cnode1 = edge.StartNode
        if dist1 > 0 :
            cnode1 = self.AddIntersectionBetween(edge.StartNode, edge.EndNode, dist1, itype, prefix)
        
        # find the second split point
        edge = cnode1.EastEdge()
        while (edge.EndNode.X - edge.StartNode.X <= dist2) :
            dist2 = dist2 - (edge.EndNode.X - edge.StartNode.X)
            edge = edge.EndNode.EastEdge()

        cnode2 = edge.StartNode
        if dist2 > 0 :
            cnode2 = self.AddIntersectionBetween(edge.StartNode, edge.EndNode, dist2, itype, prefix)

        # cnode1 and cnode2 are the connection nodes, now build a path between them
        dnode1 = self.AddIntersection(cnode1.X, cnode1.Y + offset, rgen.IntersectionType, prefix)
        dnode2 = self.AddIntersection(cnode2.X, cnode2.Y + offset, rgen.IntersectionType, prefix)

        self.ConnectIntersections(cnode1, dnode1, rgen.RoadType)
        self.ConnectIntersections(cnode2, dnode2, rgen.RoadType)
        return self._GenerateResidentialXAxis(dnode1, dnode2, rgen, prefix)
