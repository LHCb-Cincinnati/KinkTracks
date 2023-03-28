'''
Name: decay_length.py
Description: This is a Gaudipython script to get the decay length distribution in stau MC samples.
Author: Mohamed Elashri
Date: 2023-03-28
Usage: lb-run DaVinci/v45r8 python3 -i decay_length.py
'''



from Gaudi.Configuration import *
from GaudiConf import IOHelper
from Configurables import LHCbApp, ApplicationMgr, GaudiSequencer
from Configurables import DaVinci, DecodeRawEvent, RawEventFormatConf, UnpackMCParticle, UnpackMCVertex
import GaudiPython
from ROOT import TH1F, TCanvas

import math
import re
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pdb
from utils import *


LHCbApp().Simulation = True
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



appMgr = GaudiPython.AppMgr()
appMgr.config()
appMgr.initialize()


# Common variables
# ----------------------------------
# Get the event service
evtSvc = appMgr.evtsvc()
gaudi = GaudiPython.AppMgr()
evtmax = 99
processed = 0
n_valid_decays = 0 # number of valid decays (stau -> tau + G~)
decay_lengths = [] # list of decay lengths of valid decays
# ----------------------------------

'''
## Functions
# ----------------------------------
# check if the decay is valid
def is_valid_decay(mother, daughter):
    if mother and daughter:
        if (mother.particleID().pid() == 1000015 or mother.particleID().pid() == -1000015) and (
            daughter.particleID().pid() == 15 or daughter.particleID().pid() == -15
        ):
            if mother.endVertices() and len(mother.endVertices()) > 0:
                other_daughter = [
                    child for child in mother.endVertices()[0].products() if child != daughter
                ]
                if other_daughter and other_daughter[0].particleID().pid() == 1000039:
                    return True
    return False

# calculate the decay length of a particle from vertices
def decay_length_from_vertices(production_vertex, decay_vertex):
    position_diff = decay_vertex.position() - production_vertex.position()
    decay_length = position_diff.R()
    return decay_length

# ----------------------------------
'''

gaudi = GaudiPython.AppMgr()
tes   = gaudi.evtsvc()
while processed < evtmax:
    processed += 1
    gaudi.run(1)
    particles = tes['MC/Particles']
    pid_list = [particle.particleID().pid() for particle in particles]
    print("Event number: ", processed)
    for particle in particles: 
        if particle.particleID().pid() == 1000015 or particle.particleID().pid() == -1000015:
            mother = particle
            if mother.endVertices() and len(mother.endVertices()) > 0:
                for daughter in mother.endVertices()[0].products():
                    if is_valid_decay(mother, daughter):
                        n_valid_decays += 1
                        production_vertex = mother.originVertex()
                        decay_vertex = mother.endVertices()[0]
                        decay_length = decay_length_from_vertices(production_vertex, decay_vertex)
                        decay_lengths.append(decay_length)                        
                        #print("Valid decay found:")
                        #print("The mother particle is stau with ID", mother.particleID().pid())
                        #print("The daughter particle is tau with ID", daughter.particleID().pid())
                        
print("Number of valid decays: ", n_valid_decays)        

# ----------------------------------

## Useful common tricks

# automate naming directories in plots
### TODO: Make this work with different mass points

mm_value = re.search(r'(\d+)mm', datafile).group(1) # Extract the number before 'mm' from the input file path
# Create a folder for the output files if it doesn't exist
output_folder = f"figs/100GeV_{mm_value}mm"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)



# Plot the decay length distribution using matplotlib
plt.figure()
plt.hist(decay_lengths, bins=100)
plt.xlabel('Decay Length (m)')
plt.ylabel('Frequency')
plt.title('Stau Decay Length Distribution')
plt.savefig(f"{output_folder}/DecayLength_{mm_value}mm.pdf")

pdb.set_trace()        