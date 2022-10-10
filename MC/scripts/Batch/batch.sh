#!/bin/bash
for i in {1..10}
do
    cat << EOF > Gauss-Job_${i}.py
from Gaudi.Configuration import *
from Configurables import Gauss, LHCbApp
theApp = Gauss()
from Gaudi.Configuration import VERBOSE
from Configurables import MessageSvc
MessageSvc().OutputLevel = VERBOSE
importOptions("\$APPCONFIGOPTS/Gauss/Beam6500GeV-md100-2017-nu1.6.py") # Sets beam energy and position
importOptions("\$APPCONFIGOPTS/Gauss/DataType-2017.py") # Sets data type
importOptions("\$APPCONFIGOPTS/Gauss/RICHRandomHits.py") # Random hits in RICH for occupancy
importOptions("/afs/cern.ch/work/m/melashri/public/SUSY/MC/Sim10/Gauss_Dev/GaussDev_v55r4/Gen/DecFiles/options/47000210.py")
importOptions("\$LBPYTHIA8ROOT/options/Pythia8.py") #Setting generator
importOptions("\$APPCONFIGOPTS/Gauss/G4PL_FTFP_BERT_EmNoCuts.py") # Physics simulated by Geant4
GaussGen = GenInit("GaussGen")
GaussGen.FirstEventNumber = 5
GaussGen.RunNumber = 150
LHCbApp().DDDBtag   = "dddb-20210215-6"
LHCbApp().CondDBtag = "sim-20201113-8-vc-mu100-Sim10"
nEvts = 100
LHCbApp().EvtMax = nEvts
OutputStream("GaussTape").Output = "DATAFILE='PFN:Stau_100GeV_100nEv_llp_100Events_${i}.sim' TYP='POOL_ROOTTREE' OPT='RECREATE'"
EOF
done
