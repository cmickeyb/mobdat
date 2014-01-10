mobdat
======

Mobdat is a simulator used to generate mobility data for people. Mobdat
combines traffic simulation from the SUMO traffic simulator
(http://sumo-sim.org/), OpenSim 3D application platform
(http://opensimulator.org/wiki/Main_Page), and an agent-based social
simulator. 

The following packages need to be installed to run mobdat:

* Python 2.7
  - The pymongo package is required for the BSON encoder, see
  installation instructions at https://pypi.python.org/pypi/pymongo/

* SUMO 0.19

* OpenSim 
  - JsonStore must be turned on, instructions for configuring the
  JsonStore can be found at http://opensimulator.org/wiki/JsonStore_Module 
  - The scisim-addons package is also required, this can be retrieved
  from https://github.com/cmickeyb/scisim-addons, enable the dispatcher
  and remote control modules.



