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
#datafile = '/afs/cern.ch/work/m/melashri/public/SUSY/MC/Sim10/Gauss_Dev/GaussDev_v55r4/analysis/data/Stau_150GeV_100n_100mm_ctau_with_length_Cut.sim'
datafile = '/afs/cern.ch/work/m/melashri/public/SUSY/MC/Sim10/Gauss_Dev/GaussDev_v55r4/Stau_100GeV_100n_100mm_ctau_with_length_Cut_test.sim'
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

gaudi = GaudiPython.AppMgr()
tes   = gaudi.evtsvc()
while processed < evtmax:
    processed += 1
    gaudi.run(1)
    particles = tes['MC/Particles']
    pid_list = [particle.particleID().pid() for particle in particles]
    #print("Event number: ", processed)
    for particle in particles: 
        if particle.particleID().pid() == 1000015 or particle.particleID().pid() == -1000015:
            mother = particle
            if mother.endVertices() and len(mother.endVertices()) > 0:
                # Iterate over all the end vertices of the mother particle
                for end_vertex in mother.endVertices():
                    # Analyze the daughter particles of each end vertex
                    for daughter in end_vertex.products():
                        if is_valid_decay(mother, daughter):
                            n_valid_decays += 1
                            # Call the calculate_decay_length function to get a list of decay lengths
                            decay_lengths_for_mother = calculate_decay_length(mother)
                            # Append each decay length to the decay_lengths list
                            decay_lengths.extend(decay_lengths_for_mother)
                            #print("Valid decay found:")
                            #print("The mother particle is stau with ID", mother.particleID().pid())
                            #print("The daughter particle is tau with ID", daughter.particleID().pid())
                        
print("Number of valid decays: ", n_valid_decays)        

# ----------------------------------

## Useful common tricks

# automate naming directories in plots
### TODO: Make this work with different mass points

mm_value = re.search(r'(\d+)mm', datafile).group(1) # Extract the number before 'mm' from the input file path
mass_value = re.search(r'(\d+)GeV', datafile).group(1) # Extract the number before 'GeV' from the input file path
# Create a folder for the output files if it doesn't exist
output_folder = f"figs/{mass_value}GeV_{mm_value}mm"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)



# Plot the decay length distribution using matplotlib
plt.figure()
plt.hist(decay_lengths, bins=50)
plt.xlabel('Decay Length (m)')
plt.ylabel('Frequency')
## Add text with the total number of valid decays on the plot
plt.text(0.45, 0.70, f"Total number of valid decays: {n_valid_decays}", transform=plt.gca().transAxes)
plt.title('Stau Decay Length Distribution')
plt.savefig(f"{output_folder}/DecayLength_{mass_value}GeV_{mm_value}mm_cut_test.pdf")

pdb.set_trace()        