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
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


LHCbApp().Simulation = True
IOHelper().inputFiles(['/afs/cern.ch/work/m/melashri/public/SUSY/MC/Sim10/Gauss_Dev/GaussDev_v55r4/analysis/data/Stau_100GeV_100n_vshort_tau_with_Cut.sim'], clear=True)

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
gaudi = GaudiPython.AppMgr()
evtmax = 95
processed = 0
total_velo_hits = 0
total_it_hits = 0
total_ot_hits = 0
total_muon_hits = 0
total_rich_hits = 0
total_tt_hits = 0
stau_hit_count = 0
tau_hit_count = 0
pi_hit_count = 0
proton_hit_count = 0
muons_hit_count = 0
velo_muon_hit_count = 0
tt_muon_hit_count = 0
it_muon_hit_count = 0
ot_muon_hit_count = 0
muon_muon_hit_count = 0
rich_muon_hit_count = 0
total_hits = 0
interesting_muon_hit_count= 0
while processed < evtmax:
    processed += 1
    gaudi.run(1)
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
        # Iterate over the MCHits
        for mchit in mchits: # Inner loop 2: iterate over the MCHits within a specific subdetector
            mcparticle = mchit.mcParticle()
            particle_id = mcparticle.particleID().pid()
            
            
            # Check total hits in each subdetector
            if location == "/Event/MC/Velo/Hits":
                total_velo_hits += 1
            elif location == "/Event/MC/TT/Hits":
                total_tt_hits += 1    
            elif location == "/Event/MC/IT/Hits":
                total_it_hits += 1
            elif location == "/Event/MC/OT/Hits":
                total_ot_hits += 1
            elif location == "/Event/MC/Muon/Hits":
                total_muon_hits += 1
            elif location == "/Event/MC/Rich/Hits":
                total_rich_hits += 1
                
            # Calculate total hits in all subdetectors    
            total_hits = total_velo_hits + total_tt_hits + total_it_hits + total_ot_hits + total_muon_hits + total_rich_hits
            
            # Check for hits from specific particles                    
            if particle_id == 1000015 or particle_id == -1000015:
                stau_hit_count += 1
            if particle_id == 15 or particle_id == -15:
                tau_hit_count += 1    
            if particle_id == -211 or particle_id == 211:
                pi_hit_count += 1   
            if particle_id == 2212 or particle_id == -2212:
                proton_hit_count += 1    
            if particle_id == 13 or particle_id == -13:
                muons_hit_count += 1    
            ## Now check for which subdetector this muon hit belongs to
                if location == "/Event/MC/Velo/Hits":
                    velo_muon_hit_count += 1
                elif location == "/Event/MC/TT/Hits":
                    tt_muon_hit_count += 1
                elif location == "/Event/MC/IT/Hits":
                    it_muon_hit_count += 1
                elif location == "/Event/MC/OT/Hits":
                    ot_muon_hit_count += 1
                elif location == "/Event/MC/Muon/Hits":
                    muon_muon_hit_count += 1
                elif location == "/Event/MC/Rich/Hits":
                    rich_muon_hit_count += 1
                # Now we want to see hits from muons which are decay products of taus
                mother = mcparticle.mother()
                if mother:
                    mother_id = mother.particleID().pid()
                    if mother_id == 15 or mother_id == -15:
                        interesting_muon_hit_count += 1
                            
print("Total number of Velo hits: ", total_velo_hits)
print("Total number of TT hits: ", total_tt_hits)
print("Total number of IT hits: ", total_it_hits)
print("Total number of OT hits: ", total_ot_hits)
print("Total number of Muon hits: ", total_muon_hits)
print("Total number of Rich hits: ", total_rich_hits)
print("Total number of hits: ", total_hits)
print("Number of Stau hits: ", stau_hit_count)
print("Number of Tau hits: ", tau_hit_count)
print("Number of Pi hits: ", pi_hit_count)
print("Number of Proton hits: ", proton_hit_count)
print("Number of Muons hits: ", muons_hit_count)
print("Number of interesting Muon hits (tau decys): ", interesting_muon_hit_count)
print("Number of Muon Velo hits: ", velo_muon_hit_count)
print("Number of Muon TT hits: ", tt_muon_hit_count)
print("Number of Muon IT hits: ", it_muon_hit_count)
print("Number of Muon OT hits: ", ot_muon_hit_count)
print("Number of Muon Rich hits: ", rich_muon_hit_count)
print("Number of Muon chamber Muon hits: ", muon_muon_hit_count)


# Create histogram plot of the number of hits in each subdetector
subdetectors = ["Velo", "TT", "IT", "OT", "Muon", "Rich"]
hits = [total_velo_hits, total_tt_hits, total_it_hits, total_ot_hits, total_muon_hits, total_rich_hits]
plt.figure()  # Add this line to create a new figure
plt.bar(subdetectors, hits, width=0.5, color="blue")
plt.xlabel("Subdetector")
plt.ylabel("Number of hits")
plt.yscale('log')
plt.title("Number of hits in each subdetector")
plt.savefig("figs/pv_ctau_stau/hits_in_each_subdetector.png")

# Create histogram plot of the number of hits from each particle
particles = ["Stau", "Tau", "Muons"]
hits = [stau_hit_count, tau_hit_count, interesting_muon_hit_count]
plt.figure()  # Add this line to create a new figure
plt.bar(particles, hits, width=0.5, color="red")
plt.xlabel("Particle")
plt.ylabel("Number of hits")
plt.yscale('log')
plt.title("Number of hits from each particle")
plt.savefig("figs/pv_ctau_stau/hits_from_each_particle.png")
pdb.set_trace()
