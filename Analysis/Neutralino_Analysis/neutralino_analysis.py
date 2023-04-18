'''
Author: Mohamed Elashri
date: 2022-08-02
Usage: lb-run DaVinci/v45r8 python3 -i neutralino_analysis.py
'''

# # import python packages
import sys
import pdb
import numpy as np
from array import array
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Import HEP/LHCb
import ROOT
from ROOT import gROOT, gStyle, TCanvas, TFile, TTree, TH1F, TH2F, TH3F, TH1D, TH2D, TH3D
import GaudiPython
from GaudiConf import IOHelper
from Configurables import DaVinci
from Configurables import CombineParticles
from Configurables import ApplicationMgr 

''' 
from glob import glob
for file in glob("*.sim"):
    IOHelper('ROOT').inputFiles([file], clear=True)   
'''
#datafile = '/afs/cern.ch/work/m/melashri/public/SUSY/MC/Sim10/Gauss_Dev/GaussDev_v55r4/analysis/data/Stau_100GeV_100n_10000mm_ctau_with_Cut.sim'

datafile = '/afs/cern.ch/work/m/melashri/public/SUSY/MC/Sim10/Gauss_Dev/GaussDev_v55r4/Neutralino.sim'
IOHelper().inputFiles([
    datafile
], clear=True)

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


# Configure GaudiPythone
gaudi = GaudiPython.AppMgr()
tes   = gaudi.evtsvc()
# let gaudi loop and run over all events
gaudi.run(1)  

n_neutralino = 0
n_neutralino_in_acc = 0
n_muons_from_neutralino = 0
n_amuons_from_neutralino = 0     
n_muons = 0
n_amuons = 0                 
evtmax = 19
processed = 0





while processed < evtmax:
#while bool(tes['/Event']) and processed < evtmax:
    processed += 1
    gaudi.run(1)
    particles = tes['MC/Particles']
    pid_list = [particle.particleID().pid() for particle in particles]
    print("Event number: ", processed)
       
    for particle in particles: 
        if particle.particleID().pid() == 1000022:
            n_neutralino += 1        
            print("The particle is an neutralino-")
            print("The particle ID is",particle.particleID().pid())
            print("The particle Mass is",particle.momentum().mass())
            print("Particle momentum is", particle.momentum().pt())
            print("Primary Vertex is",particle.primaryVertex().position4vector())   
            print("Origin Vertex is",particle.originVertex().position4vector())
            print("Particle eta is",particle.momentum().eta())
            if particle.momentum().eta() > 1.9 and particle.momentum().eta() < 5.1:
                n_neutralino_in_acc += 1
            # Get information on how long the particle has been in the detector
            
                      
        if particle.particleID().pid() == 13:
            n_muons += 1
            '''
            print("The particle is muon-")
            print("The particle ID is",particle.particleID().pid())
            print("The particle Mass is",particle.momentum().mass())
            print("Primary Vertex is",particle.primaryVertex().position4vector())   
            print("Origin Vertex is",particle.originVertex().position4vector())
            print("Particle mother pid is",particle.mother())
            '''
        if particle.particleID().pid() == -13:
            n_amuons += 1
            '''
            print("The particle is muon+")
            print("The particle ID is",particle.particleID().pid())
            print("The particle Mass is",particle.momentum().mass())
            print("Primary Vertex is",particle.primaryVertex().position4vector())   
            print("Origin Vertex is",particle.originVertex().position4vector())
            print("Particle mother pid is",particle.mother())
            '''
        # check for muons that results from neutralino
        if particle and particle.particleID() and particle.mother() and particle.mother().particleID():
            if particle.particleID().pid() == 13 and particle.mother().particleID().pid() == 1000022:
                n_muons_from_neutralino += 1

        if particle and particle.particleID() and particle.mother() and particle.mother().particleID():
            if particle.particleID().pid() == -13 and particle.mother().particleID().pid() == 1000022:
                n_amuons_from_neutralino += 1
            
print("Total number of neutralinos is",n_neutralino)
print("Total number of neutralinos in acceptance is",n_neutralino_in_acc)
print("Total number of muons is",n_muons)
print("Total number of anti-muons is",n_amuons)
print("Total number of muons from neutralinos is",n_muons_from_neutralino)
print("Total number of anti-muons from neutralinos is",n_amuons_from_neutralino)

# Create a histogram of the number of each particle type in the event

# Data
labels = [
    "neutralino",
    "neutralino InAcce",
    "muons-",
    "muons+",
    "muon- from neutralino",
    "muos+ from neutralino",
]
values = [
    n_neutralino,
    n_neutralino_in_acc,
    n_muons,
    n_amuons,
    n_muons_from_neutralino,
    n_amuons_from_neutralino,
]

# Bar plot
fig, ax = plt.subplots(figsize=(12, 6))
bars = plt.bar(range(len(values)), values)
plt.xticks(range(len(labels)), labels, rotation=45, ha='right')

# Add the actual values on top of the bars
for bar, value in zip(bars, values):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), value, ha='center', va='bottom')

# Axis labels and title
plt.xlabel('Particles')
plt.ylabel('Number of particles')
# Add legends that this is for 100 Events in Gauss
plt.legend(['100 Events in Gauss'])
plt.title('Number of particles in the events')

# Save the figure
plt.savefig('figs/neutralino/n_particles_hist.pdf', bbox_inches='tight')
