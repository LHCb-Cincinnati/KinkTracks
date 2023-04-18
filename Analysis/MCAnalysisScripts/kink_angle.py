'''
Name: kink_angle.py
Description: This is a Gaudipython script to calculate the kink angle in stau MC samples.
Author: Mohamed Elashri
Date: 2023-03-27
Usage: lb-run DaVinci/v45r8 python3 -i kink_angle.py
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
datafile = '/afs/cern.ch/work/m/melashri/public/SUSY/MC/Sim10/Gauss_Dev/GaussDev_v55r4/analysis/data/Stau_100GeV_100n_10000mm_ctau_with_Cut.sim'
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
kink_angles_phi = [] # list to store the kink angles based  on the phi angles
kink_angles_theta = [] # list to store the kink angles based  on the theta angles
kink_angles_3d = [] # list to store the 3D kink angles
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

# calculate the kink angle based on the phi angles
def calculate_kink_angle_phi(mother, daughter):
    stau_phi = mother.momentum().phi()
    tau_phi = daughter.momentum().phi()
    kink_angle = stau_phi - tau_phi
    # convert the angles to degrees
    kink_angle = kink_angle * 180 / 3.14159265359
    return kink_angle

# calculate the kink angle based on the theta angles
def calculate_kink_angle_theta(mother, daughter):
    stau_theta = mother.momentum().theta()
    tau_theta = daughter.momentum().theta()
    kink_angle = stau_theta - tau_theta
    # convert the angles to degrees
    kink_angle = kink_angle * 180 / 3.14159265359
    return kink_angle

# calculate the 3D kink angle
def calculate_3d_kink_angle(mother, daughter):
    theta_mother = mother.momentum().theta()
    theta_daughter = daughter.momentum().theta()
    phi_mother = mother.momentum().phi()
    phi_daughter = daughter.momentum().phi()
    
    cos_kink_angle = (math.sin(theta_mother) * math.sin(theta_daughter) * 
                      (math.cos(phi_mother) * math.cos(phi_daughter) + math.sin(phi_mother) * math.sin(phi_daughter)) +
                      math.cos(theta_mother) * math.cos(theta_daughter))
    
    kink_angle = math.acos(cos_kink_angle)
    kink_angle = kink_angle * 180 / 3.14159265359
    return kink_angle


# ----------------------------------
'''



gaudi = GaudiPython.AppMgr()
tes   = gaudi.evtsvc()


## Histograms

# ----------------------------------
# create histograms to store the kink angle distributions
kink_angle_phi_hist = TH1F("kink_angle_hist", "Kink Angle Distribution(phi)", 100, -180, 180)
kink_angle_theta_hist = TH1F("kink_angle_hist", "Kink Angle Distribution (theta)", 100, -180, 180)
kink3D_angle_hist = TH1F("3d_kink_angle_hist", "3D Kink Angle Distribution", 100, 0, 180)
# ----------------------------------


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
                        kink_angle_phi = calculate_kink_angle_phi(mother, daughter)
                        kink_angle_theta = calculate_kink_angle_theta(mother, daughter)
                        kink3_angle = calculate_3d_kink_angle(mother, daughter)
                        kink_angle_phi_hist.Fill(kink_angle_phi)
                        kink_angle_theta_hist.Fill(kink_angle_theta)
                        kink3D_angle_hist.Fill(kink3_angle)
                        kink_angles_phi.append(kink_angle_phi)
                        kink_angles_theta.append(kink_angle_theta)
                        kink_angles_3d.append(kink3_angle)
                        #print("Valid decay found:")
                        #print("The mother particle is stau with ID", mother.particleID().pid())
                        #print("The daughter particle is tau with ID", daughter.particleID().pid())
                        #print("The kink angle is", kink_angle)
                        
print("Number of valid decays: ", n_valid_decays)        



## Useful common tricks

# automate naming directories in plots
### TODO: Make this work with different mass points

mm_value = re.search(r'(\d+)mm', datafile).group(1) # Extract the number before 'mm' from the input file path
# Create a folder for the output files if it doesn't exist
output_folder = f"figs/100GeV_{mm_value}mm"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
"""
We use the following to update 
canvas.SaveAs(f"{output_folder}/kink_angle_distribution_phi_{mm_value}mm.pdf")
canvas.SaveAs(f"{output_folder}/kink_angle_distribution_theta_{mm_value}mm.pdf")
canvas.SaveAs(f"{output_folder}/kink_3d_angle_distribution_{mm_value}mm.pdf")
plt.savefig(f"{output_folder}/kink_angle_distribution_phi_{mm_value}mm.pdf")
plt.savefig(f"{output_folder}/kink_angle_distribution_theta_{mm_value}mm.pdf")
plt.savefig(f"{output_folder}/kink_3d_angle_distribution_{mm_value}mm.pdf")
"""

# ---------------------------------------------
# draw the phi 3d kink angle distribution histogram using ROOT
canvas = TCanvas("c1", "Kink Angle Distribution (phi)", 800, 600)
kink_angle_phi_hist.Draw()
canvas.SaveAs("figs/100GeV_10mm/kink_angle_distribution_phi_10mm.pdf")   

# draw the theta 2d kink angle distribution histogram using ROOT
canvas = TCanvas("c2", "Kink Angle Distribution (theta)", 800, 600)
kink_angle_theta_hist.Draw()
canvas.SaveAs(f"{output_folder}/kink_angle_distribution_theta_{mm_value}mm.pdf")

# draw the 3D kink angle distribution histogram using ROOT
canvas = TCanvas("c3", "3D Kink Angle Distribution", 800, 600)
kink3D_angle_hist.Draw()
canvas.SaveAs(f"{output_folder}/kink_3d_angle_distribution_{mm_value}mm.pdf")

# draw the phi 2d kink angle distribution histogram using matplotlib
plt.figure()
plt.hist(kink_angles_phi, bins=100, range=(-180, 180))
plt.xlabel('Kink Angle')
plt.ylabel('Frequency')
plt.title('Kink Angle Distribution (phi)')
plt.savefig(f"{output_folder}/kink_angle_distribution_phi_{mm_value}mm_plt.pdf")

# draw the theta 2d kink angle distribution histogram using matplotlib
plt.figure()
plt.hist(kink_angles_theta, bins=100, range=(-180, 180))
plt.xlabel('Kink Angle')
plt.ylabel('Frequency')
plt.title('Kink Angle Distribution (phi)')
plt.savefig(f"{output_folder}/kink_angle_distribution_theta_{mm_value}mm_plt.pdf")

# draw the 3D kink angle distribution histogram using matplotlib
plt.figure()
plt.hist(kink_angles_3d, bins=100, range=(0, 180))
plt.xlabel('3D Kink Angle')
plt.ylabel('Frequency')
plt.title('3D Kink Angle Distribution')
plt.savefig(f"{output_folder}/kink_3d_angle_distribution_{mm_value}mm_plt.pdf")
# ---------------------------------------------


pdb.set_trace()        