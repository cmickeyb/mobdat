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

# -----------------------------------------------------------------
# -----------------------------------------------------------------
def BuildNetwork(ng) :

    # residence and business nodes
    rntype = ng.AddNodeType('residence', 'priority')
    bntype = ng.AddNodeType('business', 'priority', False)

    # basic roadway nodes and edges
    pntype = ng.AddNodeType('priority','priority_stop')
    sntype = ng.AddNodeType('stoplight','traffic_light')

    e1A = ng.AddEdgeType('etype1A', 1, 70, 2.0, sig='1L')
    e1B = ng.AddEdgeType('etype1B', 1, 40, 1.5, sig='1L')
    e1C = ng.AddEdgeType('etype1C', 1, 20, 1.0, sig='1L')
    e2A = ng.AddEdgeType('etype2A', 2, 70, 3.0, sig='2L')
    e2B = ng.AddEdgeType('etype2B', 2, 40, 2.0, sig='2L')
    e2C = ng.AddEdgeType('etype2C', 2, 20, 1.0, sig='2L')

    # driveway
    dntype = ng.AddNodeType('driveway', 'priority_stop') 
    edrv = ng.AddEdgeType('driveway', 1, 10, 0.5, sig='D')

    # parking lots
    #plotnode  = ng.AddNodeType('parking_drive_intersection', 'priority', False)
    #plotentry = ng.AddEdgeType('parking_entry', 1, 20, 1.0, sig='1L', render=False)
    #plotdrive = ng.AddEdgeType('parking_drive', 1, 10, 0.5, sig='D', render=False)
    plotnode  = ng.AddNodeType('parking_drive_intersection', 'priority')
    plotentry = ng.AddEdgeType('parking_entry', 1, 20, 1.0, sig='P')
    plotdrive = ng.AddEdgeType('parking_drive', 1, 10, 0.5, sig='D')

    # XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    # MAIN GRIDS
    # XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

    # Create the main east and west grids and drop the corner nodes
    ng.GenerateGrid(-400, -400, -100, 400, 100, 100, sntype, e2A, 'main')
    ng.GenerateGrid(100, -400, 400, 400, 100, 100, sntype, e2A, 'main')
    ng.DropNodeByPattern('main400[EW][34]00[SN]')

    # All of these nodes should be four way stops, they are the
    # two lane intersections
    ng.SetNodeTypeByPattern('main[24]00[EW]:[24]00[NS]',pntype)
    ng.SetNodeTypeByPattern('main[24]00[EW]:0N',pntype)

    # And then set a bunch of the edges to be two lane instead
    # of the four lane edges we created for the rest of the grid
    # ng.SetEdgeTypeByPattern('main.*[EW]0N:main.*[EW]0N',e1A)
    # ng.SetEdgeTypeByPattern('main[0-9]*[EW][24]00[NS]:main[0-9]*[EW][24]00[NS]',e1A)
    # ng.SetEdgeTypeByPattern('main[24]00[EW][0-9]*[NS]:main[24]00[EW][0-9]*[NS]',e1A)

    ng.SetEdgeTypeByPattern('main[0-9]*[EW]200[NS]:main[0-9]*[EW]200[NS]',e1A)
    ng.SetEdgeTypeByPattern('main[0-9]*[EW]400[NS]:main[0-9]*[EW]400[NS]',e1A)

    ng.SetEdgeTypeByPattern('main300[EW][0-9]*[NS]:main300[EW][0-9]*[NS]',e1A)
    ng.SetEdgeTypeByPattern('main400[EW][0-9]*[NS]:main400[EW][0-9]*[NS]',e1A)

    # XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    # PLAZA GRID
    # XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

    # Create the plaza grid in the center of the map
    ng.GenerateGrid(-50, -250, 50, 250, 50, 50, sntype, e1B, 'plaza')

    # The central north/south road is four lane
    ng.SetEdgeTypeByPattern('plaza[0-9]*[EW]100[NS]:plaza[0-9]*[EW]100[NS]',e2B)
    ng.SetEdgeTypeByPattern('plaza[0-9]*[EW]0N:plaza[0-9]*[EW]0N',e2B)
    ng.SetEdgeTypeByPattern('plaza0E[0-9]*[NS]:plaza0E[0-9]*[NS]',e2B)
    ng.SetEdgeTypeByPattern('plaza0E[0-9]*[NS]:plaza0E[0-9]*[NS]',e2B)

    # XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    # CONNECT THE GRIDS
    # XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

    # Create nodes at the north and south ends of the plaza
    ng.AddNode(0, -300, sntype, 'main') # south end of the plaza
    ng.AddNode(0, 300, sntype, 'main')  # north end of the plaza

    # And connect them to the east and west main grids
    ng.ConnectNodes(ng.gNodes['main100W300N'],ng.gNodes['main0E300N'],e2A)
    ng.ConnectNodes(ng.gNodes['main100E300N'],ng.gNodes['main0E300N'],e2A)
    ng.ConnectNodes(ng.gNodes['main100W300S'],ng.gNodes['main0E300S'],e2A)
    ng.ConnectNodes(ng.gNodes['main100E300S'],ng.gNodes['main0E300S'],e2A)

    # Connect the plaza nodes to the north & south ends
    ng.ConnectNodes(ng.gNodes['plaza0E250S'],ng.gNodes['main0E300S'],e2A)
    ng.ConnectNodes(ng.gNodes['plaza0E250N'],ng.gNodes['main0E300N'],e2A)

    # Connect the plaza nodes to the east and west roads
    ng.ConnectNodes(ng.gNodes['main100W100N'],ng.gNodes['plaza50W100N'],e2A)
    ng.ConnectNodes(ng.gNodes['main100W100S'],ng.gNodes['plaza50W100S'],e2A)
    ng.ConnectNodes(ng.gNodes['main100E100N'],ng.gNodes['plaza50E100N'],e2A)
    ng.ConnectNodes(ng.gNodes['main100E100S'],ng.gNodes['plaza50E100S'],e2A)
    ng.ConnectNodes(ng.gNodes['main100W0N'],ng.gNodes['plaza50W0N'],e2A)
    ng.ConnectNodes(ng.gNodes['main100E0N'],ng.gNodes['plaza50E0N'],e2A)

    # XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    # BUILD THE RESIDENTIAL NEIGHBORHOODS
    # XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

    rgenv = NetBuilder.ResidentialGenerator(e1C, dntype, edrv, rntype, bspace = 20, spacing = 10, driveway = 5)
    rgenh = NetBuilder.ResidentialGenerator(e1C, dntype, edrv, rntype, bspace = 40, spacing = 10)

    ng.GenerateResidential(ng.gNodes['main400W200S'],ng.gNodes['main400W100S'], rgenv)
    ng.GenerateResidential(ng.gNodes['main400W100S'],ng.gNodes['main400W0N'], rgenv)
    ng.GenerateResidential(ng.gNodes['main400W0N'],  ng.gNodes['main400W100N'], rgenv)
    ng.GenerateResidential(ng.gNodes['main400W100N'],ng.gNodes['main400W200N'], rgenv)

    ng.GenerateResidential(ng.gNodes['main400E200S'],ng.gNodes['main400E100S'], rgenv)
    ng.GenerateResidential(ng.gNodes['main400E100S'],ng.gNodes['main400E0N'], rgenv)
    ng.GenerateResidential(ng.gNodes['main400E0N'],  ng.gNodes['main400E100N'], rgenv)
    ng.GenerateResidential(ng.gNodes['main400E100N'],ng.gNodes['main400E200N'], rgenv)

    ng.GenerateResidential(ng.gNodes['main300W400N'],ng.gNodes['main200W400N'], rgenv)
    ng.GenerateResidential(ng.gNodes['main200W400N'],ng.gNodes['main100W400N'], rgenv)

    ng.GenerateResidential(ng.gNodes['main300W400S'],  ng.gNodes['main200W400S'], rgenv)
    ng.GenerateResidential(ng.gNodes['main200W400S'],  ng.gNodes['main100W400S'], rgenv)

    ng.GenerateResidential(ng.gNodes['main300E400N'],ng.gNodes['main200E400N'], rgenv)
    ng.GenerateResidential(ng.gNodes['main200E400N'],ng.gNodes['main100E400N'], rgenv)

    ng.GenerateResidential(ng.gNodes['main300E400S'],ng.gNodes['main200E400S'], rgenv)
    ng.GenerateResidential(ng.gNodes['main200E400S'],ng.gNodes['main100E400S'], rgenv)

    rgenv.BothSides = False
    ng.GenerateResidential(ng.gNodes['main300W200N'],ng.gNodes['main400W200N'], rgenv)
    ng.GenerateResidential(ng.gNodes['main300E200N'],ng.gNodes['main400E200N'], rgenv)

    rgenv.DrivewayLength = - rgenv.DrivewayLength
    ng.GenerateResidential(ng.gNodes['main400W200S'],ng.gNodes['main300W200S'], rgenv)
    ng.GenerateResidential(ng.gNodes['main400E200S'],ng.gNodes['main300E200S'], rgenv)

    # XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    # BUILD THE BUSINESS NEIGHBORHOODS
    # XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

    # Time to build out some tiles... starting with simple parking lots, do not render
    # with OpenSim
    rgenplR = NetBuilder.ResidentialGenerator(plotentry, plotnode, plotdrive, bntype, driveway = 8, bspace = 5, spacing = 5, both = False)
    rgenplL = NetBuilder.ResidentialGenerator(plotentry, plotnode, plotdrive, bntype, driveway = -8, bspace = 5, spacing = 5, both = False)

    for n in ['main300W200S', 'main200W200S', 'main100E200S', 'main200E200S'] :
        ng.BuildSimpleParkingLotEW(ng.gNodes[n], pntype, rgenplR, "tile", offset=15)
        ng.BuildSimpleParkingLotEW(ng.gNodes[n], pntype, rgenplL, "tile", offset=-15)

    for n in ['main300W200N', 'main200W200N', 'main100E200N', 'main200E200N'] :
        ng.BuildSimpleParkingLotEW(ng.gNodes[n], pntype, rgenplR, "tile", offset=15)
        ng.BuildSimpleParkingLotEW(ng.gNodes[n], pntype, rgenplL, "tile", offset=-15)

    for n in ['plaza50W250S', 'plaza50W200S', 'plaza50W150S', 'plaza50W100S', 'plaza50W50S' ] :
        ng.BuildSimpleParkingLotNS(ng.gNodes[n], pntype, rgenplL, "tile", offset=15, slength = 17.5, elength=32.5)

    for n in ['plaza50W0N', 'plaza50W50N', 'plaza50W100N', 'plaza50W150N', 'plaza50W200N' ] :
        ng.BuildSimpleParkingLotNS(ng.gNodes[n], pntype, rgenplL, "tile", offset=15, slength = 17.5, elength=32.5)

    for n in ['plaza50E250S', 'plaza50E200S', 'plaza50E150S', 'plaza50E100S', 'plaza50E50S'] :
        ng.BuildSimpleParkingLotNS(ng.gNodes[n], pntype, rgenplR, "tile", offset=-15, slength = 17.5, elength=32.5)

    for n in ['plaza50E0N', 'plaza50E50N', 'plaza50E100N', 'plaza50E150N', 'plaza50E200N'] :
        ng.BuildSimpleParkingLotNS(ng.gNodes[n], pntype, rgenplR, "tile", offset=-15, slength = 17.5, elength=32.5)
        
    # for n in ['main200W300S', 'main200W200S', 'main200W100S', 'main200W0N', 'main200W100N', 'main200W200N'] : 
    #     ng.BuildSimpleParkingLot(ng.gNodes[n], pntype, rgenplR, "tile", offset=15)
    #     ng.BuildSimpleParkingLot(ng.gNodes[n], pntype, rgenplL, "tile", offset=-15)

    # for n in ['main200E300S', 'main200E200S', 'main200E100S', 'main200E0N', 'main200E100N', 'main200E200N'] : 
    #     ng.BuildSimpleParkingLot(ng.gNodes[n], pntype, rgenplR, "tile", offset=15)
    #     ng.BuildSimpleParkingLot(ng.gNodes[n], pntype, rgenplL, "tile", offset=-15)

    # ng.GenerateResidential(ng.gNodes['main400W200S'],ng.gNodes['main300W200S'], rgenh)
    # ng.GenerateResidential(ng.gNodes['main400W0N'],  ng.gNodes['main300W0N'], rgenh)
    # ng.GenerateResidential(ng.gNodes['main400W200N'],ng.gNodes['main300W200N'], rgenh)

    # ng.GenerateResidential(ng.gNodes['main400E200S'],ng.gNodes['main300E200S'], rgenh)
    # ng.GenerateResidential(ng.gNodes['main400E0N'],  ng.gNodes['main300E0N'], rgenh)
    # ng.GenerateResidential(ng.gNodes['main400E200N'],ng.gNodes['main300E200N'], rgenh)

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
BuildNetwork(netgen)
print "Loaded fullnet builder extension file"
