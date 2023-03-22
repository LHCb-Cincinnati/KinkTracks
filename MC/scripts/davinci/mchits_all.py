'''
Name: mchits_all.py
Description: This is a simple example to show how to access the MCHits containers for all subdetectors (expect Calorimeters) in a `.sim` file.
Then, it prints the number of MCHits that belongs to staus for each subdetector.
Author: Mohamed Elashri
Date: 2023-03-20
Usage: lb-run DaVinci/v45r8 python3 -i mchits_all.py
'''



from Gaudi.Configuration import *
from GaudiConf import IOHelper
from Configurables import LHCbApp, ApplicationMgr, GaudiSequencer
from Configurables import DaVinci, DecodeRawEvent, RawEventFormatConf, UnpackMCParticle, UnpackMCVertex
import GaudiPython

import pdb

LHCbApp().Simulation = True
IOHelper().inputFiles(['/afs/cern.ch/work/m/melashri/public/SUSY/MC/Sim10/Gauss_Dev/GaussDev_v55r4/Stau_100GeV_100n_long_tau.sim'], clear=True)

# Configure DaVinci
DaVinci().Simulation = True
DaVinci().Lumi = False
DaVinci().DataType = '2017'
DaVinci().InputType = 'DIGI'
DaVinci().EvtMax = -1
DaVinci().DDDBtag = 'dddb-20210215-6'

# for the event loop                                                                                                     
from Configurables import EventSelector
EventSelector().PrintFreq = 1000

from Gaudi.Configuration import appendPostConfigAction
def doIt():
    """
    specific post-config action for (x)GEN-files 
    """
    extension = "sim"
    ext = extension.upper()

    from Configurables import DataOnDemandSvc
    dod  = DataOnDemandSvc ()
    from copy import deepcopy 
    algs = deepcopy ( dod.AlgMap ) 
    bad  = set() 
    for key in algs :
        if     0 <= key.find ( 'Rec'     )                  : bad.add ( key )
        elif   0 <= key.find ( 'Raw'     )                  : bad.add ( key )
        elif   0 <= key.find ( 'DAQ'     )                  : bad.add ( key )
        elif   0 <= key.find ( 'Trigger' )                  : bad.add ( key )
        elif   0 <= key.find ( 'Phys'    )                  : bad.add ( key )
        elif   0 <= key.find ( 'Prev/'   )                  : bad.add ( key )
        elif   0 <= key.find ( 'Next/'   )                  : bad.add ( key )
        elif   0 <= key.find ( '/MC/'    ) and 'GEN' == ext : bad.add ( key )
        
    for b in bad :
        del algs[b]
            
    dod.AlgMap = algs
    
    from Configurables import EventClockSvc, CondDB 
    EventClockSvc ( EventTimeDecoder = "FakeEventTime" )
    CondDB  ( IgnoreHeartBeat = True )
    
appendPostConfigAction( doIt )



appMgr = GaudiPython.AppMgr()
appMgr.config()
appMgr.initialize()

# Get the event service
evtSvc = appMgr.evtsvc()




for i in range(100):   # Outer loop: iterate through the number of events we want to process
    appMgr.run(1)  
    
    # Get the MCHits containers for all subdetectors (expect Calorimeters)
    mchits_locations = [
    "/Event/MC/Velo/Hits",
    "/Event/MC/TT/Hits",
    "/Event/MC/IT/Hits",
    "/Event/MC/OT/Hits",
    "/Event/MC/Muon/Hits",
    "/Event/MC/Rich/Hits"
]

    
    for location in mchits_locations: # Inner loop 1: iterate through the MCHits locations for each subdetector
        mchits = evtSvc[location]  # get the MCHits container for the subdetector
        stau_hit_count = 0
        tau_hit_count = 0
        pi_hit_count = 0
        proton_hit_count = 0
        # Iterate over the MCHits
        for mchit in mchits: # Inner loop 2: iterate over the MCHits within a specific subdetector
            mcparticle = mchit.mcParticle()
            particle_id = mcparticle.particleID().pid()

            if particle_id == 1000015 or particle_id == -1000015:
                stau_hit_count += 1
            if particle_id == 15 or particle_id == -15:
                tau_hit_count += 1    
            if particle_id == -211 or particle_id == 211:
                pi_hit_count += 1   
            if particle_id == 2212 or particle_id == -2212:
                proton_hit_count += 1    

print("Number of Stau hits: ", stau_hit_count)
print("Number of Tau hits: ", tau_hit_count)
print("Number of Pi hits: ", pi_hit_count)
print("Number of Proton hits: ", proton_hit_count)
pdb.set_trace()        
