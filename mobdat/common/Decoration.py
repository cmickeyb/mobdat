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

@file    Decoration.py
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

import uuid, json, re

## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class Decoration :
    DecorationName = 'Decoration'

    # -----------------------------------------------------------------
    @staticmethod
    def Load(graph, info) :
        return(Decoration())

    # -----------------------------------------------------------------
    def __init__(self) : 
        pass
        
    # -----------------------------------------------------------------
    def Dump(self) : 
        result = dict()
        result['__TYPE__'] = self.DecorationName

        return result

## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class NodeTypeDecoration(Decoration) :
    DecorationName = 'NodeType'

    # -----------------------------------------------------------------
    @staticmethod
    def Load(graph, info) :
        return NodeTypeDecoration(info['Name'], info['IntersectionType'], info['Render'])

    # -----------------------------------------------------------------
    def __init__(self, name, itype = 'priority', render = True) :
        Decoration.__init__(self)

        self.Name = name
        self.IntersectionType = itype
        self.Render = render

    # -----------------------------------------------------------------
    def Dump(self) :
        result = Decoration.Dump(self)
        result['Name'] = self.Name
        result['IntersectionType'] = self.IntersectionType
        result['Render'] = self.Render

## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class EdgeTypeDecoration(Decoration) :
    DecorationName = 'EdgeType'

    # -----------------------------------------------------------------
    @staticmethod
    def Load(graph, info) :
        etype = EdgeTypeDecoration(info['Name'])

        self.Lanes = info['Lanes']
        self.Priority = info['Priority']
        self.Speed = info['Speed']
        self.Width = info['Width']
        self.Signature = info['Signature']
        self.Render = info['Render']
        self.Center = info['Center']

        return etype

    # -----------------------------------------------------------------
    def __init__(self, name, lanes = 1, pri = 70, speed = 2.0, wid = 2.5, sig = '1L', render = True, center = False) :
        Decoration.__init__(self)
        self.Name = name
        self.Lanes = lanes
        self.Priority = pri
        self.Speed = speed
        self.Width = wid
        self.Signature = sig
        self.Render = render
        self.Center = center


    # -----------------------------------------------------------------
    def Dump(self) :
        result = Decoration.Dump(self)
        
        result['Name'] = self.Name
        result['Lanes'] = self.Lanes
        result['Priority'] = self.Priority
        result['Speed'] = self.Speed
        result['Width'] = self.Width
        result['Signature'] = self.Signature
        result['Render'] = self.Render
        result['Center'] = self.Center

        return result

## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class EndPointDecoration(Decoration) :
    DecorationName = 'EndPoint'

    # -----------------------------------------------------------------
    @staticmethod
    def GenFromNode(node) :
        return EndPointDecoration(EndPointDecoration.GenOutboundName(node), EndPointDecoration.GenInboundName(node))

    # -----------------------------------------------------------------
    @staticmethod
    def GenOutboundName(node) :
        return 'r' + node.Name

    # -----------------------------------------------------------------
    @staticmethod
    def GenInboundName(node) :
        return node.InputEdges[0].Name

    # -----------------------------------------------------------------
    @staticmethod
    def Load(graph, info) :
        return EndPointDecoration(info['InboundEdgeName'], info['OutboundRounteName'])

    # -----------------------------------------------------------------
    def __init__(self, iname, rname) :
        Decoration.__init__(self)

        self.InboundEdgeName = iname
        self.OutboundRouteName = rname

    # -----------------------------------------------------------------
    def Dump(self) :
        result = Decoration.Dump(self)
        
        result['InboundEdgeName'] = self.InboundEdgeName
        result['OutboundRounteName'] = self.OutboundRouteName

        return result
