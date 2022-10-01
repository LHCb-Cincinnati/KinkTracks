/*****************************************************************************\
* (c) Copyright 2000-2020 CERN for the benefit of the LHCb Collaboration      *
*                                                                             *
* This software is distributed under the terms of the GNU General Public      *
* Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   *
*                                                                             *
* In applying this licence, CERN does not waive the privileges and immunities *
* granted to it by virtue of its status as an Intergovernmental Organization  *
* or submit itself to any jurisdiction.                                       *
\*****************************************************************************/
// $Id: GiGaPhysUnknownParticles.cpp,v 1.6 2009-10-20 07:35:07 marcin Exp $
// Include files

// from Gaudi
#include "GaudiKernel/PhysicalConstants.h"

// G4
#include "G4UnknownParticle.hh"
#include "G4ProcessManager.hh"
#include "G4ParticleTable.hh"

// local
#include "G4BcMesonMinus.h"
#include "G4BcMesonPlus.h"
#include "G4AntiLambdabZero.h"
#include "G4LambdabZero.h"
#include "G4AntiXibZero.h"
#include "G4XibZero.h"
#include "G4XibMinus.h"
#include "G4XibPlus.h"
#include "G4OmegabMinus.h"
#include "G4OmegabPlus.h"
#include "G4AntiXiccStarMinus.h"
#include "G4XiccStarPlus.h"
#include "G4AntiXiccMinus.h"
#include "G4XiccPlus.h"
#include "G4AntiXibcMinus.h"
#include "G4XibcPlus.h"
#include "G4AntiXibcZero.h"
#include "G4XibcZero.h"
#include "G4AntiXiccMinusMinus.h"
#include "G4XiccPlusPlus.h"
#include "G4Neutralino.h"
#include "G4Neutralino2.h"
#include "G4CharginoMinus.h"
#include "G4CharginoPlus.h"
#include "G4AntiOmegaccMinus.h"
#include "G4OmegaccPlus.h"
#include "G4AntiOmegabcZero.h"
#include "G4OmegabcZero.h"
#include "G4Gravitino.h"
#include "G4StauPlus.h"
#include "G4StauMinus.h"

//
#include "GiGaPhysUnknownParticles.h"

//-----------------------------------------------------------------------------
// Implementation file for class : GiGaPhysUnknownParticles
//-----------------------------------------------------------------------------

// Declaration of the Tool Factory
DECLARE_COMPONENT( GiGaPhysUnknownParticles )

//=============================================================================
// Standard constructor, initializes variables
//=============================================================================
GiGaPhysUnknownParticles::GiGaPhysUnknownParticles
( const std::string& type   ,
  const std::string& name   ,
  const IInterface*  parent )
  : GiGaPhysConstructorBase( type , name , parent ) 
{ }

//=============================================================================
// Destructor
//=============================================================================
GiGaPhysUnknownParticles::~GiGaPhysUnknownParticles(){}

//=============================================================================
// ConstructParticle
//=============================================================================
void GiGaPhysUnknownParticles::ConstructParticle()
{
  G4BcMesonMinus::BcMesonMinusDefinition() ;
  G4BcMesonPlus::BcMesonPlusDefinition() ;  
  G4XibMinus::XibMinusDefinition() ;
  G4XibPlus::XibPlusDefinition() ;  
  G4OmegabMinus::OmegabMinusDefinition() ;
  G4OmegabPlus::OmegabPlusDefinition() ;  
  G4AntiLambdabZero::AntiLambdabZeroDefinition();
  G4LambdabZero::LambdabZeroDefinition();
  G4AntiXibZero::AntiXibZeroDefinition();
  G4XibZero::XibZeroDefinition();
  G4AntiXiccStarMinus::AntiXiccStarMinusDefinition();
  G4XiccStarPlus::XiccStarPlusDefinition();
  G4AntiXiccMinus::AntiXiccMinusDefinition();
  G4XiccPlus::XiccPlusDefinition();
  G4AntiXibcMinus::AntiXibcMinusDefinition();
  G4XibcPlus::XibcPlusDefinition();
  G4AntiXibcZero::AntiXibcZeroDefinition();
  G4XibcZero::XibcZeroDefinition();
  G4AntiXiccMinusMinus::AntiXiccMinusMinusDefinition();
  G4XiccPlusPlus::XiccPlusPlusDefinition();
  G4Neutralino::NeutralinoDefinition();
  G4Neutralino2::Neutralino2Definition();
  G4CharginoPlus::CharginoPlusDefinition();
  G4CharginoMinus::CharginoMinusDefinition();
  G4OmegaccPlus::OmegaccPlusDefinition(); 
  G4AntiOmegaccMinus::AntiOmegaccMinusDefinition();
  G4OmegabcZero::OmegabcZeroDefinition();
  G4AntiOmegabcZero::AntiOmegabcZeroDefinition(); 
  G4Gravitino::GravitinoDefinition(); 
  G4StauPlus::StauPlusDefinition();
  G4StauMinus::StauMinusDefinition();

 
  G4UnknownParticle::UnknownParticleDefinition();  
}

//=============================================================================
// ConstructProcess
//=============================================================================
void GiGaPhysUnknownParticles::ConstructProcess()
{
  auto theParticleIterator = GetParticleIterator();
  theParticleIterator -> reset() ;
  while ( (*theParticleIterator)() ) {
    G4ParticleDefinition * particle = theParticleIterator -> value() ;
    G4ProcessManager     * pmanager = particle -> GetProcessManager() ;
//    if ( m_decayProcess.IsApplicable( *particle ) ) {
//      debug() << "### Decays for " << particle -> GetParticleName() 
//              << endmsg ;
//      pmanager -> AddProcess( &m_decayProcess ) ;
      // set ordering for PostStepDoIt and AtRestDoIt
//      pmanager -> SetProcessOrdering( &m_decayProcess , idxPostStep ) ;
//      pmanager -> SetProcessOrdering( &m_decayProcess , idxAtRest   ) ;
//      pmanager -> DumpInfo() ;      
//    }
    if ( particle -> GetParticleName() == "unknown" ) {
      pmanager -> AddProcess( &m_unknownDecay ) ;
      pmanager -> SetProcessOrdering( &m_unknownDecay , idxPostStep ) ;
      debug() << "### Unknown Decays for " << particle -> GetParticleName() 
              << endmsg ;
      if ( msgLevel( MSG::DEBUG) ) 
        pmanager -> DumpInfo() ;
    }
  }
}

//=============================================================================