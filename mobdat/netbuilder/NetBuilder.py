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

@file    NetBuilder.py
@author  Mic Bowman
@date    2013-12-03

This file defines routines used to build features of a mobdat traffic
network such as building a grid of roads. 

"""

import os, sys, warnings, copy

# we need to import python modules from the $SUMO_HOME/tools directory
sys.path.append(os.path.join(os.environ.get("OPENSIM","/share/opensim"),"lib","python"))
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "lib")))

import re

## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class NodeType :

    # -----------------------------------------------------------------
    def __init__(self, name, ntype = 'priority', render = True) :
        self.Name = name
        self.NType = ntype
        self.Render = render

## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class Node :
    WEST  = 0
    NORTH = 1
    EAST  = 2
    SOUTH = 3

    # -----------------------------------------------------------------
    def __init__(self, x, y, ntype, prefix) :
        self.X = int(x)
        self.Y = int(y)

        self.Name = self._GenerateNodeName(prefix)
        self.NodeType = ntype

        self.OEdges = []
        self.IEdges = []

    # -----------------------------------------------------------------
    def _GenerateNodeName(self, prefix) :
        ewdir = 'E'
        x = self.X
        if x < 0 :
            ewdir = 'W'
            x = abs(self.X)

        nsdir = 'N'
        y = self.Y
        if y < 0 :
            nsdir = 'S'
            y = abs(y)

        return "%s%d%s%d%s" % (prefix, int(x), ewdir, int(y), nsdir)

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
    def __str__(self) :
        out = "%s, %s, %d, %d" % (self.Name, self.NodeType.Name, self.X, self.Y)
        for e in self.OEdges :
            out += ", "
            out += str(e.EdgeType.Lanes)

        return out

    # -----------------------------------------------------------------
    def AddIEdge(self, edge) :
        self.IEdges.append(edge)

    # -----------------------------------------------------------------
    def AddOEdge(self, edge) :
        self.OEdges.append(edge)

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
        for e in self.OEdges :
            position = self._EdgeMapPosition(e.EndNode)
            edgemap[position] = e

        return edgemap

    # -----------------------------------------------------------------
    def InputEdgeMap(self) :
        edgemap = [None, None, None, None]
        for e in self.IEdges :
            position = self._EdgeMapPosition(e.StartNode)
            edgemap[position] = e

        return edgemap

    # -----------------------------------------------------------------
    # signature returned is west, north, east, south
    # -----------------------------------------------------------------
    def Signature(self) :
        osignature = []
        for e in self.OutputEdgeMap() :
            sig = e.EdgeType.Signature if e else '0L'
            osignature.append(sig)

        isignature = []
        for e in self.InputEdgeMap() :
            sig = e.EdgeType.Signature if e else '0L'
            isignature.append(sig)

        signature = []
        for i in range(0,4) :
            signature.append("{0}/{1}".format(osignature[i], isignature[i]))

        return signature

## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class EdgeType :

    # -----------------------------------------------------------------
    def __init__(self, name, lanes = 1, pri = 70, speed = 2.0, wid = 2.5, sig = '1L', render = True) :
        self.Name = name
        self.Lanes = lanes
        self.Priority = pri
        self.Speed = speed
        self.Width = wid
        self.Signature = sig
        self.Render = render

## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class Edge :
    
    # -----------------------------------------------------------------
    def __init__(self, snode, enode, etype) :
        self.Name = "%s=O=%s" % (snode.Name, enode.Name)
        self.EdgeType = etype
        self.StartNode = snode
        self.EndNode = enode

        snode.AddOEdge(self)
        enode.AddIEdge(self)

    # -----------------------------------------------------------------
    def ReverseName(self) :
        return "%s=O=%s" % (self.EndNode.Name, self.StartNode.Name)

## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class ResidentialGenerator :

    # -----------------------------------------------------------------
    def __init__(self, etype, itype, dtype, rtype, driveway = 10, bspace = 20, spacing = 20, both = True) :
        self.EdgeType = etype
        self.IntersectionType = itype
        self.DrivewayType = dtype
        self.ResidentialType = rtype
        self.DrivewayLength = driveway
        self.DrivewayBuffer = bspace
        self.Spacing = spacing
        self.BothSides = both

## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class Network :

    # -----------------------------------------------------------------
    def __init__(self) :
        self.gEdgeTypes = {}
        self.gNodeTypes = {}
        self.gNodes = {}
        self.gEdges = {}
        self.InjectPrefix = "IN"

    # -----------------------------------------------------------------
    def AddEdgeType(self, name, lanes = 1, pri = 70, speed = 2.0, wid = 2.5, sig = '1L', render = True) :
        if name not in self.gEdgeTypes :
            self.gEdgeTypes[name] = EdgeType(name, lanes, pri, speed, wid, sig, render)
            
        return self.gEdgeTypes[name]

    # -----------------------------------------------------------------
    def AddNodeType(self, name, ntype = 'priority', render = True) :
        if name not in self.gNodeTypes :
            self.gNodeTypes[name] = NodeType(name,ntype,render)

        return self.gNodeTypes[name]

    # -----------------------------------------------------------------
    def AddNode(self, curx, cury, ntype, prefix) :
        node = Node(curx, cury, ntype, prefix)
        if node.Name in self.gNodes :
            print 'duplicate node %s' % (node.Name)
            return self.gNodes[node.Name]

        self.gNodes[node.Name] = node
        return node

    # -----------------------------------------------------------------
    def AddEdge(self, snode, enode, etype) :
        edge = Edge(snode, enode, etype)
        self.gEdges[edge.Name] = edge
        
        return edge

    # -----------------------------------------------------------------
    def FindEdgeBetweenNodes(self, node1, node2) :
        for e in node1.OEdges :
            if e.EndNode == node2 :
                return e
        return None

    # -----------------------------------------------------------------
    def ConnectNodes(self, node1, node2, etype) :
        self.AddEdge(node1, node2, etype)
        self.AddEdge(node2, node1, etype)

        return True

    # -----------------------------------------------------------------
    def AddNodeBetween(self, node1, node2, dist, ntype, prefix) :
        # assumes dist is positive and less than the distance between node1 and node2
        # assumes there is a direct link between node1 and node2

        edge1 = self.FindEdgeBetweenNodes(node1, node2)
        edge2 = self.FindEdgeBetweenNodes(node2, node1)
        if edge1 == None and edge2 == None:
            warnings.warn("no edge found between %s and %s" % (node1.Name, node2.Name))

        curx = node1.X
        cury = node1.Y

        if node1.X == node2.X :
            cury = (node1.Y + dist) if node1.Y < node2.Y else (node1.Y - dist)
        elif node1.Y == node2.Y :
            curx = (node1.X + dist) if node1.X < node2.X else (node1.X - dist)
        else:
            warnings.warn("expecting north/south or east/west nodes for split")
            return None

        nnode = self.AddNode(curx, cury, ntype, prefix)

        if edge1 :
            etype1 = edge1.EdgeType
            self.DropEdgeByName(edge1.Name)
            self.AddEdge(node1,nnode,etype1)
            self.AddEdge(nnode,node2,etype1)

        if edge2 :
            etype2 = edge2.EdgeType
            self.DropEdgeByName(edge2.Name)
            self.AddEdge(node2,nnode,etype2)
            self.AddEdge(nnode,node1,etype2)

        return nnode

    # -----------------------------------------------------------------
    def DropNodeByName(self, name) :
        if name not in self.gNodes :
            print 'unable to drop unknown node %s' % (name)
            return False

        node = self.gNodes[name]

        for e in node.OEdges :
            n = e.EndNode
            n.IEdges.remove(e)
            if e.Name in self.gEdges :
                del self.gEdges[e.Name]

        for e in node.IEdges :
            n = e.StartNode
            n.OEdges.remove(e)
            if e.Name in self.gEdges :
                del self.gEdges[e.Name]

        del self.gNodes[node.Name]
        return True

    # -----------------------------------------------------------------
    def DropNodeByPattern(self, pattern) :
        names = self.gNodes.keys()
        for name in names :
            if re.match(pattern, name) :
                self.DropNodeByName(name)

        return True

    # -----------------------------------------------------------------
    def SetNodeTypeByPattern(self, pattern, ntype) :
        names = self.gNodes.keys()
        for name in names :
            if re.match(pattern, name) :
                self.gNodes[name].NodeType = ntype

        return True

    # -----------------------------------------------------------------
    def DropEdgeByName(self, name) :
        if name not in self.gEdges :
            print 'unable to drop unknown edge %s' % (name)
            return False

        edge = self.gEdges[name]
        edge.StartNode.OEdges.remove(edge)
        edge.EndNode.IEdges.remove(edge)

        del self.gEdges[name]
        return True

    # -----------------------------------------------------------------
    def DropEdgeByPattern(self, pattern) :
        names = self.gEdges.keys()
        for name in names :
            if re.match(pattern, name) :
                self.DropEdgeByName(name)
        
        return True

    # -----------------------------------------------------------------
    def SetEdgeTypeByPattern(self, pattern, etype) :
        names = self.gEdges.keys()
        for name in names :
            if re.match(pattern, name) :
                self.gEdges[name].EdgeType = etype

    # -----------------------------------------------------------------
    def GenerateGrid(self, x0, y0, x1, y1, stepx, stepy, ntype, etype, prefix = 'node') :
        lastlist = []

        curx = int(x0)
        while curx <= x1 :
            thislist = []

            cury = int(y0)
            while cury <= y1 :
                node = self.AddNode(curx, cury, ntype, prefix)
            
                if curx > x0 :
                    wnode = lastlist.pop(0)
                    self.ConnectNodes(node, wnode, etype)

                if cury > y0 :
                    snode = thislist[len(thislist) - 1]
                    self.ConnectNodes(node, snode, etype)

                thislist.append(node)
                cury += int(stepy)

            lastlist = thislist
            curx += int(stepx)

    # -----------------------------------------------------------------
    def GenerateResidential(self, node1, node2, rgen, prefix = 'res') :
        self.DropEdgeByName("%s=O=%s" % (node1.Name, node2.Name))
        self.DropEdgeByName("%s=O=%s" % (node2.Name, node1.Name))
        rgenp = copy.copy(rgen)

        if node1.X == node2.X :
            if node1.Y < node2.Y :
                self._GenerateResidentialYAxis(node1,node2,rgen,prefix)
            else :
                # reverse direction, reverse sense of left and right
                rgenp.DrivewayLength = -rgenp.DrivewayLength
                self._GenerateResidentialYAxis(node2,node1,rgen,prefix)
        else :
            if node1.X < node2.X :
                self._GenerateResidentialXAxis(node1,node2,rgen,prefix)
            else :
                # reverse direction, reverse sense of left and right
                rgenp.DrivewayLength = -rgenp.DrivewayLength
                self._GenerateResidentialXAxis(node2,node1,rgen,prefix)

    # -----------------------------------------------------------------
    def _GenerateResidentialYAxis(self, node1, node2, rgen, prefix) :
        lastnode = node1

        cury = node1.Y + rgen.DrivewayBuffer
        while cury + rgen.DrivewayBuffer <= node2.Y :
            node = self.AddNode(node1.X, cury, rgen.IntersectionType, prefix)
            self.ConnectNodes(node,lastnode,rgen.EdgeType)

            enode = self.AddNode(node1.X + rgen.DrivewayLength, cury, rgen.ResidentialType, self.InjectPrefix + prefix)
            self.ConnectNodes(node,enode,rgen.DrivewayType)

            if rgen.BothSides :
                wnode = self.AddNode(node1.X - rgen.DrivewayLength, cury, rgen.ResidentialType, self.InjectPrefix + prefix)
                self.ConnectNodes(node,wnode,rgen.DrivewayType)

            lastnode = node
            cury += rgen.Spacing

        self.ConnectNodes(lastnode,node2,rgen.EdgeType)

    # -----------------------------------------------------------------
    def _GenerateResidentialXAxis(self, node1, node2, rgen, prefix) :
        lastnode = node1

        curx = node1.X + rgen.DrivewayBuffer
        while curx + rgen.DrivewayBuffer <= node2.X :
            node = self.AddNode(curx, node1.Y, rgen.IntersectionType, prefix)
            self.ConnectNodes(node,lastnode,rgen.EdgeType)

            nnode = self.AddNode(curx, node1.Y + rgen.DrivewayLength, rgen.ResidentialType, self.InjectPrefix + prefix)
            self.ConnectNodes(node,nnode,rgen.DrivewayType)

            if rgen.BothSides :
                snode = self.AddNode(curx, node1.Y - rgen.DrivewayLength, rgen.ResidentialType, self.InjectPrefix + prefix)
                self.ConnectNodes(node,snode,rgen.DrivewayType)

            lastnode = node
            curx += rgen.Spacing

        self.ConnectNodes(lastnode,node2,rgen.EdgeType)

    # -----------------------------------------------------------------
    def _FindNodeClosestToLocation(self, node) :
        cnode = None
        cdist = 0

        for n in self.gNodes.itervalues() :
            if cnode== None :
                cnode = n
                cdist = (cnode.X - node.X)**2 + (cnode.Y - node.Y)**2
                continue
            dist = (n.X - node.X)**2 + (n.Y - node.Y)**2
            if (dist < cdist) :
                cnode = n
                cdist = dist

        return cnode

    # -----------------------------------------------------------------
    def _FindNodeNearLocation(self, node, margin = 1.0) :
        for n in self.gNodes.itervalues() :
            if abs(n.X - node.X) < margin and abs(n.Y - node.Y) < margin :
                return n

        return None

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
            cnode1 = self.AddNodeBetween(edge.StartNode, edge.EndNode, dist1, itype, prefix)
        
        # find the second split point
        edge = cnode1.NorthEdge()
        while (edge.EndNode.Y - edge.StartNode.Y <= dist2) :
            dist2 = dist2 - (edge.EndNode.Y - edge.StartNode.Y)
            edge = edge.EndNode.NorthEdge()

        cnode2 = edge.StartNode
        if dist2 > 0 :
            cnode2 = self.AddNodeBetween(edge.StartNode, edge.EndNode, dist2, itype, prefix)

        # cnode1 and cnode2 are the connection nodes, now build a path between them
        dnode1 = self.AddNode(cnode1.X + offset, cnode1.Y, rgen.IntersectionType, prefix)
        dnode2 = self.AddNode(cnode2.X + offset, cnode2.Y, rgen.IntersectionType, prefix)

        self.ConnectNodes(cnode1, dnode1, rgen.EdgeType)
        self.ConnectNodes(cnode2, dnode2, rgen.EdgeType)
        self._GenerateResidentialYAxis(dnode1, dnode2, rgen, prefix)

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
            cnode1 = self.AddNodeBetween(edge.StartNode, edge.EndNode, dist1, itype, prefix)
        
        # find the second split point
        edge = cnode1.SouthEdge()
        while (edge.StartNode.Y - edge.EndNode.Y <= dist2) :
            dist2 = dist2 - (edge.StartNode.Y - edge.EndNode.Y)
            edge = edge.StartNode.SouthEdge()

        cnode2 = edge.EndNode
        if dist2 > 0 :
            cnode2 = self.AddNodeBetween(edge.StartNode, edge.EndNode, dist2, itype, prefix)

        # cnode1 and cnode2 are the connection nodes, now build a path between them
        dnode1 = self.AddNode(cnode1.X + offset, cnode1.Y, rgen.IntersectionType, prefix)
        dnode2 = self.AddNode(cnode2.X + offset, cnode2.Y, rgen.IntersectionType, prefix)

        self.ConnectNodes(cnode1, dnode1, rgen.EdgeType)
        self.ConnectNodes(cnode2, dnode2, rgen.EdgeType)
        self._GenerateResidentialYAxis(dnode2, dnode1, rgen, prefix)

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
            cnode1 = self.AddNodeBetween(edge.StartNode, edge.EndNode, dist1, itype, prefix)
        
        # find the second split point
        edge = cnode1.EastEdge()
        while (edge.EndNode.X - edge.StartNode.X <= dist2) :
            dist2 = dist2 - (edge.EndNode.X - edge.StartNode.X)
            edge = edge.EndNode.EastEdge()

        cnode2 = edge.StartNode
        if dist2 > 0 :
            cnode2 = self.AddNodeBetween(edge.StartNode, edge.EndNode, dist2, itype, prefix)

        # cnode1 and cnode2 are the connection nodes, now build a path between them
        dnode1 = self.AddNode(cnode1.X, cnode1.Y + offset, rgen.IntersectionType, prefix)
        dnode2 = self.AddNode(cnode2.X, cnode2.Y + offset, rgen.IntersectionType, prefix)

        self.ConnectNodes(cnode1, dnode1, rgen.EdgeType)
        self.ConnectNodes(cnode2, dnode2, rgen.EdgeType)
        self._GenerateResidentialXAxis(dnode1, dnode2, rgen, prefix)
