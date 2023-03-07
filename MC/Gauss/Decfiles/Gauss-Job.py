from Gauss.Configuration import *
from Configurables import Gauss, LHCbApp

theApp = Gauss()

from Gaudi.Configuration import VERBOSE
from Configurables import MessageSvc
MessageSvc().OutputLevel = VERBOSE

importOptions("$APPCONFIGOPTS/Gauss/Beam6500GeV-md100-2017-nu1.6.py") # Sets beam energy and position
importOptions("$APPCONFIGOPTS/Gauss/DataType-2017.py") # Sets data type
importOptions("$APPCONFIGOPTS/Gauss/RICHRandomHits.py") # Random hits in RICH for occupancy
importOptions("$DECFILESROOT/options/47501000.py")
importOptions("$LBPYTHIA8ROOT/options/Pythia8.py") #Setting generator
importOptions("$APPCONFIGOPTS/Gauss/G4PL_FTFP_BERT_EmNoCuts.py") # Physics simulated by Geant4
#importOptions("$GAUSSOPTS/GenStandAlone.py") # Run only the Generation part
#--Generator phase, set random numbers
GaussGen = GenInit("GaussGen")
GaussGen.FirstEventNumber = 5
GaussGen.RunNumber = 150


# For Run3 (otherwise wait for bugs)
LHCbApp().DDDBtag   = "dddb-20210215-6"
LHCbApp().CondDBtag = "sim-20201113-8-vc-mu100-Sim10"

#--Number of events
nEvts = 10
LHCbApp().EvtMax = nEvts

OutputStream("GaussTape").Output = "DATAFILE='PFN:Stau_100GeV_10n_short_tau.sim' TYP='POOL_ROOTTREE' OPT='RECREATE'"
#OutputStream("GaussTape").Output = "DATAFILE='PFN:Stau_100GeV_10nEv.xgen' TYP='POOL_ROOTTREE' OPT='RECREATE'"