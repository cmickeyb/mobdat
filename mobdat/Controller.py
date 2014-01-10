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

@file    Controller.py
@author  Mic Bowman
@date    2013-12-03

This module defines routines for controling the mobdat simulator. The controller
sets up the connectors and then drives the simulation through the periodic
clock ticks.

"""

import os, sys, warnings

sys.path.append(os.path.join(os.environ.get("OPENSIM","/share/opensim"),"lib","python"))
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "lib")))

import time
import EventRegistry, EventTypes, ValueTypes
import platform

# -----------------------------------------------------------------
# -----------------------------------------------------------------
import SumoConnector, OpenSimConnector, SocialConnector
_SimulationControllers = {
    'sumo' : SumoConnector.SumoConnector,
    'opensim' : OpenSimConnector.OpenSimConnector,
    'social' : SocialConnector.SocialConnector
    }

# -----------------------------------------------------------------
# -----------------------------------------------------------------
def _RunSimulation(evhandler, interval, lastiteration) :
    """
    Run the simulation by sending the periodic clock ticks that each of the connectors
    can process.

    Arguments:
    evhandler -- the initialized event handler object
    interval -- time between successive clock ticks
    lastiteration -- number of iterations
    """

    clk = time.time

    ## this is an ugly hack because the cygwin and linux
    ## versions of time.clock seem seriously broken
    if platform.system() == 'Windows' :
        clk = time.clock

    starttime = clk()

    iterations = 0
    while iterations < lastiteration :
        stime = clk()

        event = EventTypes.TimerEvent(iterations, stime)
        evhandler.PublishEvent(event)

        etime = clk()

        if (etime - stime) < interval :
            # print "sleep %f seconds" % (interval - (etime - stime))
            time.sleep(interval - (etime - stime))

        iterations += 1

    elapsed = clk() - starttime
    avginterval = 1000.0 * elapsed / iterations
    print "%d iterations completed with an elapsed time %f or %f ms per iteration" % (iterations, elapsed, avginterval)

# -----------------------------------------------------------------
# -----------------------------------------------------------------
def Controller(settings) :
    """
    Controller is the main entry point for driving the simulation.

    Arguments:
    settings -- nested dictionary with variables for configuring the connectors
    """

    interval = float(settings["General"]["Interval"])
    cnames = settings["General"].get("Connectors",['sumo', 'opensim', 'social'])

    evhandler = EventRegistry.EventRegistry()

    # initialize the connectors first
    connectors = []
    for cname in cnames :
        if cname not in _SimulationControllers :
            warnings.warn('skipping unknown simulation connector; %s' % (cname))
            continue

        connectors.append(_SimulationControllers[cname](evhandler, settings))
            
    # and start the connectors
    for connector in connectors :
        connector.SimulationStart()

    # and run the simulation through all its iterations
    lastiteration = settings["General"]["TimeSteps"]
    try :
        _RunSimulation(evhandler, interval, lastiteration)
    except :
        warnings.warn('[controller] error occured during simulation, shutting down; %s' % (sys.exc_info()[0]))
    finally :
        # and finally shut down the connectors
        for connector in connectors :
            connector.SimulationStop()
        sys.exit(-1)
            
