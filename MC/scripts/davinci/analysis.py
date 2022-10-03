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


# Use the local input data
datafile = '/afs/cern.ch/work/m/melashri/public/SUSY/MC/Sim10/Gauss_Dev/GaussDev_v55r4/Stau_100GeV_100nEv_llp.sim'
IOHelper().inputFiles([
    datafile
], clear=True)

# Configure DaVinci
#DaVinci().TupleFile = "DVntuple.root"
DaVinci().Simulation = True
DaVinci().Lumi = False
DaVinci().DataType = '2017'
DaVinci().InputType = 'DIGI'
#DaVinci().UserAlgorithms = [mctuple]d100'
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


# Configure GaudiPython
gaudi = GaudiPython.AppMgr()
tes   = gaudi.evtsvc()
gaudi.run(100)
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
c1.Print("Distributions/stau_minus_L_eta_distribution.pdf")        


# for stau_plus_L create Eta distribution and plot it
stau_plus_L = [particle for particle in particles if particle.particleID().pid() == -1000015]
stau_plus_L_eta = [particle.momentum().eta() for particle in stau_plus_L]
stau_plus_L_eta_histo = TH1F("stau_plus_L_eta_histo", "stau_plus_L_eta_histo", 10, 1.5, 5)
for eta in stau_plus_L_eta:
    stau_plus_L_eta_histo.Fill(eta)
c2 = TCanvas()
stau_plus_L_eta_histo.Draw()
c2.Print("Distributions/stau_plus_L_eta_distribution.pdf")

#  for gravitino create Eta distribution and plot it
gravitino = [particle for particle in particles if particle.particleID().pid() == 1000039]
gravitino_eta = [particle.momentum().eta() for particle in gravitino]
gravitino_eta_histo = TH1F("gravitino_eta_histo", "gravitino_eta_histo", 10, 1.5, 5)
for eta in gravitino_eta:
    gravitino_eta_histo.Fill(eta)
c3 = TCanvas()
gravitino_eta_histo.Draw()
c3.Print("Distributions/gravitino_eta_distribution.pdf")

#  for tau or anti tau create Eta distribution and plot it
tau = [particle for particle in particles if particle.particleID().pid() == 15]
tau_eta = [particle.momentum().eta() for particle in tau]
tau_eta_histo = TH1F("tau_eta_histo", "tau_eta_histo", 10, 1.5, 5)
for eta in tau_eta:
    tau_eta_histo.Fill(eta)
c4 = TCanvas()
tau_eta_histo.Draw()
c4.Print("Distributions/tau_eta_distribution.pdf")

a_tau = [particle for particle in particles if particle.particleID().pid() == -15]
a_tau_eta = [particle.momentum().eta() for particle in a_tau]
a_tau_eta_histo = TH1F("a_tau_eta_histo", "a_tau_eta_histo", 10, 1.5, 5)
for eta in a_tau_eta:
    a_tau_eta_histo.Fill(eta)
c5 = TCanvas()
a_tau_eta_histo.Draw()
c5.Print("Distributions/a_tau_eta_distribution.pdf")




# for stau_minus_L and stau_Plus_L  creat decay length distribution and plot it
stau_minus_L_decay_length = [particle.endVertices() for particle in stau_minus_L]
stau_minus_L_decay_length_histo = TH1F("stau_minus_L_decay_length_histo", "stau_minus_L_decay_length_histo", 10, 0, 50)
for length in stau_minus_L_decay_length:
    stau_minus_L_decay_length_histo.Fill(length)
c6 = TCanvas()
stau_minus_L_decay_length_histo.Draw()
c6.Print("Distributions/stau_minus_L_decay_length_distribution.pdf")

stau_plus_L_decay_length = [particle.endVertices() for particle in stau_plus_L]
stau_plus_L_decay_length_histo = TH1F("stau_plus_L_decay_length_histo", "stau_plus_L_decay_length_histo", 10, 0, 50)
for length in stau_plus_L_decay_length:
    stau_plus_L_decay_length_histo.Fill(length)
c7 = TCanvas()
stau_plus_L_decay_length_histo.Draw()
c7.Print("Distributions/stau_plus_L_decay_length_distribution.pdf")

# for gravitino, tau and anti-tau  creat decay length distribution and plot it
gravitino_decay_length = [particle.endVertices() for particle in gravitino]
gravitino_decay_length_histo = TH1F("gravitino_decay_length_histo", "gravitino_decay_length_histo", 10, 0, 50)
for length in gravitino_decay_length:
    gravitino_decay_length_histo.Fill(length)
c8 = TCanvas()
gravitino_decay_length_histo.Draw()
c8.Print("Distributions/gravitino_decay_length_distribution.pdf")

tau_decay_length = [particle.endVertices() for particle in tau]
tau_decay_length_histo = TH1F("tau_decay_length_histo", "tau_decay_length_histo", 10, 0, 50)
for length in tau_decay_length:
    tau_decay_length_histo.Fill(length)
c9 = TCanvas()
tau_decay_length_histo.Draw()
c9.Print("Distributions/tau_decay_length_distribution.pdf")

a_tau_decay_length = [particle.endVertex() for particle in a_tau]
a_tau_decay_length_histo = TH1F("a_tau_decay_length_histo", "a_tau_decay_length_histo", 10, 0, 50)
for length in a_tau_decay_length:
    a_tau_decay_length_histo.Fill(length)
c10 = TCanvas()
a_tau_decay_length_histo.Draw()
c10.Print("Distributions/a_tau_decay_length_distribution.pdf")


 '''      
for particle in particles: 
    if particle.particleID().pid() == 1000015:       
       print("The particle is an stau-")
       print("The particle ID is",particle.particleID().pid())
       print("The particle Mass is",particle.momentum().mass())
       print("Particle momentum is", particle.momentum().pt())
       print("Primary Vertex is",particle.primaryVertex())   
       print("Origin Vertex is",particle.originVertex())
       print("Total number of anti-taus is",n_tau)
       
    if particle.particleID().pid() == -1000015:
       print("The particle is a stau+")
       print("The particle ID is",particle.particleID().pid())
       print("The particle Mass is",particle.momentum().mass())
       print("Particle momentum is", particle.momentum().pt())
       print("Primary Vertex is",particle.primaryVertex())   
       print("Origin Vertex is",particle.originVertex()) 
       print("Total number of taus is",n_a_stau)

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
       print("Total number of taus is",n_tau)      

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
       print("Total number of taus is",n_a_tau)       
          
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
       print("Total number of gravitinos is",n_gravitino)    
'''       
       
pdb.set_trace()
