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

@file    SocialConnector.py
@author  Mic Bowman
@date    2013-12-03

This module defines the SocialConnector class. This class implements
the social (people) aspects of the mobdat simulation.

"""

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class LocationCapsule :
    """
    The LocationCapsule class is a collection of LocationNodes that
    can be treated as a single allocation unit. For the purpose of
    simulating the source and destination of traffic, all LocationNodes
    in the LocationCapsule are equivalent.
    """

    def __init__(self, capacity = 1) :
        self.NodeCapacity = capacity
        self.LocationNodes = []

    def AddNode(self, info) :
        self.LocationNodes.append(LocationNode(info), self.NodeCapacity)

    def GetNode(self) :
        return random.choice(self.LocationNodes)
    
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class LocationNode :
    """
    The LocationNode class holds information that binds the social
    location profiles to the map information used to drive the
    simulation. 
    """
    def __init__(self, info, capacity = 1) :
        try :
            self.Name = info["Name"]
            self.Type = info["Type"]
            self.InEdge = info["InEdge"]
            self.OutRoute = info["OutRoute"]
            self.Capacity = capacity
        except :
            warnings.warn('failed to extract injection point data; %s' % (sys.exc_info()[0]))
            sys.exit(-1)
    

    # -----------------------------------------------------------------
    def _CreateNodeTypeMap(self, nfile) :
        self.NodeTypeMap = {}
        self.NodeNameMap = {}

        with open(nfile, 'r') as fp :
            nlist = json.load(fp)
            for ninfo in nlist :
                node = InjectionNode(ninfo)
                self.NodeNameMap[node.Name] = node
                if node.Type not in self.NodeTypeMap :
                    self.NodeTypeMap[node.Type] = []
                self.NodeTypeMap[node.Type].append(node)

        # make sure the people are more or less distributed evenly through the residences
        rescapacity = 1 + int(self.PeopleCount / len(self.NodeTypeMap['residence']))
        for node in self.NodeTypeMap['residence'] :
            node.Capacity = rescapacity

        # even distribution in the businesses is a little less important, will make this
        # more interesting in a bit
        buscapacity = 1 + int(self.PeopleCount / len(self.NodeTypeMap['business']))
        for node in self.NodeTypeMap['business'] :
            node.Capacity = 2 * buscapacity

