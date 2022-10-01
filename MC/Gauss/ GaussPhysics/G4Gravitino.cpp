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

#include <fstream>
#include <iomanip>

#include "G4Gravitino.h"
#include "G4ParticleTable.hh"

// ###################################################################### 
// ###                       Gravitino                                ###
// ######################################################################

G4Gravitino* G4Gravitino::theInstance = 0 ;

G4Gravitino * G4Gravitino:: Definition()
{
      if (theInstance !=0) return theInstance;
  const G4String name = "s_G";
  // search in particle table
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
   anInstance = new G4ParticleDefinition(
                 name,    3.6e-19*CLHEP::GeV,       3.12e-13*CLHEP::GeV,         0.0, 
		    +3/2,              +1,             0,          
		    0,               0,             0,             
		    "supersymmetric",               0,             0,          1000039,
		    true,             0.0,          NULL,
		    false,            "Gravitino"
              );
  }
  theInstance = reinterpret_cast<G4Gravitino*>(anInstance);
  return theInstance;
}

G4Gravitino*  G4Gravitino::GravitinoDefinition(){return Definition();}
G4Gravitino*  G4Gravitino::Gravitino(){return Definition();}