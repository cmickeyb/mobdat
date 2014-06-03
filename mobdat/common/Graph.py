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
def GenEdgeName(snode, enode) :
    return snode.Name + '=O=' + enode.Name

## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
def GenNodeName(prefix = 'node') :
    return GenName(prefix)

## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class GraphObject :

    # -----------------------------------------------------------------
    def __init__(self, name) :
        self.Name = name
        self.Decorations = {}
        self.Collections = {}

        self.OutputEdges = []
        self.InputEdges = []

        self.AddDecoration(NodeTypeDecoration(self.__class__.__name__))

    # -----------------------------------------------------------------
    def __getattr__(self, attr) :
        """
        __getattr__

        Look for a reference to the attribute among the collection of decorations
        associated with the object and in the output edges. 
        """

        # First look for a decoration with the right name
        provider = self.FindDecorationProvider(attr)
        if provider :
            return provider.Decorations[attr]

        # Next look for an edge with the right name, if there
        # are multiple then take the first one found
        for edge in self.OutputEdges :
            if edge.NodeType.Name == attr :
                return edge.EndNode

        nodetype = self.__class__.__name__
        if 'NodeType' in self.Decorations :
            nodetype = self.Decorations['NodeType'].Name

        raise AttributeError("graph object %r of type %r has no attribute %r" % (self.Name, nodetype, attr))

    # -----------------------------------------------------------------
    def _FindEdges(self, edgelist, edgetype) :
        """
        _FindEdges -- Build and return a list of edges that match the
        specified type.

        Args: 
            edgelist -- list of objects of type Graph.Edge
            edgetype -- string name of edge type
        """
        edges = []
        for edge in edgelist :
            if edgetype and edge.NodeType.Name != edgetype :
                continue
            edges.append(edge)
        return edges

    def FindInputEdges(self, edgetype = None) :
        return self._FindEdges(self.InputEdges, edgetype)

    def FindOutputEdges(self, edgetype = None) :
        return self._FindEdges(self.OutputEdges, edgetype)

    # -----------------------------------------------------------------
    def _IterEdges(self, edgelist, edgetype) :
        """
        _IterEdges -- Build and return an iterator over the edges of a
        specified type.

        Args: 
            edgelist -- list of objects of type Graph.Edge
            edgetype -- string name of edge type
        """
        for edge in edgelist :
            if edgetype and edge.NodeType.Name != edgetype :
                continue
            yield edge

    def IterInputEdges(self, edgetype = None) :
        return self._IterEdges(self.InputEdges, edgetype)

    def IterOutputEdges(self, edgetype = None) :
        return self._IterEdges(self.OutputEdges, edgetype)

    # -----------------------------------------------------------------
    def AddInputEdge(self, edge) :
        self.InputEdges.append(edge)

    # -----------------------------------------------------------------
    def AddOutputEdge(self, edge) :
        self.OutputEdges.append(edge)

    # -----------------------------------------------------------------
    def AddToCollection(self, collection) :
        self.Collections[collection.Name] = collection

    # -----------------------------------------------------------------
    def DropFromCollection(self, collection) :
        del self.Collections[collection.Name]

    # -----------------------------------------------------------------
    def AddDecoration(self, decoration) :
        decoration.HostObject = self
        self.Decorations[decoration.DecorationName] = decoration

    # -----------------------------------------------------------------
    def FindDecorationProvider(self, attr) :
        """
        FindDecorationProvider -- check this object and any object in
        which this object is a member for an attribute that matches
        the specified attribute.

        Args:
            attr -- string, attribute name
        """
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
class Edge(GraphObject) :

    # -----------------------------------------------------------------
    @staticmethod
    def Load(graph, einfo) :
        sname = einfo['StartNode']
        snode = graph.Nodes[sname] if sname in graph.Nodes else graph.Collections[sname]
        ename = einfo['EndNode']
        enode = graph.Nodes[ename] if ename in graph.Nodes else graph.Collections[ename]
        edge = Edge(snode, enode, einfo['Name'])

        edge.LoadDecorations(graph, einfo)

        return edge

    # -----------------------------------------------------------------
    def __init__(self, snode, enode, name = None) :
        if not name : name = GenEdgeName(snode, enode)
        GraphObject.__init__(self, name)

        self.StartNode = snode
        self.EndNode = enode

        snode.AddOutputEdge(self)
        enode.AddInputEdge(self)

    # -----------------------------------------------------------------
    def Dump(self) : 
        result = GraphObject.Dump(self)

        result['StartNode'] = self.StartNode.Name
        result['EndNode'] = self.EndNode.Name

        return result

## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class Node(GraphObject) :

    # -----------------------------------------------------------------
    @staticmethod
    def Load(graph, ninfo) :
        node = Node(name = ninfo['Name'])
        node.LoadDecorations(graph, ninfo)
            
        return node

    # -----------------------------------------------------------------
    @staticmethod
    def LoadMembers(graph, ninfo) :
        node = graph.Nodes[ninfo['Name']]
        for mname in ninfo['Members'] :
            node.AddMember(graph.FindByName(mname))

    # -----------------------------------------------------------------
    def __init__(self, members = [], name = None, prefix = 'node') :
        if not name : name = GenNodeName(prefix)
        GraphObject.__init__(self, name)

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
        result = GraphObject.Dump(self)

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
    def __init__(self) :
        self.DecorationMap = {}

        self.Edges = {}
        self.Nodes = {}

        for dtype in CommonDecorations :
            self.AddDecorationHandler(dtype)

    # -----------------------------------------------------------------
    def Dump(self) :
        result = dict()

        nodes = []
        for node in self.Nodes.itervalues() :
            nodes.append(node.Dump())
        result['Nodes'] = nodes

        edges = []
        for edge in self.Edges.itervalues() :
            edges.append(edge.Dump())
        result['Edges'] = edges

        return result
    
    # -----------------------------------------------------------------
    def Load(self, info) :
        """
        Load the graph from the dictionary representation
        """
        for ninfo in info['Nodes'] :
            self.AddNode(Node.Load(self, ninfo))

        for einfo in info['Edges'] :
            self.AddEdge(Edge.Load(self, einfo))

        # setting up the membership after creating all the
        # collections makes it possible to have collections within collections
        for ninfo in info['Nodes'] :
            Node.LoadMembers(self, ninfo)

    # =================================================================
    # DECORATION METHODS
    # =================================================================

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

    # =================================================================
    # UTILITY METHODS
    # =================================================================

    # -----------------------------------------------------------------
    def FindByName(self, name) :
        if name in self.Nodes :
            return self.Nodes[name]
        elif name in self.Edges :
            return self.Edges[name]
        else :
            raise NameError("graph contains no object named %s" % mname)

    # =================================================================
    # NODE methods
    # =================================================================

    # -----------------------------------------------------------------
    def AddNode(self, node) :
        self.Nodes[node.Name] = node

    # -----------------------------------------------------------------
    def DropNode(self, node) :
        # need to use values because dropping the member in the collection
        # will change the list of connections here

        # drop this node from other nodes where it is a member
        for collection in node.Collections.values() :
            collection.DropMember(node)

        # drop all nodes that are a member of this one
        for obj in node.Members[:] :
            node.DropMember(obj)

        for edge in node.InputEdges[:] :
            self.DropEdge(edge)

        for edge in node.OutputEdges[:] :
            self.DropEdge(edge)

        del self.Nodes[node.Name]

    # -----------------------------------------------------------------
    def FindNodeByName(self, name) :
        if name in self.Nodes :
            return self.Nodes[name]
        else :
            raise NameError("graph contains no node named %s" % name)

    # -----------------------------------------------------------------
    def DropNodeByName(self, name) :
        if name not in self.Nodes :
            return

        self.DropNode(self.Nodes[name])

    # -----------------------------------------------------------------
    def DropNodes(self, pattern = None, nodetype = None) :
        """
        Args:
            pattern -- string representing a regular expression
            nodetype -- string name of a node type
        """
        nodes = self.FindNodes(pattern, nodetype)
        for node in nodes :
            self.DropNode(node)

        return True

    # -----------------------------------------------------------------
    def FindNodes(self, pattern = None, nodetype = None, predicate = None) :
        """
        Args:
            pattern -- string representing a regular expression
            nodetype -- string name of a node type
        """
        nodes = []
        for name, node in self.IterNodes(pattern, nodetype, predicate) :
            nodes.append(node)

        return nodes

    # -----------------------------------------------------------------
    def IterNodes(self, pattern = None, nodetype = None, predicate = None) :
        """
        Args:
            pattern -- string representing a regular expression
            nodetype -- string name of a node type
        """
        for name, node in self.Nodes.iteritems() :
            if nodetype and node.NodeType.Name != nodetype :
                continue

            if pattern and not re.match(pattern, name) :
                continue

            if predicate and not predicate(node) :
                continue

            yield name, node

    # =================================================================
    # EDGE methods
    # =================================================================

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
    def DropEdges(self, pattern = None, edgetype = None) :
        """
        Args:
            pattern -- string representing a regular expression
            edgetype -- string name of a edge type
        """
        edges = self.FindEdges(pattern, edgetype)
        for edge in edges :
            self.DropEdge(edge)

        return True

    # -----------------------------------------------------------------
    def FindEdges(self, pattern = None, edgetype = None) :
        """
        Args:
            pattern -- string representing a regular expression
            edgetype -- string name of a edge type
        """
        edges = []
        for name, edge in self.Edges.iteritems() :
            if edgetype and edge.NodeType.Name != edgetype :
                continue

            if pattern and not re.match(pattern, name) :
                continue

            edges.append(edge)

        return edges

    # -----------------------------------------------------------------
    def IterEdges(self, pattern = None, edgetype = None) :
        """
        Args:
            pattern -- string representing a regular expression
            edgetype -- string name of a edge type
        """
        for name, edge in self.Edges.iteritems() :
            if edgetype and edge.NodeType.Name != edgetype :
                continue

            if pattern and not re.match(pattern, name) :
                continue

            yield name, edge


    # -----------------------------------------------------------------
    def DropEdgesByPattern(self, pattern) :
        # need to use items because dropping the member in the collection
        # will change the list of connections here
        for name, edge in self.Edges.items() :
            if re.match(pattern, name) :
                self.DropEdge(edge)
        
        return True

    # -----------------------------------------------------------------
    def FindEdgeByName(self, name) :
        if name in self.Edges :
            return self.Edges[name]
        else :
            raise NameError("graph contains no edge named %s" % mname)
            
    # -----------------------------------------------------------------
    def FindEdgeBetweenNodes(self, node1, node2) :
        for e in node1.OutputEdges :
            if e.EndNode == node2 :
                return e
        return None


## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
if __name__ == '__main__' :
    from mobdat.common.Utilities import GenNameFromCoordinates
    from mobdat.common.Decoration import Decoration, CoordDecoration

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
            node = Node(GenNameFromCoordinates(x, y))
            node.AddDecoration(CoordDecoration(x, y))
            net1.AddNode(node)
            if x > 0 :
                if y > 0 :
                    edge = Edge(node, net1.Nodes[GenNameFromCoordinates(x-1,y-1)])
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
