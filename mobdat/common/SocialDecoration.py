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

@file    SocialDecoration.py
@author  Mic Bowman
@date    2013-12-03

This file defines routines used to build features of a mobdat traffic
network such as building a grid of roads. 

"""

import os, sys

# we need to import python modules from the $SUMO_HOME/tools directory
sys.path.append(os.path.join(os.environ.get("OPENSIM","/share/opensim"),"lib","python"))
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "lib")))

from mobdat.common.Business import Business, BusinessProfile, JobProfile
from mobdat.common.Decoration import Decoration

## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class JobProfileDecoration(Decoration) :
    DecorationName = 'JobProfile'
    
    # -----------------------------------------------------------------
    @staticmethod
    def Load(graph, info) :
        jobprofile = JobProfile.Load(info['JobProfile'])
        return JobProfileDecoration(jobprofile)

    # -----------------------------------------------------------------
    def __init__(self, jobprofile) :
        """
        Args:
            jobprofile -- an object of type Business.JobProfile
        """
        Decoration.__init__(self)
        self.JobProfile = jobprofile

    # -----------------------------------------------------------------
    def __getattr__(self, name) :
            return getattr(self.JobProfile, name)

    # -----------------------------------------------------------------
    def Dump(self) :
        result = Decoration.Dump(self)
        result['JobProfile'] = self.JobProfile.Dump()
        
        return result
    
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class BusinessProfileDecoration(Decoration) :
    DecorationName = 'BusinessProfile'
    
    # -----------------------------------------------------------------
    @staticmethod
    def Load(graph, info) :
        profile = BusinessProfile.Load(info['BusinessProfile'])
        return BusinessProfileDecoration(profile)

    # -----------------------------------------------------------------
    def __init__(self, profile) :
        """
        Args:
            profile -- an object of type Business.BusinessProfile
        """
        Decoration.__init__(self)
        self.BusinessProfile = profile

    # -----------------------------------------------------------------
    def __getattr__(self, name) :
            return getattr(self.BusinessProfile, name)

    # -----------------------------------------------------------------
    def Dump(self) :
        result = Decoration.Dump(self)
        result['BusinessProfile'] = self.BusinessProfile.Dump()
        
        return result
    
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class BusinessDecoration(Decoration) :
    DecorationName = 'Business'
    
    # -----------------------------------------------------------------
    @staticmethod
    def Load(graph, info) :
        employer = Business.Load(info['Business'])
        return BusinessDecoration(employer)

    # -----------------------------------------------------------------
    def __init__(self, business) :
        """
        Args:
            business -- an object of type Business.Business
        """
        Decoration.__init__(self)
        self.Business = business

    # -----------------------------------------------------------------
    def __getattr__(self, name) :
            return getattr(self.Business, name)

    # -----------------------------------------------------------------
    def Dump(self) :
        result = Decoration.Dump(self)
        result['Business'] = self.Business.Dump()
        
        return result
    
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class ResidenceDecoration(Decoration) :
    DecorationName = 'Residence'
    
    # -----------------------------------------------------------------
    @staticmethod
    def Load(graph, info) :
        return ResidenceDecoration(info['LocationName'], info['EndPointName'])

    # -----------------------------------------------------------------
    def __init__(self, location, endpoint) :
        """
        Args:
            location -- LayoutInfo.ResidentialLocation
            endpoint -- LayoutInfo.EndPoint
        """
        Decoration.__init__(self)
        self.LocationName = location.Name
        self.EndPointName = endpoint.Name

    # -----------------------------------------------------------------
    def __getattr__(self, name) :
            return self.Residence.__dict__[name]

    # -----------------------------------------------------------------
    def Dump(self) :
        result = Decoration.Dump(self)
        result['LocationName'] = self.LocationName
        result['EndPointName'] = self.EndPointName
        
        return result
    
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
## XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
CommonDecorations = [ JobProfileDecoration, BusinessProfileDecoration, BusinessDecoration, ResidenceDecoration ]

