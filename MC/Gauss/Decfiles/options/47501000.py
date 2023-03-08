# file /afs/cern.ch/work/m/melashri/public/SUSY/MC/Sim10/Gauss_Dev/GaussDev_v56r3/Gen/DecFiles/options/47501000.py generated: Tue, 07 Mar 2023 19:04:22
#
# Event Type: 47501000
#
# ASCII decay Descriptor: pp -> (~tau_1- -> ~Gravitino tau- ' )
#
from Gaudi.Configuration import *
importOptions( "$DECFILESROOT/options/kinktracks.py" )
from Configurables import Generation
Generation().EventType = 47501000
Generation().SampleGenerationTool = "Special"
from Configurables import Special
Generation().addTool( Special )
Generation().Special.ProductionTool = "Pythia8Production"
from Configurables import ToolSvc
from Configurables import EvtGenDecay
ToolSvc().addTool( EvtGenDecay )
ToolSvc().EvtGenDecay.UserDecayFile = "$DECFILESROOT/dkfiles/GMSB_mtau_100GeV.dec"
Generation().Special.CutTool = "DaughtersInLHCb"
Generation().FullGenEventCutTool = "LoKi::FullGenEventCut/StauInAccTauInAcc"
 
from Configurables import LoKi__FullGenEventCut
Generation().addTool( LoKi__FullGenEventCut, "StauInAccTauInAcc" )
GenLevelSelection.Preambulo += [
     "from GaudiKernel.SystemOfUnits import GeV, mrad, mm, meter"
   , "inAcceptance           = ( GTHETA < 400.*mrad ) & ( GP > 2.0*GeV )"
   , "GEVZ                   =  GFAEVX( GVZ, LoKi.Constants.InvalidDistance )"
   , "GEVRHO                =  GFAEVX( GVRHO, LoKi.Constants.HugeDistance )"
   #, "DecayLengthCut         = in_range( 7800.*mm, GEVZ, 9500.*mm )"
   , "isStau                 = ( ( '~tau_1-' == GABSID ) | ( '~tau_1+' == GABSID ) )"
   , "isGoodTau              = ( ( 'tau-' == GABSID ) | ( 'tau+' == GABSID ) & inAcceptance)"
   #, "isStauWithTau = ( isStau & inAcceptance  & DecayLengthCut & ( GNINTREE( isStau, HepMC.descendants ) == 0 ) & ( GNINTREE( isGoodTau, HepMC.descendants ) > 0 ) )"
   , "isStauWithTau = ( isStau & inAcceptance   & ( GNINTREE( isStau, HepMC.descendants ) == 0 ) & ( GNINTREE( isGoodTau, HepMC.descendants ) > 0 ) )"
   ]
GenLevelSelection.Code = " count ( isStauWithTau ) > 0 "

from Configurables import GenerationToSimulation 
GenerationToSimulation("GenToSim").KeepCode = "( '~tau_1+' == GABSID  ) | ( '~tau_1-' == GABSID  )" # Keep MCParticles (staus)

### Particle properties
spcFileName = "$DECFILESROOT/lhafiles/GMSB_mtau_100GeV.LHspc"
specialSusyParticles = [ "1000015","1000039" ]

import sys,os
sys.path.append(os.path.expandvars("$DECFILESROOT/scripts/"))

Generation().Special.Pythia8Production.Commands += [
      "SLHA:file            %s" % spcFileName
    , "SLHA:useDecayTable = true"
    ]

from Configurables import LHCb__ParticlePropertySvc
LHCb__ParticlePropertySvc().Particles += [
      "~tau_1- 879  1000015  -1.0 %e %e unknown  1000015 0.00000000" % (100, 3.5e-8),
      "~tau_1+ 880 -1000015   1.0 %e %e unknown -1000015 0.00000000" % (100, 3.5e-8),
      "~Gravitino 892  1000039  0.0 %e %e unknown  1000039 0.00000000" % (80, 1e08),
    ]
EndInsertPythonCode
from Configurables import LHCb__ParticlePropertySvc