#include <fstream>
#include <iomanip>

#include "G4Gravitino.h"
#include "Geant4/G4ParticleTable.hh"

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

