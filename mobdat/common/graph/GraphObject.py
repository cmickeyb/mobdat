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

@file    GraphObject.py
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

logger = logging.getLogger(__name__)

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
    def FindOutputEdge(self, enode, edgetype = None) :
        for e in self._FindEdges(self.OutputEdges, edgetype) :
            if e.EndNode == enode : return e

        return None

    def FindInputEdge(self, snode, edgetype = None) :
        for e in self._FindEdges(self.InputEdges, edgetype) :
            if e.StartNode == snode : return e

        return None
        
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
    def EdgeExists(self, endnode, edgetype = None) :
        for edge in self._IterEdges(self.OutputEdges, edgetype) :
            if edge.EndNode == endnode : return edge

        return None

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

