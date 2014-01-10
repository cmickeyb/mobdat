#!/usr/bin/python
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

@file    SocialBuilder.py
@author  Mic Bowman
@date    2013-12-03

This file defines the SocialBuilder class for building the SocialConnector
configuration file from the mobdat traffic network. 

"""

import os, sys, warnings

# we need to import python modules from the $SUMO_HOME/tools directory
sys.path.append(os.path.join(os.environ.get("OPENSIM","/share/opensim"),"lib","python"))
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "lib")))

import json, string

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class SocialBuilder :

    # -----------------------------------------------------------------
    def __init__(self, settings, net, netinfo) :

        self.Network = net
        self.NetworkInfo = netinfo
        self.EdgeMap = {}
        self.NodeMap = {}

        try :
            self.InjectPrefix = settings["NetworkBuilder"].get("InjectionPrefix","IN")
            self.InjectionFile = settings["SocialConnector"]["NodeDataFile"]
        except NameError as detail: 
            warnings.warn("Failed processing social configuration; name error %s" % (str(detail)))
            sys.exit(-1)
        except KeyError as detail: 
            warnings.warn("unable to locate social configuration value for %s" % (str(detail)))
            sys.exit(-1)
        except :
            warnings.warn("SocialBuilder configuration failed; %s" % (sys.exc_info()[0]))
            sys.exit(-1)

    # -----------------------------------------------------------------
    def PushNetworkToSocial(self) :
        nlist = []

        for node in self.Network.gNodes.itervalues() :
            if string.find(node.Name,self.InjectPrefix) != 0 :
                continue

            ninfo = {}
            ninfo["Name"] = node.Name
            ninfo["Type"] = node.NodeType.Name
            ninfo["InEdge"] = node.IEdges[0].Name
            ninfo["OutRoute"] = "r" + node.Name
            nlist.append(ninfo)

        with open(self.InjectionFile,"w") as fp :
            json.dump(nlist,fp,indent=2)


