    # @file
#  Options to include to produce stau. This contains pythia
#  commands to be set independently from the model to be used.
#  Must be included from model dependent options.
#
#  @author Neal Gauvin (Gueissaz)
#  @date   2008-10-23
#  @author Mohamed Elashri (melashri)
#  @date   2022-07-06

#Cut Tool options
#Generation.Special.PythiaLSP.LSPCond = 1 ; //LSP in acceptance, Default
from Configurables import Generation, Special, PythiaLSP
from GaudiKernel.SystemOfUnits import GeV, mrad, mm, meter
Generation().addTool( Special )
Generation().Special.addTool( PythiaLSP ) 
Generation().Special.PythiaLSP.LSPID = [ 1000015,-1000015 ] #LSPID
Generation().Special.PythiaLSP.NbLSP = 1 
Generation().Special.PythiaLSP.AtLeast = True
Generation().Special.PythiaLSP.DgtsInAcc = [1000039,15]
Generation().Special.PythiaLSP.LSPCond = 1 #following daughters in acc
Generation().Special.PythiaLSP.OutputLevel = 3
#Generation().Special.PythiaLSP.DistToPVMin = 0*mm
#Generation().Special.PythiaLSP.DistToPVMax = 9500*mm
#Generation().Special.PythiaLSP.EtaMin = 1.8
#Generation().Special.PythiaLSP.EtaMax = 4.9

from Configurables import PythiaProduction

Generation().Special.addTool( PythiaProduction )

# list of particles to be printed using PyList(12)
Generation().Special.PythiaProduction.PDTList = [ 1000015,-1000015 ]

#Pile-up and luminosity
Generation().PileUpTool = "FixedLuminosityForRareProcess"

#set off unwanted processes
from Gaudi.Configuration import importOptions
importOptions( "$DECFILESROOT/options/SwitchOffAllPythiaProcesses.py" )