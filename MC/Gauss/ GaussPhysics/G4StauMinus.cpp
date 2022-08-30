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
// $Id: G4StauMinus.cpp,v 1.2 2008-11-27 20:18:13 robbep Exp $

#include <fstream>
#include <iomanip>

#include "G4StauMinus.h"
#include "Geant4/G4ParticleTable.hh"

// ######################################################################
// ###                     StauMinus                                  ###
// ######################################################################

G4StauMinus * G4StauMinus::theInstance = 0 ;

G4StauMinus * G4StauMinus::Definition()
{

  if (theInstance !=0) return theInstance;
  const G4String name = "s_tau_minus_L";
  // search in particle table]
  G4ParticleTable* pTable = G4ParticleTable::GetParticleTable();
  G4ParticleDefinition* anInstance = pTable->FindParticle(name);
  if (anInstance ==0)
  {
  // create particle
  //
  //    Arguments for constructor are as follows
  //               name             mass          width         charge
  //             2*spin           parity  C-conjugation
  //          2*Isospin       2*Isospin3       G-parity
  //               type    lepton number  baryon number   PDG encoding
  //             stable         lifetime    decay table
  //             shortlived      subType    anti_encoding
    anInstance = 
      new G4ParticleDefinition( name , 100.00*CLHEP::GeV, 2.73e-13*CLHEP::GeV, -1.*CLHEP::eplus, 
                                1,              0,             0,
                                0,              0,             0,
                                "supersymmetric", 0,  0, 1000015,
                                false,     6.68e-1*CLHEP::ns,      NULL,
                                false, "StauMinus" );
  }
  theInstance = reinterpret_cast<G4StauMinus*>(anInstance);
  return theInstance;
}

G4StauMinus*  G4StauMinus::StauMinusDefinition(){return Definition();}
G4StauMinus*  G4StauMinus::StauMinus(){return Definition();}

