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

@file    fullnet/builder.py
@author  Mic Bowman
@date    2013-12-03

This file contains the programmatic specification of the fullnet 
traffic network. It depends on the network builder package from
mobdat.

"""

import os, sys

from mobdat.netbuilder import *
from mobdat.socbuilder import *
from mobdat.common import NetworkInfo, Decoration

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
CapsuleTypeMap = {}
CapsuleMap = {}

def BuildCapsuleMaps(ng) :
    global CapsuleTypeMap
    global CapsuleMap

    for collection in ng.Collections.itervalues() :
        if Decoration.CapsuleTypeDecoration.DecorationName not in collection.Decorations :
            continue

        typename = collection.CapsuleType.Name
        if typename not in CapsuleTypeMap :
            CapsuleTypeMap[typename] = []

        CapsuleTypeMap[typename].append(collection)
        CapsuleMap[collection.Name] = collection
        print 'added %s to %s' % (collection.Name, typename)

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
BuildCapsuleMaps(netinfo)

BusinessList = []
for bcapsule in CapsuleTypeMap['plaza'] :
    blocation = Location.BusinessLocation(bcapsule)
    BusinessList.append(blocation)


print "Loaded fullnet builder extension file"
