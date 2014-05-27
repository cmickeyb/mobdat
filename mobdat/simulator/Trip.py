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

@file    Trip.py
@author  Mic Bowman
@date    2014-04-02

This module defines the SocialConnector class. This class implements
the social (people) aspects of the mobdat simulation.

"""

import os, sys
import logging

sys.path.append(os.path.join(os.environ.get("SUMO_HOME"), "tools"))
sys.path.append(os.path.join(os.environ.get("OPENSIM","/share/opensim"),"lib","python"))
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "lib")))

import random
from mobdat.common.Utilities import GenName

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class Trip :
    # -----------------------------------------------------------------
    def __init__(self, traveler, stime, source, destination) :
        self.Traveler = traveler
        self.StartTime = stime
        self.Source = source
        self.Destination = destination

        self.VehicleType = self.Traveler.Person.Vehicle.VehicleType
        self.VehicleName = GenName('trip')
        #self.VehicleName = self.Traveler.Person.Vehicle.VehicleName

    # -----------------------------------------------------------------
    def TripCompleted(self, connector) :
        connector.GenerateTripStatsEvent(self)
        self.Traveler.TripCompleted(self, connector)

    # -----------------------------------------------------------------
    def TripStarted(self, connector) :
        self.Traveler.TripStarted(self, connector)
        connector.GenerateAddVehicleEvent(self)

    # -----------------------------------------------------------------
    def __cmp__(self, other) :
        return cmp(self.StartTime, other.StartTime)

