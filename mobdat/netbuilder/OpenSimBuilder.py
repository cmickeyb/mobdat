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

@file    OpenSimBuilder.py
@author  Mic Bowman
@date    2013-12-03

This file defines the opensim builder class for mobdat traffic networks.
The functions in this file will rez a mobdat network in an OpenSim region.
"""

import os, sys, warnings

# we need to import python modules from the $SUMO_HOME/tools directory
sys.path.append(os.path.join(os.environ.get("OPENSIM","/share/opensim"),"lib","python"))
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "lib")))

import uuid
import OpenSimRemoteControl

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class OpenSimBuilder :

    # -----------------------------------------------------------------
    def __init__(self, settings, net, netinfo) :

        self.Network = net
        self.NetworkInfo = netinfo
        self.EdgeMap = {}
        self.NodeMap = {}

        try :
            self.OpenSimConnector = OpenSimRemoteControl.OpenSimRemoteControl(settings["OpenSimConnector"]["EndPoint"])
            self.OpenSimConnector.Capability = uuid.UUID(settings["OpenSimConnector"]["Capability"])
            self.OpenSimConnector.Scene = settings["OpenSimConnector"]["Scene"]
        except NameError as detail: 
            warnings.warn("Failed processing OpenSim configuration; name error %s" % (str(detail)))
            sys.exit(-1)
        except KeyError as detail: 
            warnings.warn("unable to locate OpenSim configuration value for %s" % (str(detail)))
            sys.exit(-1)
        except :
            warnings.warn("OpenSimConnector configuration failed; %s" % (sys.exc_info()[0]))
            sys.exit(-1)

    # -----------------------------------------------------------------
    def ComputeRotation(self, sig1, sig2) :
        for i in range(4) :
            success = True
            for j in range(4) :
                if sig1[j] != sig2[(i + j) % 4] and sig2[(i + j) % 4] != '*' :
                    success = False
                    break

            if success :
                return i

        return -1

    # -----------------------------------------------------------------
    def ComputeLocation(self, snode, enode) :
        if snode.Name not in self.NodeMap :
            warnings.warn('cannot find node %s in the node map' % (snode.Name))
            return False

        if enode.Name not in self.NodeMap :
            warnings.warn('cannot find node %s in the node map' % (enode.Name))
            return False

        sbump = self.NodeMap[snode.Name].Padding
        ebump = self.NodeMap[enode.Name].Padding
    
        deltax = enode.X - snode.X
        deltay = enode.Y - snode.Y

        # west
        if deltax < 0 and deltay == 0 :
            s1x = snode.X - sbump
            s1y = snode.Y
            e1x = enode.X + ebump
            e1y = enode.Y

        # north
        elif deltax == 0 and deltay > 0 :
            s1x = snode.X
            s1y = snode.Y + sbump
            e1x = enode.X
            e1y = enode.Y - ebump

        # east
        elif deltax > 0 and deltay == 0 :
            s1x = snode.X + sbump
            s1y = snode.Y
            e1x = enode.X - ebump
            e1y = enode.Y

        # south
        elif deltax == 0 and deltay < 0 :
            s1x = snode.X
            s1y = snode.Y - sbump
            e1x = enode.X
            e1y = enode.Y + ebump

        else :
            warnings.warn('something went wrong computing the signature')
            return(0,0,0,0)

        return (s1x + 512, s1y + 512, e1x + 512, e1y + 512)


    # -----------------------------------------------------------------
    def PushNetworkToOpenSim(self) :
        self.CreateNodes()
        self.CreateEdges()

    # -----------------------------------------------------------------
    def CreateEdges(self) :

        for e in self.Network.gEdges :
            edge = self.Network.gEdges[e]

            if edge.Name in self.EdgeMap :
                continue

            if edge.EdgeType.Name not in self.NetworkInfo.EdgeTypeMap :
                warnings.warn('Failed to find asset for %s' % (edge.EdgeType.Name))
                continue 

            # check to see if we need to render this edge at all
            if edge.EdgeType.Render :
                asset = self.NetworkInfo.EdgeTypeMap[edge.EdgeType.Name][0].AssetID
                zoff = self.NetworkInfo.EdgeTypeMap[edge.EdgeType.Name][0].ZOffset

                (p1x, p1y, p2x, p2y) = self.ComputeLocation(edge.StartNode, edge.EndNode)

                startparms = "{ 'spoint' : '<%f, %f, %f>', 'epoint' : '<%f, %f, %f>' }" % (p1x, p1y, zoff, p2x, p2y, zoff)

                result = self.OpenSimConnector.CreateObject(asset, pos=[p1x, p1y, 20.5], name=e, parm=startparms)

            self.EdgeMap[edge.Name] = True
            self.EdgeMap[edge.ReverseName()] = True
    
    # -----------------------------------------------------------------
    def CreateNodes(self) :
        for n in self.Network.gNodes :
            node = self.Network.gNodes[n]

            tname = node.NodeType.Name
            sig1 = node.Signature()

            if tname not in self.NetworkInfo.NodeTypeMap :
                warnings.warn('Unable to locate node type %s' % (tname))
                continue

            success = False
            for itype in self.NetworkInfo.NodeTypeMap[tname] :
                sig2 = itype.Signature

                rot = self.ComputeRotation(sig1, sig2)
                if rot >= 0 :
                    self.NodeMap[n] = itype

                    p1x = node.X + 512
                    p1y = node.Y + 512
                    p1z = itype.ZOffset
                    asset = itype.AssetID
                    startparms = "{ 'center' : '<%f, %f, %f>', 'angle' : %f }" % (p1x, p1y, p1z, 90.0 * rot)

                    if node.NodeType.Render :
                        result = self.OpenSimConnector.CreateObject(asset, pos=[p1x, p1y, p1z], name=n, parm=startparms)

                    success = True
                    break

            if not success :
                warnings.warn("No match for node %s with type %s and signature %s" % (n, tname, sig1))
