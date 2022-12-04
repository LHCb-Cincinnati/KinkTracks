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

''' 
from glob import glob
for file in glob("*.sim"):
    IOHelper('ROOT').inputFiles([file], clear=True)   
'''
datafile = '/afs/cern.ch/work/m/melashri/public/SUSY/MC/Sim10/Gauss_Dev/GaussDev_v55r4/Stau_100GeV_100nEv_llp.sim'
datafile1 = '/afs/cern.ch/work/m/melashri/public/SUSY/MC/Sim10/Gauss_Dev/GaussDev_v55r4/Stau_100GeV_100nEv_llp_0-199Events.sim'
datafile2 = '/afs/cern.ch/work/m/melashri/public/SUSY/MC/Sim10/Gauss_Dev/GaussDev_v55r4/Stau_100GeV_100nEv_llp_200-399Events.sim'
datafile3 = '/afs/cern.ch/work/m/melashri/public/SUSY/MC/Sim10/Gauss_Dev/GaussDev_v55r4/Stau_100GeV_100nEv_llp_400-599Events.sim'
datafile4 = '/afs/cern.ch/work/m/melashri/public/SUSY/MC/Sim10/Gauss_Dev/GaussDev_v55r4/Stau_100GeV_100nEv_llp_600-799Events.sim'
datafile5 = '/afs/cern.ch/work/m/melashri/public/SUSY/MC/Sim10/Gauss_Dev/GaussDev_v55r4/Stau_100GeV_100nEv_llp_800-999Events.sim'
datafile6 = '/afs/cern.ch/work/m/melashri/public/SUSY/MC/Sim10/Gauss_Dev/GaussDev_v55r4/Stau_100GeV_100nEv_llp_1000-1199Events.sim'
datafile7 = '/afs/cern.ch/work/m/melashri/public/SUSY/MC/Sim10/Gauss_Dev/GaussDev_v55r4/Stau_100GeV_100nEv_llp_1200-1399Events.sim'
datafile8 = '/afs/cern.ch/work/m/melashri/public/SUSY/MC/Sim10/Gauss_Dev/GaussDev_v55r4/Stau_100GeV_100nEv_llp_1400-1599Events.sim'
datafile9 = '/afs/cern.ch/work/m/melashri/public/SUSY/MC/Sim10/Gauss_Dev/GaussDev_v55r4/Stau_100GeV_100nEv_llp_1600-1799Events.sim'
datafile10 = '/afs/cern.ch/work/m/melashri/public/SUSY/MC/Sim10/Gauss_Dev/GaussDev_v55r4/Stau_100GeV_100nEv_llp_1800-1999Events.sim'

IOHelper().inputFiles([
    datafile1,datafile2
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
#gaudi.evtMax = 100
#particles = tes['MC/Particles']
#pid_list = [particle.particleID().pid() for particle in particles]

'''
# using the PDG naming convention, more about in this link
# https://gist.github.com/MohamedElashri/aaa9c58d9d3477b4f0fca40f7f2f91ec
n_stau = pid_list.count(1000015) # Number of staus (stau-) > (s_tau_minus_L)
n_a_stau = pid_list.count(-1000015) # Number of anti-staus (stau+) > (s_tau_plus_L)
n_gravitino = pid_list.count(1000039) # Number of gravitinos (gravitino) > (s_G)
n_tau = pid_list.count(15) # Number of taus (tau-) > (tau_minus)
n_a_tau = pid_list.count(-15) # Number of anti-taus (tau+) > (tau_plus)
'''
n_stau = 0
n_a_stau = 0
n_gravitino = 0
n_tau = 0
n_a_tau = 0
evtmax = 100
processed = 0
#stau_minus_L_eta_histo = TH1F("stau_minus_L_eta_histo", "stau_minus_L_eta_histo", 10, 1.5, 5)
#stau_plus_L_eta_histo = TH1F("stau_plus_L_eta_histo", "stau_plus_L_eta_histo", 10, 1.5, 5)
#gravitino_eta_histo = TH1F("gravitino_eta_histo", "gravitino_eta_histo", 10, 1.5, 5)
#tau_eta_histo = TH1F("tau_eta_histo", "tau_eta_histo", 10, 1.5, 5)
#a_tau_eta_histo = TH1F("a_tau_eta_histo", "a_tau_eta_histo", 10, 1.5, 5)
decay_angle_histo = TH1F("decay_angle_histo", "decay_angle_histo", 10, 0, 50)
#c1 = TCanvas()
#c2 = TCanvas()
#c3 = TCanvas()
#c4 = TCanvas()
#c5 = TCanvas()
c6 = TCanvas()



while processed < evtmax:
#while bool(tes['/Event']) and processed < evtmax:
    processed += 1
    gaudi.run(1)
    particles = tes['MC/Particles']
    pid_list = [particle.particleID().pid() for particle in particles]
    #n_stau = pid_list.count(1000015) # Number of staus (stau-) > (s_tau_minus_L)
    #n_a_stau = pid_list.count(-1000015) # Number of anti-staus (stau+) > (s_tau_plus_L)
    #n_gravitino = pid_list.count(1000039) # Number of gravitinos (gravitino) > (s_G)
    #n_tau = pid_list.count(15) # Number of taus (tau-) > (tau_minus)
    #n_a_tau = pid_list.count(-15) # Number of anti-taus (tau+) > (tau_plus)
       
    for particle in particles: 
        if particle.particleID().pid() == 1000015:
            n_stau += 1        
            print("The particle is an stau-")
            print("The particle ID is",particle.particleID().pid())
            print("The particle Mass is",particle.momentum().mass())
            print("Particle momentum is", particle.momentum().pt())
            print("Primary Vertex is",particle.primaryVertex().position4vector())   
            print("Origin Vertex is",particle.originVertex().position4vector())
            # find daughter particles of stau 
            print
       
        if particle.particleID().pid() == -1000015:
            n_a_stau += 1 
            print("The particle is a stau+")
            print("The particle ID is",particle.particleID().pid())
            print("The particle Mass is",particle.momentum().mass())
            print("Particle momentum is", particle.momentum().pt())
            print("Primary Vertex is",particle.primaryVertex().position4vector())   
            print("Origin Vertex is",particle.originVertex().position4vector())

        if particle.particleID().pid() == 15:
            n_tau += 1
            print("The particle is a tau-")
            print("The particle ID is",particle.particleID().pid())
            print("The particle Mass is",particle.momentum().mass())
            print("Primary Vertex is",particle.primaryVertex().position4vector())   
            print("Origin Vertex is",particle.originVertex().position4vector())
            print("Particle mother pid is",particle.mother())
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
    stau_minus_L = [particle for particle in particles if particle.particleID().pid() == 1000015]
    stau_plus_L = [particle for particle in particles if particle.particleID().pid() == -1000015]
    
    gravitino_phi_angle = [particle.momentum().phi() for particle in particles if particle.particleID().pid() == 1000039]
    tau_phi_angle = [particle.momentum().phi() for particle in particles if particle.particleID().pid() == 15]
    atau_phi_angle = [particle.momentum().phi() for particle in particles if particle.particleID().pid() == -15]
    #decay_angle is the difference in phi between the gravitino and the tau or gravitino and the anti-tau
    for i in gravitino_phi_angle:
        for j in tau_phi_angle:
            decay_angle = abs(i-j)
            decay_angle_histo.Fill(decay_angle)

    for i in gravitino_phi_angle:
        for j in atau_phi_angle:
            decay_angle = abs(i-j)
            decay_angle_histo.Fill(decay_angle)
    c6.Print("decay_angle_histo.pdf")   
'''
    stau_minus_L = [particle for particle in particles if particle.particleID().pid() == 1000015]
    stau_minus_L_eta = [particle.momentum().eta() for particle in stau_minus_L]
    for eta in stau_minus_L_eta:
        stau_minus_L_eta_histo.Fill(eta)
    stau_minus_L_eta_histo.Draw()
    c1.Print("stau_minus_L_eta_distribution.pdf")  

    stau_plus_L = [particle for particle in particles if particle.particleID().pid() == -1000015]
    stau_plus_L_eta = [particle.momentum().eta() for particle in stau_plus_L]
    for eta in stau_plus_L_eta:
        stau_plus_L_eta_histo.Fill(eta)
    stau_plus_L_eta_histo.Draw()        
    c2.Print("stau_plus_L_eta_distribution.pdf")          
    
    gravitino = [particle for particle in particles if particle.particleID().pid() == 1000039]
    gravitino_eta = [particle.momentum().eta() for particle in gravitino]
    for eta in gravitino_eta:
        gravitino_eta_histo.Fill(eta)
    gravitino_eta_histo.Draw()
    c3.Print("gravitino_eta_distribution.pdf")
        
    tau = [particle for particle in particles if particle.particleID().pid() == 15]
    tau_eta = [particle.momentum().eta() for particle in tau]
    for eta in tau_eta:
        tau_eta_histo.Fill(eta)
    tau_eta_histo.Draw()
    c4.Print("tau_eta_distribution.pdf")
    
    a_tau = [particle for particle in particles if particle.particleID().pid() == -15]
    a_tau_eta = [particle.momentum().eta() for particle in a_tau]
    for eta in a_tau_eta:
        a_tau_eta_histo.Fill(eta)
    a_tau_eta_histo.Draw()
    c5.Print("a_tau_eta_distribution.pdf")
'''      
            
      

            
print("Total number of staus is",n_stau)
print("Total number of anti-staus is",n_a_stau)
print("Total number of taus is",n_tau)
print("Total number of anti-taus is",n_a_tau)
print("Total number of gravitinos is",n_gravitino)     

pdb.set_trace()
