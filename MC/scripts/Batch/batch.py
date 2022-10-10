# create mutiple files from Gauss-Job and change OutputStream only

import os
import sys
import subprocess

for i in range(1, 11):
    # create file
    with open('Gauss-Job_{}.py'.format(i), 'w') as f:
        f.write('from Gaudi.Configuration import *\n')
        f.write('from Configurables import Gauss, LHCbApp\n')
        f.write('theApp = Gauss()\n')
        f.write('from Gaudi.Configuration import VERBOSE\n')
        f.write('from Configurables import MessageSvc\n')
        f.write('MessageSvc().OutputLevel = VERBOSE\n')
        f.write('importOptions("$APPCONFIGOPTS/Gauss/Beam6500GeV-md100-2017-nu1.6.py") # Sets beam energy and position\n')
        f.write('importOptions("$APPCONFIGOPTS/Gauss/DataType-2017.py") # Sets data type\n')
        f.write('importOptions("$APPCONFIGOPTS/Gauss/RICHRandomHits.py") # Random hits in RICH for occupancy\n')
        f.write('importOptions("/afs/cern.ch/work/m/melashri/public/SUSY/MC/Sim10/Gauss_Dev/GaussDev_v55r4/Gen/DecFiles/options/47000210.py")\n')
        f.write('importOptions("$LBPYTHIA8ROOT/options/Pythia8.py") #Setting generator\n')
        f.write('importOptions("$APPCONFIGOPTS/Gauss/G4PL_FTFP_BERT_EmNoCuts.py") # Physics simulated by Geant4\n')
        f.write('GaussGen = GenInit("GaussGen")\n')
        f.write('GaussGen.FirstEventNumber = 5\n')
        f.write('GaussGen.RunNumber = 150\n')
        f.write('LHCbApp().DDDBtag   = "dddb-20210215-6"\n')
        f.write('LHCbApp().CondDBtag = "sim-20201113-8-vc-mu100-Sim10"\n')
        f.write('nEvts = 100\n')
        f.write('LHCbApp().EvtMax = nEvts\n')
        f.write('OutputStream("GaussTape").Output = "DATAFILE=\'PFN:Stau_100GeV_100nEv_llp_100Events_{}.sim\' TYP=\'POOL_ROOTTREE\' OPT=\'RECREATE\'"\n'.format(i))
