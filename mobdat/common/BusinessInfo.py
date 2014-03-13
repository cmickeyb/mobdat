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

@file    BusinessInfo.py
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
import json

logger = logging.getLogger(__name__)

## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class BusinessInfo :

    # -----------------------------------------------------------------
    def __init__(self, netinfo) :
        self.JobProfiles = {}
        self.BusinessProfiles = {}
        self.BusinessList = {}

        self.BusinessLocationProfiles = {}
        self.BusinessLocations = []

        self.CapsuleTypeMap = {}
        self.CapsuleMap = {}

        self._BuildCapsuleMaps(netinfo)

    # -----------------------------------------------------------------
    def _BuildCapsuleMaps(self, netinfo) :
        for collection in netinfo.Collections.itervalues() :
            if CapsuleTypeDecoration.DecorationName not in collection.Decorations :
                continue

            typename = collection.CapsuleType.Name
            if typename not in self.CapsuleTypeMap :
                self.CapsuleTypeMap[typename] = []

            self.CapsuleTypeMap[typename].append(collection)
            self.CapsuleMap[collection.Name] = collection

    # -----------------------------------------------------------------
    def Dump(self) :
        result = dict()
        result['BusinessList'] = []
        for c in self.BusinessList.itervalues() :
            result['BusinessList'].append(c.Dump())

        result['BusinessProfiles'] = []
        for p in self.BusinessProfiles.itervalues() :
            result['BusinessProfiles'].append(p.Dump())

        result['BusinessLocations'] = []
        for bl in self.BusinessLocations :
            result['BusinessLocations'].append(bl.Dump())

        result['BusinessLocationProfiles'] = []
        for blp in self.BusinessLocationProfiles.itervalues() :
            result['BusinessLocationProfiles'].append(blp.Dump())

        return result
