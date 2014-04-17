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

@file    LocationBuilder.py
@author  Mic Bowman
@date    2014-02-04

This file defines routines used to build profiles for people and places.

"""

import os, sys, warnings, copy

# we need to import python modules from the $SUMO_HOME/tools directory
sys.path.append(os.path.join(os.environ.get("OPENSIM","/share/opensim"),"lib","python"))
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "lib")))

from mobdat.common.LocationInfo import LocationInfo
from mobdat.common.Graph import Collection
from mobdat.common.Decoration import CapsuleTypeDecoration, EndPointDecoration
from mobdat.common.Location import *

## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class LocationBuilder(LocationInfo) :

    # -----------------------------------------------------------------
    def __init__(self, layinfo) :
        LocationInfo.__init__(self)

        self.LayoutInfo = layinfo
        self.CapsuleIdentifier = {} 

    # -----------------------------------------------------------------
    def GenCapsuleName(self, captypename) :
        if captypename not in self.CapsuleIdentifier :
            self.CapsuleIdentifier[captypename] = 0

        self.CapsuleIdentifier[captypename] += 1
        return captypename + str(self.CapsuleIdentifier[captypename])

    # -----------------------------------------------------------------
    def CreateCapsule(self, captypename, nodelist) :
        """
        CreateCapsule -- create a collection from the nodes and add CapsuleType
        decoration to the collection
    
        captypename -- string, the name of the capsule type
        nodelist -- list of nodes to put in the capsule
        """

        capsulename = self.GenCapsuleName(captypename)
        capsule = Collection(name = capsulename)
        capsule.AddDecoration(CapsuleTypeDecoration(captypename))

        for node in nodelist :
            node.AddDecoration(EndPointDecoration.GenFromNode(node))
            capsule.AddMember(node)

        self.AddCapsule(capsule)
        self.LayoutInfo.AddCollection(capsule)

    # -----------------------------------------------------------------
    def AddBusinessLocationProfile(self, name, employees, customers, types) :
        self.BusinessLocationProfiles[name] = BusinessLocationProfile(name, employees, customers, types)

    # -----------------------------------------------------------------
    def AddBusinessLocation(self, capsule, profile) :
        self.BusinessLocations[capsule.Name] = BusinessLocation(capsule, profile)

    # -----------------------------------------------------------------
    def AddResidentialLocationProfile(self, name, residents) :
        self.ResidentialLocationProfiles[name] = ResidentialLocationProfile(name, residents)

    # -----------------------------------------------------------------
    def AddResidentialLocation(self, capsule, profile) :
        self.ResidentialLocations[capsule.Name] = ResidentialLocation(capsule, profile)

