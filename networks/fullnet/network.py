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

from mobdat.builder import *
from mobdat.common import NetworkInfo
from mobdat.common.Utilities import GenName, GenNameFromCoordinates

# -----------------------------------------------------------------
# -----------------------------------------------------------------
def ConvertNodeCoordinate(prefix, p) :
    return GenNameFromCoordinates(p[0], p[1], prefix)

# -----------------------------------------------------------------
# -----------------------------------------------------------------
def ConvertEdgeCoordinate(prefix, p1, p2) :
    return ConvertNodeCoordinate(prefix, p1) + '=O=' + ConvertNodeCoordinate(prefix, p2)

# -----------------------------------------------------------------
# -----------------------------------------------------------------
def BuildNetwork() :
    global netinfo, locinfo

    # residence and business nodes
    rntype = netinfo.AddNodeType('townhouse', 'priority')
    antype = netinfo.AddNodeType('apartment', 'priority', False)
    bntype = netinfo.AddNodeType('business', 'priority', False)

    # basic roadway nodes and edges
    pntype = netinfo.AddNodeType('priority','priority_stop')
    sntype = netinfo.AddNodeType('stoplight','traffic_light')

    e1A = netinfo.AddEdgeType('etype1A', 1, 70, 2.0, sig='1L')
    e1B = netinfo.AddEdgeType('etype1B', 1, 40, 1.5, sig='1L')
    e1C = netinfo.AddEdgeType('etype1C', 1, 20, 1.0, sig='1L')
    e2A = netinfo.AddEdgeType('etype2A', 2, 70, 3.0, sig='2L')
    e2B = netinfo.AddEdgeType('etype2B', 2, 40, 2.0, sig='2L')
    e2C = netinfo.AddEdgeType('etype2C', 2, 20, 1.0, sig='2L')

    e1way = netinfo.AddEdgeType('1way2lane', 2, 40, 2.0, sig='2L', center=True) 

    # driveway
    dntype = netinfo.AddNodeType('driveway', 'priority_stop') 
    edrv = netinfo.AddEdgeType('driveway', 1, 10, 0.5, sig='D')

    # parking lots
    #plotnode  = netinfo.AddNodeType('parking_drive_intersection', 'priority', False)
    #plotentry = netinfo.AddEdgeType('parking_entry', 1, 20, 1.0, sig='1L', render=False)
    #plotdrive = netinfo.AddEdgeType('parking_drive', 1, 10, 0.5, sig='D', render=False)
    plotnode  = netinfo.AddNodeType('parking_drive_intersection', 'priority')
    plotentry = netinfo.AddEdgeType('parking_entry', 1, 20, 1.0, sig='P')
    plotdrive = netinfo.AddEdgeType('parking_drive', 1, 10, 0.5, sig='D')

    # XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    # MAIN GRIDS
    # XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

    # Create the main east and west grids and drop the corner nodes
    netinfo.GenerateGrid(-400, -400, -100, 400, 100, 100, sntype, e2A, 'main')
    netinfo.GenerateGrid(100, -400, 400, 400, 100, 100, sntype, e2A, 'main')
    netinfo.DropNodesByPattern('main400[EW][34]00[SN]')

    # All of these nodes should be four way stops, they are the
    # two lane intersections

    # netinfo.SetNodeTypeByPattern('main[24]00[EW][24]00[NS]',pntype)
    # netinfo.SetNodeTypeByPattern('main[24]00[EW]0N',pntype)

    # And then set a bunch of the edges to be two lane instead
    # of the four lane edges we created for the rest of the grid
    netinfo.SetEdgeTypeByPattern('main[0-9]*[EW]200[NS]=O=main[0-9]*[EW]200[NS]',e1A)
    netinfo.SetEdgeTypeByPattern('main[0-9]*[EW]400[NS]=O=main[0-9]*[EW]400[NS]',e1A)

    netinfo.SetEdgeTypeByPattern('main300[EW][0-9]*[NS]=O=main300[EW][0-9]*[NS]',e1A)
    netinfo.SetEdgeTypeByPattern('main400[EW][0-9]*[NS]=O=main400[EW][0-9]*[NS]',e1A)

    # XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    # PLAZA GRID
    # XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

    # Create the plaza grid in the center of the map
    netinfo.GenerateGrid(-50, -250, 50, 250, 50, 50, sntype, e1B, 'plaza')

    # Make the east and west edges one way
    # pattern = 'plaza50W{0}{2}=O=plaza50W{1}{3}'
    for ns in range(-250, 250, 50) :
        netinfo.DropEdgeByName(ConvertEdgeCoordinate('plaza', (-50, ns), (-50, ns + 50)))

    for ns in range(-200, 300, 50) :
        netinfo.DropEdgeByName(ConvertEdgeCoordinate('plaza', ( 50, ns), ( 50, ns - 50)))

    # Make the north and south most east/west streets one way as well
    netinfo.DropEdgeByName('plaza50E250S=O=plaza0E250S')
    netinfo.DropEdgeByName('plaza0E250S=O=plaza50W250S')
    netinfo.DropEdgeByName('plaza50W250N=O=plaza0E250N')
    netinfo.DropEdgeByName('plaza0E250N=O=plaza50E250N')

    # The one way streets are all 2 lanes
    netinfo.SetEdgeTypeByPattern('plaza50[EW].*=O=plaza50[EW].*',e1way)
    netinfo.SetEdgeTypeByPattern('plaza.*250[NS]=O=plaza.*250[NS]',e1way)

    # The central north/south road is four lane
    netinfo.SetEdgeTypeByPattern('plaza[0-9]*[EW]100[NS]=O=plaza[0-9]*[EW]100[NS]',e2A)
    netinfo.SetEdgeTypeByPattern('plaza[0-9]*[EW]0N=O=plaza[0-9]*[EW]0N',e2A)
    netinfo.SetEdgeTypeByPattern('plaza0E[0-9]*[NS]=O=plaza0E[0-9]*[NS]',e2A)
    netinfo.SetEdgeTypeByPattern('plaza0E[0-9]*[NS]=O=plaza0E[0-9]*[NS]',e2A)

    # XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    # CONNECT THE GRIDS
    # XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

    # Create nodes at the north and south ends of the plaza
    netinfo.AddNode(0, -300, sntype, 'main') # south end of the plaza
    netinfo.AddNode(0, 300, sntype, 'main')  # north end of the plaza

    # And connect them to the east and west main grids
    netinfo.ConnectNodes(netinfo.Nodes['main100W300N'],netinfo.Nodes['main0E300N'],e2A)
    netinfo.ConnectNodes(netinfo.Nodes['main100E300N'],netinfo.Nodes['main0E300N'],e2A)
    netinfo.ConnectNodes(netinfo.Nodes['main100W300S'],netinfo.Nodes['main0E300S'],e2A)
    netinfo.ConnectNodes(netinfo.Nodes['main100E300S'],netinfo.Nodes['main0E300S'],e2A)

    # Connect the plaza nodes to the north & south ends
    netinfo.ConnectNodes(netinfo.Nodes['plaza0E250S'],netinfo.Nodes['main0E300S'],e2A)
    netinfo.ConnectNodes(netinfo.Nodes['plaza0E250N'],netinfo.Nodes['main0E300N'],e2A)

    # Connect the plaza nodes to the east and west roads
    netinfo.ConnectNodes(netinfo.Nodes['main100W100N'],netinfo.Nodes['plaza50W100N'],e2A)
    netinfo.ConnectNodes(netinfo.Nodes['main100W100S'],netinfo.Nodes['plaza50W100S'],e2A)
    netinfo.ConnectNodes(netinfo.Nodes['main100E100N'],netinfo.Nodes['plaza50E100N'],e2A)
    netinfo.ConnectNodes(netinfo.Nodes['main100E100S'],netinfo.Nodes['plaza50E100S'],e2A)
    netinfo.ConnectNodes(netinfo.Nodes['main100W0N'],netinfo.Nodes['plaza50W0N'],e2A)
    netinfo.ConnectNodes(netinfo.Nodes['main100E0N'],netinfo.Nodes['plaza50E0N'],e2A)

    netinfo.ConnectNodes(netinfo.Nodes['main100W200S'], netinfo.Nodes['plaza50W200S'], e1A)
    netinfo.ConnectNodes(netinfo.Nodes['main100E200S'], netinfo.Nodes['plaza50E200S'], e1A)
    netinfo.ConnectNodes(netinfo.Nodes['main100W200N'], netinfo.Nodes['plaza50W200N'], e1A)
    netinfo.ConnectNodes(netinfo.Nodes['main100E200N'], netinfo.Nodes['plaza50E200N'], e1A)

    # XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    # BUILD THE RESIDENTIAL NEIGHBORHOODS
    # XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

    rgenv = NetBuilder.ResidentialGenerator(e1C, dntype, edrv, rntype, bspace = 20, spacing = 10, driveway = 5)
    rgenh = NetBuilder.ResidentialGenerator(e1C, dntype, edrv, rntype, bspace = 40, spacing = 10)

    for ew in [-400, -300, 300, 400] :
        for nw in range (-200, 200, 100) :
            node1 = netinfo.Nodes[ConvertNodeCoordinate('main', (ew, nw))]
            node2 = netinfo.Nodes[ConvertNodeCoordinate('main', (ew, nw + 100))]
            locinfo.CreateCapsule('townhouse', netinfo.GenerateResidential(node1, node2, rgenv))

    for nw in [-400, 400] :
        for ew in [-300, -200, 100, 200] :
            node1 = netinfo.Nodes[ConvertNodeCoordinate('main', (ew, nw))]
            node2 = netinfo.Nodes[ConvertNodeCoordinate('main', (ew + 100, nw))]
            locinfo.CreateCapsule('townhouse', netinfo.GenerateResidential(node1, node2, rgenv))

    rgenv.BothSides = False
    locinfo.CreateCapsule('townhouse', netinfo.GenerateResidential(netinfo.Nodes['main300W200N'],netinfo.Nodes['main400W200N'], rgenv))
    locinfo.CreateCapsule('townhouse', netinfo.GenerateResidential(netinfo.Nodes['main300E200N'],netinfo.Nodes['main400E200N'], rgenv))

    rgenv.DrivewayLength = - rgenv.DrivewayLength
    locinfo.CreateCapsule('townhouse', netinfo.GenerateResidential(netinfo.Nodes['main400W200S'],netinfo.Nodes['main300W200S'], rgenv))
    locinfo.CreateCapsule('townhouse', netinfo.GenerateResidential(netinfo.Nodes['main400E200S'],netinfo.Nodes['main300E200S'], rgenv))

    # some of the malls to be marked as residential apartments
    rgenplR = NetBuilder.ResidentialGenerator(plotentry, plotnode, plotdrive, antype, driveway = -8, bspace = 5, spacing = 5, both = False)
    rgenplL = NetBuilder.ResidentialGenerator(plotentry, plotnode, plotdrive, antype, driveway = 8, bspace = 5, spacing = 5, both = False)

    for n in ['main200W200S', 'main100E200S', 'main200E200S', 'main300W200N', 'main200W200N', 'main100E200N'] :
        locinfo.CreateCapsule('apartment', netinfo.BuildSimpleParkingLotEW(netinfo.Nodes[n], pntype, rgenplR, 'apartment', offset=-15, slength=40, elength=60))
        locinfo.CreateCapsule('apartment', netinfo.BuildSimpleParkingLotEW(netinfo.Nodes[n], pntype, rgenplL, 'apartment', offset=15, slength=40, elength=60))

    for n in ['main200W200S', 'main200W100S', 'main200W200N', 'main200W100N'] : 
        locinfo.CreateCapsule('apartment', netinfo.BuildSimpleParkingLotNS(netinfo.Nodes[n], pntype, rgenplR, 'apartment', offset=-30))
        locinfo.CreateCapsule('apartment', netinfo.BuildSimpleParkingLotNS(netinfo.Nodes[n], pntype, rgenplL, 'apartment', offset=30))

    for n in ['main200E100S', 'main200E0N', 'main200E100N'] : 
        locinfo.CreateCapsule('apartment', netinfo.BuildSimpleParkingLotNS(netinfo.Nodes[n], pntype, rgenplR, 'apartment', offset=-30))
        locinfo.CreateCapsule('apartment', netinfo.BuildSimpleParkingLotNS(netinfo.Nodes[n], pntype, rgenplL, 'apartment', offset=30))

    # XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    # BUILD THE BUSINESS NEIGHBORHOODS
    # XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

    rgenplR = NetBuilder.ResidentialGenerator(plotentry, plotnode, plotdrive, bntype, driveway = 8, bspace = 5, spacing = 5, both = False)
    rgenplL = NetBuilder.ResidentialGenerator(plotentry, plotnode, plotdrive, bntype, driveway = -8, bspace = 5, spacing = 5, both = False)

    # mark some school
    for n in ['main300W200S', 'main200E200N'] :
        locinfo.CreateCapsule('civic', netinfo.BuildSimpleParkingLotEW(netinfo.Nodes[n], pntype, rgenplR, 'civic', offset=-15, slength=40, elength=60))
        locinfo.CreateCapsule('civic', netinfo.BuildSimpleParkingLotEW(netinfo.Nodes[n], pntype, rgenplL, 'civic', offset=15, slength=40, elength=60))

    # these are the downtown work and shopping plazas
    for ns in range(-200, 300, 50) :
        wname = ConvertNodeCoordinate('plaza', (-50, ns))
        locinfo.CreateCapsule('plaza', netinfo.BuildSimpleParkingLotSN(netinfo.Nodes[wname], pntype, rgenplL, 'plaza', offset=25, slength = 17.5, elength=32.5))

        ename = ConvertNodeCoordinate('plaza', (50, ns-50))
        locinfo.CreateCapsule('plaza', netinfo.BuildSimpleParkingLotNS(netinfo.Nodes[ename], pntype, rgenplR, 'plaza', offset=-25, slength = 17.5, elength=32.5))
        
    # these are the main business areas
    for n in ['main200W300S', 'main200W0N'] : 
        locinfo.CreateCapsule('mall', netinfo.BuildSimpleParkingLotNS(netinfo.Nodes[n], pntype, rgenplR, 'mall', offset=-30))
        locinfo.CreateCapsule('mall', netinfo.BuildSimpleParkingLotNS(netinfo.Nodes[n], pntype, rgenplL, 'mall', offset=30))

    for n in ['main200E300S', 'main200E200S', 'main200E200N'] : 
        locinfo.CreateCapsule('mall', netinfo.BuildSimpleParkingLotNS(netinfo.Nodes[n], pntype, rgenplR, 'mall', offset=-30))
        locinfo.CreateCapsule('mall', netinfo.BuildSimpleParkingLotNS(netinfo.Nodes[n], pntype, rgenplL, 'mall', offset=30))

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
BuildNetwork()

print "Loaded fullnet network builder extension file"
