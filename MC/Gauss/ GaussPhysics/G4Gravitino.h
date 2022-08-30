
#ifndef G4Gravitino_h 
#define G4Gravitino_h 1 

#include "Geant4/globals.hh"
#include "Geant4/G4ios.hh"
#include "Geant4/G4ParticleDefinition.hh"

/** @class  G4Gravitino G4Gravitino.h  *
 * 
 *  Define the Gravitino LSP in Geant
 * 
 *  @author Mohamed Elashri
 * 
 *  @date   2022-08-23
 */

// ###################################################################### 
// ###                       Gravitino                                ###
// ######################################################################

class G4Gravitino : public G4ParticleDefinition
{
 private:
  static G4Gravitino * theInstance ;
  G4Gravitino( ) { }
  ~G4Gravitino( ) { }

 public:
   static G4Gravitino* Definition();
   static G4Gravitino* GravitinoDefinition();
   static G4Gravitino* Gravitino();
};

#endif
