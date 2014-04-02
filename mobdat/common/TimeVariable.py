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

@file    TimeVariable.py
@author  Mic Bowman
@date    2014-03-31

This package defines modules for the mobdat simulation environment

"""

import os, sys
import logging

# we need to import python modules from the $SUMO_HOME/tools directory
sys.path.append(os.path.join(os.environ.get("OPENSIM","/share/opensim"),"lib","python"))
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "lib")))

import random
from mobdat.common.Utilities import GenName

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class TimeVariable :
    Priority = 5

    # -----------------------------------------------------------------
    def __init__(self, stime, etime = None, id = None) :
        """ Create a variable to use for time constraints

        Args:
            stime -- float, the interval start time
            etime -- float, the interval end time
            id -- unique identifier for the time variable
        """

        self.STime = min(stime, etime or stime)
        self.ETime = max(stime, etime or stime)
        self.ID = id or GenName('TV')

    # -----------------------------------------------------------------
    def __str__(self) :
        fmt = "{0}:{1:.3f}" if self.IsFixed() else "{0}:<{1:.3f}-{2:.3f}>" 
        return fmt.format(self.ID, self.STime, self.ETime)

    # -----------------------------------------------------------------
    def Copy(self, id = None) :
        """ Create a copy of the time variable """
        ## return TimeVariable(self.STime, self.ETime, self.ID)
        return self.__class__(self.STime, self.ETime, id or self.ID)

    # -----------------------------------------------------------------
    def IsFixed(self) :
        """ Predicate to determine if the interval has set a single value """
        return self.STime == self.ETime

    # -----------------------------------------------------------------
    def IsValid(self) :
        """ Predicate to determine if the interval has any valid values """
        return self.STime <= self.ETime
    
    # -----------------------------------------------------------------
    def PickValue(self) :
        return self.SetValue(random.uniform(self.STime, self.ETime))

    # -----------------------------------------------------------------
    def SetValue(self, value) :
        """ Fix the time interval to a single value

        Args:
            time -- a value in the interval
        Returns:
            the fixed value of the variable
        """
        self.STime = value
        self.ETime = value
        return value

    # -----------------------------------------------------------------
    def GetValue(self) :
        return self.STime if self.IsFixed() else None

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class GaussianTimeVariable(TimeVariable) :
    Priority = 5

    # -----------------------------------------------------------------
    def __init__(self, stime, etime, id = None) :
        TimeVariable.__init__(self, stime, etime, id)

    # -----------------------------------------------------------------
    def PickValue(self) :
        mean = (self.STime + self.ETime) / 2.0
        stdev = (self.ETime - self.STime) / 4.0
        value = max(self.STime, min(self.ETime, random.gauss(mean, stdev)))

        return self.SetValue(value)

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class MinimumTimeVariable(TimeVariable) :
    Priority = 0

    # -----------------------------------------------------------------
    def __init__(self, stime, etime, id = None) :
        TimeVariable.__init__(self, stime, etime, id)

    # -----------------------------------------------------------------
    def PickValue(self) :
        return self.SetValue(self.STime)

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class MaximumTimeVariable(TimeVariable) :
    Priority = 0

    # -----------------------------------------------------------------
    def __init__(self, stime, etime, id = None) :
        TimeVariable.__init__(self, stime, etime, id)

    # -----------------------------------------------------------------
    def PickValue(self) :
        return self.SetValue(self.ETime)


