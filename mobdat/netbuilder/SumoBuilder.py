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

@file    SumoBuilder.py
@author  Mic Bowman
@date    2013-12-03

This file defines the SumoBuilder class that translates mobdat traffic
network into a network specification suitable for driving the sumo
traffic simulator.

"""

import os, sys, warnings

# we need to import python modules from the $SUMO_HOME/tools directory
sys.path.append(os.path.join(os.environ.get("OPENSIM","/share/opensim"),"lib","python"))
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "lib")))

import uuid, string
import OpenSimRemoteControl

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class SumoBuilder :

    # -----------------------------------------------------------------
    def __init__(self, settings, net, netinfo) :

        self.Network = net
        self.NetworkInfo = netinfo
        self.ScaleValue = 3.0

        try :
            self.InjectPrefix = settings["NetworkBuilder"].get("InjectionPrefix","IN")
            self.Path = settings["SumoConnector"].get("SumoNetworkPath",".")
            self.Prefix = settings["SumoConnector"].get("SumoDataFilePrefix","network")
            self.ScaleValue = settings["SumoConnector"].get("NetworkScaleFactor",3.0)
        except NameError as detail: 
            warnings.warn("Failed processing sumo configuration; name error %s" % (str(detail)))
            sys.exit(-1)
        except KeyError as detail: 
            warnings.warn("unable to locate sumo configuration value for %s" % (str(detail)))
            sys.exit(-1)
        except :
            warnings.warn("SumoBuilder configuration failed; %s" % (sys.exc_info()[0]))
            sys.exit(-1)

    # -----------------------------------------------------------------
    def Scale(self, value) :
        return self.ScaleValue * value

    # -----------------------------------------------------------------
    def CreateEdges(self) :
        fname = os.path.join(self.Path,self.Prefix + '.edg.xml')

        with open(fname, 'w') as fp :
            fp.write("<edges>\n")

            for e in self.Network.gEdges :
                edge = self.Network.gEdges[e]
                sn = edge.StartNode.Name
                en = edge.EndNode.Name
                etype = edge.EdgeType.Name

                fp.write("  <edge id=\"%s\" from=\"%s\" to=\"%s\" type=\"%s\" />\n" % (e, sn, en, etype))

            fp.write("</edges>\n")
        
    # -----------------------------------------------------------------
    def CreateNodes(self) :
        fname = os.path.join(self.Path,self.Prefix + '.nod.xml')

        with open(fname, 'w') as fp :
            fp.write("<nodes>\n")

            for n in self.Network.gNodes :
                node = self.Network.gNodes[n]
                ntype = node.NodeType.NType
                fp.write("  <node id=\"%s\" x=\"%d\" y=\"%d\" z=\"0\"  type=\"%s\" />\n" % (n, self.Scale(node.X), self.Scale(node.Y), ntype))

            fp.write("</nodes>\n")

    # -----------------------------------------------------------------
    def CreateEdgeTypes(self) :
        fname = os.path.join(self.Path,self.Prefix + '.typ.xml')

        with open(fname, 'w') as fp :
            fp.write("<types>\n")

            for et in self.Network.gEdgeTypes :
                etype = self.Network.gEdgeTypes[et]
                fp.write("  <type id=\"%s\" priority=\"%d\" numLanes=\"%d\" speed=\"%f\" width=\"%f\" />\n" %
                         (et, etype.Priority, etype.Lanes, self.Scale(etype.Speed), self.Scale(etype.Width)))

            fp.write("</types>\n")

    # -----------------------------------------------------------------
    def CreateRoutes(self) :
        vtfmt = '  <vType id="{0}" accel="{1}" decel="{2}" sigma="{3}" length="{4}" minGap="{5}" maxSpeed="{6}" guiShape="passenger"/>'

        fname = os.path.join(self.Path,self.Prefix + '.rou.xml')
        
        with open(fname, 'w') as fp :
            fp.write("<routes>\n")
            
            for v in self.NetworkInfo.VehicleTypes :
                vtype = self.NetworkInfo.VehicleTypes[v]
                fp.write(vtfmt.format(v, self.Scale(vtype.Acceleration), self.Scale(vtype.Deceleration),
                                      vtype.Sigma, self.Scale(vtype.Length), self.Scale(vtype.MinGap), self.Scale(vtype.MaxSpeed)) + "\n")

            fp.write("\n")

            for n in self.Network.gNodes :
                if string.find(n,self.InjectPrefix) == 0 :
                    node = self.Network.gNodes[n]
                    for edge in node.OEdges :
                        for redge in edge.EndNode.OEdges :
                            if redge.EndNode == node :
                                name = "r" + n
                                edges = edge.Name + " " + redge.Name
                                fp.write("  <route id=\"%s\" edges=\"%s\" />\n" % (name, edges))
                                break

            fp.write("</routes>\n")

    # -----------------------------------------------------------------
    def PushNetworkToSumo(self) :
        self.CreateNodes()
        self.CreateEdges()
        self.CreateEdgeTypes()
        self.CreateRoutes()

