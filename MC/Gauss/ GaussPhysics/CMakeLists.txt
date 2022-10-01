###############################################################################
# (c) Copyright 2000-2020 CERN for the benefit of the LHCb Collaboration      #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
#[=======================================================================[.rst:
Sim/GaussPhysics
----------------
#]=======================================================================]

gaudi_add_module(GaussPhysics
    SOURCES
        src/G4AntiLambdabZero.cpp
        src/G4AntiOmegabcZero.cpp
        src/G4AntiOmegaccMinus.cpp
        src/G4AntiXibZero.cpp
        src/G4AntiXibcMinus.cpp
        src/G4AntiXibcZero.cpp
        src/G4AntiXiccMinus.cpp
        src/G4AntiXiccMinusMinus.cpp
        src/G4AntiXiccStarMinus.cpp
        src/G4BcMesonMinus.cpp
        src/G4BcMesonPlus.cpp
        src/G4CharginoMinus.cpp
        src/G4CharginoPlus.cpp
        src/G4HiddenValley.cpp
        src/G4Higgses.cpp
        src/G4LambdabZero.cpp
        src/G4Neutralino.cpp
        src/G4Neutralino2.cpp
        src/G4OmegabMinus.cpp
        src/G4OmegabPlus.cpp
        src/G4OmegabcZero.cpp
        src/G4OmegaccPlus.cpp
        src/G4XibMinus.cpp
        src/G4XibPlus.cpp
        src/G4XibZero.cpp
        src/G4XibcPlus.cpp
        src/G4XibcZero.cpp
        src/G4XiccPlus.cpp
        src/G4XiccPlusPlus.cpp
        src/G4XiccStarPlus.cpp
        src/GaussPhysics_factories.cpp
        src/GiGaHiddenValleyParticles.cpp
        src/GiGaHiggsParticles.cpp
        src/GiGaPhysUnknownParticles.cpp
        src/G4Gravitino.cpp
        src/G4StauPlus.cpp
        src/G4StauMinus.cpp
    LINK
        Gauss::GaussToolsLib
        Geant4::G4LHCblists
        Geant4::G4physicslists
)
