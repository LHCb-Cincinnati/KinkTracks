# Imports
import sys
import pdb
from array import array
import numpy as np

#import ROOT
#from ROOT import TFile, TTree, TH1F, TCanvas, gROOT, gStyle
import ROOT
from ROOT import gROOT, gStyle, TCanvas, TFile, TTree, TH1F, TH2F, TH3F, TH1D, TH2D, TH3D

import GaudiPython
from GaudiConf import IOHelper
from Configurables import DaVinci
from Configurables import CombineParticles
from Configurables import ApplicationMgr 
from glob import glob


for file in glob("*.sim"):
    IOHelper('ROOT').inputFiles([file], clear=True)   

# Configure DaVinci
DaVinci().Simulation = True
DaVinci().Lumi = False
DaVinci().DataType = '2017'
DaVinci().InputType = 'DIGI'
DaVinci().EvtMax = -1
DaVinci().DDDBtag = 'dddb-20210215-6'

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
gaudi.run(1)
particles = tes['MC/Particles']
pid_list = [particle.particleID().pid() for particle in particles]

# using the PDG naming convention, more about in this link
# https://gist.github.com/MohamedElashri/aaa9c58d9d3477b4f0fca40f7f2f91ec
n_stau = pid_list.count(1000015) # Number of staus (stau-) > (s_tau_minus_L)
n_a_stau = pid_list.count(-1000015) # Number of anti-staus (stau+) > (s_tau_plus_L)
n_gravitino = pid_list.count(1000039) # Number of gravitinos (gravitino) > (s_G)
n_tau = pid_list.count(15) # Number of taus (tau-) > (tau_minus)
n_a_tau = pid_list.count(-15) # Number of anti-taus (tau+) > (tau_plus)
        
# for stau_minus_L create Eta distribution and plot it
stau_minus_L = [particle for particle in particles if particle.particleID().pid() == 1000015]
stau_minus_L_eta = [particle.momentum().eta() for particle in stau_minus_L]
stau_minus_L_eta_histo = TH1F("stau_minus_L_eta_histo", "stau_minus_L_eta_histo", 10, 1.5, 5)
for eta in stau_minus_L_eta:
    stau_minus_L_eta_histo.Fill(eta)
c1 = TCanvas()
stau_minus_L_eta_histo.Draw()
c1.Print("stau_minus_L_eta_distribution.pdf")        


# for stau_plus_L create Eta distribution and plot it
stau_plus_L = [particle for particle in particles if particle.particleID().pid() == -1000015]
stau_plus_L_eta = [particle.momentum().eta() for particle in stau_plus_L]
stau_plus_L_eta_histo = TH1F("stau_plus_L_eta_histo", "stau_plus_L_eta_histo", 10, 1.5, 5)
for eta in stau_plus_L_eta:
    stau_plus_L_eta_histo.Fill(eta)
c2 = TCanvas()
stau_plus_L_eta_histo.Draw()
c2.Print("stau_plus_L_eta_distribution.pdf")

#  for gravitino create Eta distribution and plot it
gravitino = [particle for particle in particles if particle.particleID().pid() == 1000039]
gravitino_eta = [particle.momentum().eta() for particle in gravitino]
gravitino_eta_histo = TH1F("gravitino_eta_histo", "gravitino_eta_histo", 10, 1.5, 5)
for eta in gravitino_eta:
    gravitino_eta_histo.Fill(eta)
c3 = TCanvas()
gravitino_eta_histo.Draw()
c3.Print("gravitino_eta_distribution.pdf")

#  for tau or anti tau create Eta distribution and plot it
tau = [particle for particle in particles if particle.particleID().pid() == 15]
tau_eta = [particle.momentum().eta() for particle in tau]
tau_eta_histo = TH1F("tau_eta_histo", "tau_eta_histo", 10, 1.5, 5)
for eta in tau_eta:
    tau_eta_histo.Fill(eta)
c4 = TCanvas()
tau_eta_histo.Draw()
c4.Print("tau_eta_distribution.pdf")

a_tau = [particle for particle in particles if particle.particleID().pid() == -15]
a_tau_eta = [particle.momentum().eta() for particle in a_tau]
a_tau_eta_histo = TH1F("a_tau_eta_histo", "a_tau_eta_histo", 10, 1.5, 5)
for eta in a_tau_eta:
    a_tau_eta_histo.Fill(eta)
c5 = TCanvas()
a_tau_eta_histo.Draw()
c5.Print("a_tau_eta_distribution.pdf")


      
for particle in particles: 
    if particle.particleID().pid() == 1000015:       
       print("The particle is an stau-")
       print("The particle ID is",particle.particleID().pid())
       print("The particle Mass is",particle.momentum().mass())
       print("Particle momentum is", particle.momentum().pt())
       print("Primary Vertex is",particle.primaryVertex())   
       print("Origin Vertex is",particle.originVertex())
       
    if particle.particleID().pid() == -1000015:
       print("The particle is a stau+")
       print("The particle ID is",particle.particleID().pid())
       print("The particle Mass is",particle.momentum().mass())
       print("Particle momentum is", particle.momentum().pt())
       print("Primary Vertex is",particle.primaryVertex())   
       print("Origin Vertex is",particle.originVertex()) 

    if particle.particleID().pid() == 15:
       print("The particle is a tau-")
       print("The particle ID is",particle.particleID().pid())
       print("The particle Mass is",particle.momentum().mass())
       print("Primary Vertex is",particle.primaryVertex())   
       print("Origin Vertex is",particle.originVertex()) 
       print("Particle mother pid is",particle.mother())
       if particle.originVertex().isDecay() == True:
          print("The particle is a decay product")
       else:
          print("The particle is a primary particle")

    if particle.particleID().pid() == -15:
       print("The particle is a tau+")
       print("The particle ID is",particle.particleID().pid())
       print("The particle Mass is",particle.momentum().mass())
       print("Primary Vertex is",particle.primaryVertex())   
       print("Origin Vertex is",particle.originVertex()) 
       print("Particle mother pid is",particle.mother())
       if particle.originVertex().isDecay() == True:
          print("The particle is a decay product")
       else:
          print("The particle is a primary particle")
          
    if particle.particleID().pid() == 1000039:
       print("The particle is Gravitino")
       print("The particle ID is",particle.particleID().pid())
       print("The particle Mass is",particle.momentum().mass())
       print("Primary Vertex is",particle.primaryVertex())   
       print("Origin Vertex is",particle.originVertex()) 
       print("Particle mother pid is",particle.mother())
       if particle.originVertex().isDecay() == True:
          print("The particle is a decay product")
       else:
          print("The particle is a primary particle")
       
print("Total number of staus is",n_stau)
print("Total number of anti-staus is",n_a_stau)
print("Total number of taus is",n_tau)
print("Total number of anti-taus is",n_a_tau)
print("Total number of gravitinos is",n_gravitino)       
pdb.set_trace()
