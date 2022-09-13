# Imports
import sys
import pdb
from array import array

import numpy as np
#import ROOT

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
pdb.set_trace()
#print(particles)