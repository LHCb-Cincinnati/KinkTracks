"""
@file

Main configuration file for long-lived kink Tracks analysis

pp->(~tau_1+ -> ~Gravitino  ~tau+)

Concrete dec files can specify a parameter point by setting the SLHA spectrum file

@code
#
# InsertPythonCode
# 
# Generation().Special.Pythia8Production.Commands.append("SLHA:file MyModelSpectrum.slha")
# 
# EndInserPythonCode
#
@endcode

@author Mohamed Elashri <mohamed.elashri@cern.ch>
@date 2022-07-06
"""
__author__ = "Mohamed Elashri <mohamed.elashri@cern.ch>"
__date__ = "2022-07-06"

# ============================================================================
from Configurables import Generation, Special, Pythia8Production, PythiaLSP
gen = Generation() 
gen.addTool( Special )
gen.Special.addTool( Pythia8Production)
gen.Special.KeepOriginalProperties = True
prod = Generation().Special.Pythia8Production

#Pile-up and luminosity
gen.PileUpTool = "FixedLuminosityForRareProcess"


prod.Commands = [
    #"SUSY:all = on",
    "SUSY:qqbar2sleptonantislepton = on",
    "SUSY:qqbar2gluinogluino  = on",
    "Main:timesAllowErrors = 10",
    "SLHA:verbose = 3",
    "SLHA:allowUserOverride =true", # allow overwriting SLHA values
    "1000015:mayDecay = true", # allow stau to decay
    #"1000015:tauCalc = false", # turn off automatic lifetime calculation
    "1000015:tau0 = 100000", # set tau ctau to 100000 mm
    "1000039:mayDecay = false", # prevent gravitino from decaying
    "Print:quiet = off",
    "1000015:oneChannel = 1 1.0 100 1000039 15",
    "HadronLevel:Hadronize = off",
    "PartonLevel:FSR = off"
]


#prod.OutputLevel = DEBUG
# ============================================================================
from Configurables import GaudiSequencer, GaussMonitor__CheckLifeTimeHepMC, GaussMonitor__CheckLifeTimeMC

GenMonitor = GaudiSequencer( "GenMonitor" )
GenMonitor.Members += [
    GaussMonitor__CheckLifeTimeHepMC("HepMCLifeTime",
        Particles = [
            "~tau_1-" ,
            "B0" , "B_s0" , "B+" , "B_c+" , "Lambda_b0" ,
            "D0" , "D+" , "D_s+" ,  "Lambda_c+"
        ]
    )
]
SimMonitor = GaudiSequencer( "SimMonitor" )
SimMonitor.Members += [
    GaussMonitor__CheckLifeTimeMC("MCLifeTime",
        Particles = [
            "~tau_1-" ,
            "B0" , "B_s0" , "B+" , "B_c+" , "Lambda_b0" ,
            "D0" , "D+" , "D_s+" ,  "Lambda_c+"
        ]
    )
]
# ============================================================================
from Configurables import GaudiSequencer, GaussMonitor__CheckLifeTimeHepMC, GaussMonitor__CheckLifeTimeMC

GenMonitor = GaudiSequencer( "GenMonitor" )
GenMonitor.Members += [
    GaussMonitor__CheckLifeTimeHepMC("HepMCLifeTime",
        Particles = [
            "~tau_1-" ,
            "B0" , "B_s0" , "B+" , "B_c+" , "Lambda_b0" ,
            "D0" , "D+" , "D_s+" ,  "Lambda_c+"
        ]
    )
]
SimMonitor = GaudiSequencer( "SimMonitor" )
SimMonitor.Members += [
    GaussMonitor__CheckLifeTimeMC("MCLifeTime",
        Particles = [
            "~tau_1-" ,
            "B0" , "B_s0" , "B+" , "B_c+" , "Lambda_b0" ,
            "D0" , "D+" , "D_s+" ,  "Lambda_c+"
        ]
    )
]
# ============================================================================
importOptions("$DECFILESROOT/options/susy.py")