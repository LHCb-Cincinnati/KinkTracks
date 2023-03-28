'''
Author: Mohamed Elashri
date: 2022-08-02
Usage: lb-run DaVinci/v45r8 python3 -i analysis.py
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
datafile = '<file_name>.sim'

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

n_stau = 0
n_stau_in_acc = 0
n_a_stau = 0
n_a_stau_in_acc = 0
n_gravitino = 0
n_tau = 0
n_taus_in_acc = 0
n_ataus_in_acc = 0
n_a_tau = 0
n_taus_from_staus = 0
n_a_taus_from_staus = 0
n_muons_from_taus = 0
n_amuons_from_taus = 0     
n_muons = 0
n_amuons = 0                 
evtmax = 99
processed = 0





while processed < evtmax:
#while bool(tes['/Event']) and processed < evtmax:
    processed += 1
    gaudi.run(1)
    particles = tes['MC/Particles']
    pid_list = [particle.particleID().pid() for particle in particles]
    print("Event number: ", processed)
       
    for particle in particles: 
        if particle.particleID().pid() == 1000015:
            n_stau += 1        
            print("The particle is an stau-")
            print("The particle ID is",particle.particleID().pid())
            print("The particle Mass is",particle.momentum().mass())
            print("Particle momentum is", particle.momentum().pt())
            print("Primary Vertex is",particle.primaryVertex().position4vector())   
            print("Origin Vertex is",particle.originVertex().position4vector())
            print("Particle eta is",particle.momentum().eta())
            if particle.momentum().eta() > 1.9 and particle.momentum().eta() < 5.1:
                n_stau_in_acc += 1
            # Get information on how long the particle has been in the detector
            
       
        if particle.particleID().pid() == -1000015:
            n_a_stau += 1 
            print("The particle is a stau+")
            print("The particle ID is",particle.particleID().pid())
            print("The particle Mass is",particle.momentum().mass())
            print("Particle momentum is", particle.momentum().pt())
            print("Primary Vertex is",particle.primaryVertex().position4vector())   
            print("Origin Vertex is",particle.originVertex().position4vector())
            print("Particle eta is",particle.momentum().eta())
            if particle.momentum().eta() > 1.9 and particle.momentum().eta() < 5.1:
                n_a_stau_in_acc += 1

        if particle.particleID().pid() == 15:
            n_tau += 1
            print("The particle is a tau-")
            print("The particle ID is",particle.particleID().pid())
            print("The particle Mass is",particle.momentum().mass())
            print("Primary Vertex is",particle.primaryVertex().position4vector())   
            print("Origin Vertex is",particle.originVertex().position4vector())
            print("Particle mother pid is",particle.mother())
            print("Particle eta is",particle.momentum().eta())
            # check if the tau is in LHCb acceptance 
            if particle.momentum().eta() > 1.9 and particle.momentum().eta() < 5.1:
                n_taus_in_acc += 1
            if particle.originVertex().isDecay() == True:
               print("The particle is a decay product")
            else:
               print("The particle is a primary particle")
               

        if particle.particleID().pid() == -15:
            n_a_tau += 1
            print("The particle is a tau+")
            print("The particle ID is",particle.particleID().pid())
            print("The particle Mass is",particle.momentum().mass())
            print("Primary Vertex is",particle.primaryVertex().position4vector())   
            print("Origin Vertex is",particle.originVertex().position4vector())
            print("Particle mother pid is",particle.mother())
            print("Particle eta is",particle.momentum().eta())
            if particle.momentum().eta() > 1.9 and particle.momentum().eta() < 5.1:
                n_ataus_in_acc += 1
            
            if particle.originVertex().isDecay() == True:
               print("The particle is a decay product")
            else:
               print("The particle is a primary particle")
          
        if particle.particleID().pid() == 1000039:
            n_gravitino += 1
            print("The particle is Gravitino")
            print("The particle ID is",particle.particleID().pid())
            print("The particle Mass is",particle.momentum().mass())
            print("Primary Vertex is",particle.primaryVertex().position4vector())   
            print("Origin Vertex is",particle.originVertex().position4vector())
            print("Particle mother pid is",particle.mother())
            if particle.originVertex().isDecay() == True:
               print("The particle is a decay product")
            else:
               print("The particle is a primary particle")
               
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
        # check for muons that results from tau decays
        if particle.particleID().pid() == 13:
            mother = particle.mother()
            if mother and mother.particleID().pid() == 15:
                n_muons_from_taus += 1
        if particle.particleID().pid() == -13:
            mother = particle.mother()
            if mother and mother.particleID().pid() == -15:
                n_amuons_from_taus += 1               
        # check how many taus are result from staus decays (both staus and anti-staus)
        if particle.particleID().pid() == 15:
            mother = particle.mother()
            if mother and mother.particleID().pid() == 1000015:
                # get the particles index for this particle from particles = tes['MC/Particles'] container
                print("The tau- particle index is",particles.index(particle))
                n_taus_from_staus += 1
        if particle.particleID().pid() == -15:
            mother = particle.mother()
            if mother and mother.particleID().pid() == -1000015:
                print("The tau+ particle index is",particles.index(particle))
                n_a_taus_from_staus += 1
            
print("Total number of staus is",n_stau)
print("Total number of staus in acceptance is",n_stau_in_acc)
print("Total number of anti-staus is",n_a_stau)
print("Total number of anti-staus in acceptance is",n_a_stau_in_acc)
print("Total number of taus is",n_tau)
print("Total number of taus in acceptance is",n_taus_in_acc)
print("Total number of taus from staus is",n_taus_from_staus)
print("Total number of anti-taus is",n_a_tau)
print("Total number of anti-taus in acceptance is",n_ataus_in_acc)
print("Total number of anti-taus from anti-staus is",n_a_taus_from_staus)
print("Total number of muons is",n_muons)
print("Total number of anti-muons is",n_amuons)
print("Total number of muons from taus is",n_muons_from_taus)
print("Total number of anti-muons from anti-taus is",n_amuons_from_taus)
print("Total number of gravitinos is",n_gravitino)     

# Create a histogram of the number of each particle type in the event

# Data
labels = [
    "stau-",
    "stau- InAcce",
    "stau+",
    "stau+ InAcce",
    "tau-",
    "tau- InAcce",
    "tau+",
    "tau+ InAcce",
    "gravitinos",
    "muons-",
    "muons+",
    "muon- from tau-",
    "muos+ from tau+",
    "tau- from stau-",
    "tau+ from stau+",
]
values = [
    n_stau,
    n_stau_in_acc,
    n_a_stau,
    n_a_stau_in_acc,
    n_tau,
    n_taus_in_acc,
    n_a_tau,
    n_ataus_in_acc,
    n_gravitino,
    n_muons,
    n_amuons,
    n_muons_from_taus,
    n_amuons_from_taus,
    n_taus_from_staus,
    n_a_taus_from_staus,
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
plt.savefig('figs/n_particles_hist.pdf', bbox_inches='tight')
