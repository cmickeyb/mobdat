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

@file    LocationInfo.py
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

from mobdat.common.Location import *
from Decoration import *

import json

logger = logging.getLogger(__name__)

## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class LocationInfo :

    # -----------------------------------------------------------------
    @staticmethod
    def LoadFromFile(filename, netinfo) :
        with open(filename, 'r') as fp :
            locdata = json.load(fp)

        locinfo = LocationInfo()
        locinfo.Load(locdata, netinfo)

        return locinfo

    # -----------------------------------------------------------------
    def __init__(self) :
        self.CapsuleMap = {}
        self.CapsuleTypeMap = {}

        self.BusinessLocationProfiles = {}
        self.BusinessLocations = {}

        self.ResidentialLocationProfiles = {}
        self.ResidentialLocations = {}

    # -----------------------------------------------------------------
    def AddCapsule(self, capsule) :
        """
        AddCapsule -- add a capsule to the maps

        capsule -- a NetworkInfo.Collection object that has capsule type decoration
        """
        typename = capsule.CapsuleType.Name
        if typename not in self.CapsuleTypeMap :
            self.CapsuleTypeMap[typename] = []

        self.CapsuleMap[capsule.Name] = capsule
        self.CapsuleTypeMap[typename].append(capsule)
        
    # -----------------------------------------------------------------
    def Load(self, locdata, netinfo) :
        self.CapsuleMap = {}
        self.CapsuleTypeMap = {}

        for collection in netinfo.Collections.itervalues() :
            if CapsuleTypeDecoration.DecorationName in collection.Decorations :
                self.AddCapsule(collection)

        for lpinfo in bizdata['BusinessLocationProfiles'] :
            locprofile = BusinessLocationProfile.Load(lpinfo)
            self.BusinessLocationProfiles[locprofile.ProfileName] = locprofile

        for linfo in bizdata['BusinessLocations'] :
            location = BusinessLocation.Load(linfo, locinfo, self)
            self.BusinessLocations[location.Capsule.Name] = location

        for lpinfo in perdata['ResidentialLocationProfiles'] :
            locprofile = ResidentialLocationProfile.Load(lpinfo)
            self.ResidentialLocationProfiles[locprofile.ProfileName] = locprofile

        for linfo in perdata['ResidentialLocations'] :
            location = ResidentialLocation.Load(linfo, locinfo, self)
            self.ResidentialLocations[location.Capsule.Name] = location

    # -----------------------------------------------------------------
    def Dump(self) :
        result = dict()

        result['BusinessLocationProfiles'] = []
        for blp in self.BusinessLocationProfiles.itervalues() :
            result['BusinessLocationProfiles'].append(blp.Dump())

        result['BusinessLocations'] = []
        for bl in self.BusinessLocations.itervalues() :
            result['BusinessLocations'].append(bl.Dump())

        result['ResidentialLocationProfiles'] = []
        for plp in self.ResidentialLocationProfiles.itervalues() :
            result['ResidentialLocationProfiles'].append(plp.Dump())

        result['ResidentialLocations'] = []
        for pl in self.ResidentialLocations.itervalues() :
            result['ResidentialLocations'].append(pl.Dump())

        return result
