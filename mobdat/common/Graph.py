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

@file    Graph.py
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

from Decoration import *
from Utilities import GenName

import uuid, re
import json

logger = logging.getLogger(__name__)

## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class _GraphObject :

    # -----------------------------------------------------------------
    def __init__(self, name) :
        self.Name = name
        self.Decorations = {}
        self.Collections = {}

    # -----------------------------------------------------------------
    def __getattr__(self, attr) :
        provider = self.FindDecorationProvider(attr)
        if provider :
            return provider.Decorations[attr]

        raise AttributeError("%r object has no attribute %r" % (self.__class__, attr))

    # -----------------------------------------------------------------
    def AddToCollection(self, collection) :
        self.Collections[collection.Name] = collection

    # -----------------------------------------------------------------
    def DropFromCollection(self, collection) :
        del self.Collections[collection.Name]

    # -----------------------------------------------------------------
    def AddDecoration(self, decoration) :
        self.Decorations[decoration.DecorationName] = decoration

    # -----------------------------------------------------------------
    def FindDecorationProvider(self, attr) :
        if attr in self.Decorations :
            return self

        # inherit the decorations of all the collections the object is in
        for coll in self.Collections.itervalues() :
            if attr in coll.Decorations :
                return coll

        return None

    # -----------------------------------------------------------------
    def LoadDecorations(self, graph, einfo) :
        for dinfo in einfo['Decorations'] :
            # if a handler for the decoration doesn't exist, we just skip loading
            decoration = graph.LoadDecoration(dinfo)
            if decoration :
                self.AddDecoration(decoration)

    # -----------------------------------------------------------------
    def Dump(self) :
        result = dict()

        result['Name'] = self.Name
        result['Decorations'] = []
        for decoration in self.Decorations.itervalues() :
            result['Decorations'].append(decoration.Dump())

        return result

## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class Node(_GraphObject) :

    # -----------------------------------------------------------------
    @staticmethod
    def Load(graph, ninfo) :
        node = Node(ninfo['Name'])
        node.LoadDecorations(graph, ninfo)
            
        return node

    # -----------------------------------------------------------------
    def __init__(self, name = None, prefix = 'node') :
        if not name : name = GenName(prefix)
        _GraphObject.__init__(self, name)

        self.OutputEdges = []
        self.InputEdges = []

    # -----------------------------------------------------------------
    def AddInputEdge(self, edge) :
        self.InputEdges.append(edge)

    # -----------------------------------------------------------------
    def AddOutputEdge(self, edge) :
        self.OutputEdges.append(edge)

    # -----------------------------------------------------------------
    def Dump(self) :
        result = _GraphObject.Dump(self)
        return result

## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class Edge(_GraphObject) :
    # -----------------------------------------------------------------
    @staticmethod
    def GenEdgeName(snode, enode) :
        return "%s=O=%s" % (snode.Name, enode.Name)

    # -----------------------------------------------------------------
    @staticmethod
    def Load(graph, einfo) :
        snode = graph.Nodes[einfo['StartNode']]
        enode = graph.Nodes[einfo['EndNode']]
        edge = Edge(snode, enode, einfo['Name'])

        edge.LoadDecorations(graph, einfo)

        return edge

    # -----------------------------------------------------------------
    def __init__(self, snode, enode, name = None) :
        if not name : name = self.GenEdgeName(snode, enode)
        _GraphObject.__init__(self, name)

        self.StartNode = snode
        self.EndNode = enode

        snode.AddOutputEdge(self)
        enode.AddInputEdge(self)

    # -----------------------------------------------------------------
    def Dump(self) : 
        result = _GraphObject.Dump(self)

        result['StartNode'] = self.StartNode.Name
        result['EndNode'] = self.EndNode.Name

        return result

## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class Collection(_GraphObject) :

    # -----------------------------------------------------------------
    @staticmethod
    def Load(graph, cinfo) :
        collection = Collection(name = cinfo['Name'])

        for member in cinfo['Members'] :
            collection.AddMember(graph.Edges[member] if member in graph.Edges else graph.Nodes[member])

        collection.LoadDecorations(graph, cinfo)

        return collection

    # -----------------------------------------------------------------
    def __init__(self, members = [], name = None, prefix = 'col') :
        if not name : name = GenName(prefix)
        _GraphObject.__init__(self, name)

        self.Members = []
        for member in members :
            self.AddMember(member)

    # -----------------------------------------------------------------
    def AddMember(self, member) :
        # add to the object the reference to the group
        member.AddToCollection(self)

        # add to the group the reference to the object
        self.Members.append(member)

    # -----------------------------------------------------------------
    def DropMember(self, member) :
        # drop the reference to the collection from the object
        member.DropFromCollection(self)
        
        # drop the object
        self.Members.remove(member)

    # -----------------------------------------------------------------
    def Dump(self) :
        result = _GraphObject.Dump(self)

        result['Members'] = []
        for member in self.Members :
            result['Members'].append(member.Name)

        return result

## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class Graph :

    # -----------------------------------------------------------------
    @staticmethod
    def LoadFromFile(filename) :
        with open(filename, 'r') as fp :
            netdata = json.load(fp)

        graph = Graph()
        graph.Load(netdata)

        return graph

    # -----------------------------------------------------------------
    @staticmethod
    def GenGroupDecorationKey(dname, iname) :
        return "%s=O=%s" % (dname, iname)

    # -----------------------------------------------------------------
    def __init__(self) :
        self.DecorationMap = {}

        self.Collections = {}
        self.Edges = {}
        self.Nodes = {}

        for dtype in CommonDecorations :
            self.AddDecorationHandler(dtype)

    # -----------------------------------------------------------------
    def Dump(self) :
        result = dict()

        collections = []
        for collection in self.Collections.itervalues() :
            collections.append(collection.Dump())
        result['Collections'] = collections

        edges = []
        for edge in self.Edges.itervalues() :
            edges.append(edge.Dump())
        result['Edges'] = edges

        nodes = []
        for node in self.Nodes.itervalues() :
            nodes.append(node.Dump())
        result['Nodes'] = nodes

        return result
    
    # -----------------------------------------------------------------
    def Load(self, info) :
        for ninfo in info['Nodes'] :
            node = Node.Load(self, ninfo)
            self.Nodes[node.Name] = node
            
        for einfo in info['Edges'] :
            edge = Edge.Load(self, einfo)
            self.Edges[edge.Name] = edge

        for cinfo in info['Collections'] :
            collection = Collection.Load(self, cinfo)
            self.Collections[collection.Name] = collection

    # -----------------------------------------------------------------
    def AddNode(self, node) :
        self.Nodes[node.Name] = node

    # -----------------------------------------------------------------
    def DropNode(self, node) :
        # need to use values because dropping the member in the collection
        # will change the list of connections here
        for collection in node.Collections.values() :
            collection.DropMember(node)

        for edge in node.InputEdges[:] :
            self.DropEdge(edge)

        for edge in node.OutputEdges[:] :
            self.DropEdge(edge)

        del self.Nodes[node.Name]

    # -----------------------------------------------------------------
    def DropNodeByName(self, name) :
        if name not in self.Nodes :
            logger.info('unable to drop unknown node %s', name)
            return False

        self.DropNode(self.Nodes[name])
        return True

    # -----------------------------------------------------------------
    def DropNodesByPattern(self, pattern) :
        for name, node in self.Nodes.items() :
            if re.match(pattern, name) :
                self.DropNode(node)

        return True

    # -----------------------------------------------------------------
    def AddEdge(self, edge) :
        self.Edges[edge.Name] = edge
        return True

    # -----------------------------------------------------------------
    def DropEdge(self, edge) :
        # need to use values because dropping the member in the collection
        # will change the list of connections here
        for collection in edge.Collections.values() :
            collection.DropMember(edge)

        edge.StartNode.OutputEdges.remove(edge)
        edge.EndNode.InputEdges.remove(edge)

        del self.Edges[edge.Name]
        return True

    # -----------------------------------------------------------------
    def DropEdgeByName(self, name) :
        if name not in self.Edges :
            return True

        return self.DropEdge(self.Edges[name])

    # -----------------------------------------------------------------
    def DropEdgesByPattern(self, pattern) :
        # need to use items because dropping the member in the collection
        # will change the list of connections here
        for name, edge in self.Edges.items() :
            if re.match(pattern, name) :
                self.DropEdge(edge)
        
        return True

    # -----------------------------------------------------------------
    def FindEdgeBetweenNodes(self, node1, node2) :
        for e in node1.OutputEdges :
            if e.EndNode == node2 :
                return e
        return None

    # -----------------------------------------------------------------
    def AddCollection(self, collection) :
        self.Collections[collection.Name] = collection

    # -----------------------------------------------------------------
    def DropCollection(self, collection) :
        for obj in collection.Members[:] :
            obj.DropFromCollection(collection)

        del self.Collections[collection.Name]

    # -----------------------------------------------------------------
    def AddDecorationHandler(self, handler) :
        self.DecorationMap[handler.DecorationName] = handler

    # -----------------------------------------------------------------
    def LoadDecoration(self, dinfo) :
        handler = self.DecorationMap[dinfo['__TYPE__']]
        if handler :
            return handler.Load(self, dinfo)

        # if we don't have a handler, thats ok we just dont load the 
        # decoration, note the missing decoration in the logs however
        logger.info('no decoration handler found for type %s', dinfo['__TYPE__'])
        return None

## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
if __name__ == '__main__' :

    # -----------------------------------------------------------------
    class TestDecoration(Decoration) :
        DecorationName = 'TestDecoration'

        # -----------------------------------------------------------------
        @staticmethod
        def Load(graph, info) :
            return TestDecoration(info['Value1'], info['Value2'])

        # -----------------------------------------------------------------
        def __init__(self, val1, val2) :
            Decoration.__init__(self)

            self.Value1 = val1
            self.Value2 = val2

        # -----------------------------------------------------------------
        def Dump(self) : 
            result = Decoration.Dump(self)

            result['Value1'] = self.Value1
            result['Value2'] = self.Value2

            return result

    # -----------------------------------------------------------------
    class EdgeTypeDecoration(Decoration) :
        DecorationName = 'EdgeType'

        # -----------------------------------------------------------------
        @staticmethod
        def Load(graph, info) :
            return EdgeTypeDecoration(info['Name'], info['Weight'])

        # -----------------------------------------------------------------
        def __init__(self, name, weight) :
            Decoration.__init__(self)

            self.Name = name
            self.Weight = weight

        # -----------------------------------------------------------------
        def Dump(self) : 
            result = Decoration.Dump(self)

            result['Name'] = self.Name
            result['Weight'] = self.Weight

            return result


    net1 = Graph()
    net1.AddDecorationHandler(CoordDecoration)
    net1.AddDecorationHandler(TestDecoration)
    net1.AddDecorationHandler(EdgeTypeDecoration)

    edges1 = Collection(name = 'type1edges')
    edges1.AddDecoration(EdgeTypeDecoration('type1', 25))
    net1.AddCollection(edges1)

    edges2 = Collection(name = 'type2edges')
    edges2.AddDecoration(EdgeTypeDecoration('type2', 5))
    net1.AddCollection(edges2)

    for x in range(0, 5) :
        for y in range(0, 5) :
            node = Node(CoordDecoration.GenName(x, y))
            node.AddDecoration(CoordDecoration(x, y))
            net1.AddNode(node)
            if x > 0 :
                if y > 0 :
                    edge = Edge(node, net1.Nodes[CoordDecoration.GenName(x-1,y-1)])
                    edges1.AddMember(edge)
                    net1.AddEdge(edge)
                    
            d = TestDecoration(x, y)
            node.AddDecoration(d)

    for edge in net1.Edges.itervalues() :
        if edge.EndNode.Coord.X % 2 == 0 :
            edges = edge.FindDecorationProvider('EdgeType')
            edges.DropMember(edge)
            edges2.AddMember(edge)

    net2 = Graph()
    net2.AddDecorationHandler(CoordDecoration)
    net2.AddDecorationHandler(TestDecoration)
    net2.AddDecorationHandler(EdgeTypeDecoration)

    net2.Load(net1.Dump())

    # print json.dumps(net2.Dump(),indent=2)
    for e in net2.Nodes.itervalues() :
        print "{0} = {1}".format(e.Name, e.TestDecoration.Value1)

    print "type1edges"
    for e in net2.Collections['type1edges'].Members :
        print "{0} has weight {1}".format(e.Name, e.EdgeType.Weight)

    print "type2edges"
    for e in net2.Collections['type2edges'].Members :
        print "{0} has weight {1}".format(e.Name, e.EdgeType.Weight)
