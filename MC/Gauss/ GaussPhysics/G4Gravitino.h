
#ifndef G4Neutralino_h 
#define G4Neutralino_h 1 

#include "globals.hh" 
#include "G4ios.hh" 
#include "G4ParticleDefinition.hh"

/** @class  G4Neutralino G4Neutralino.h  *
 * 
 *  Define the Neutralino LSP in Geant
 * 
 *  @author Mohamed Elashri
 * 
 *  @date   2022-08-23
 */

// ###################################################################### 
// ###                       Gravitino                                ###
// ######################################################################

class G4Gravitino : public G4particleDefinition

{
    private:
     static G4Gravitino * theInstance ;
        G4Gravitino() { }
        ~G4Gravitino() { }

    public:    
    static G4Gravitino * Definition() ;
    static G4Gravitino * GravitinoDefinition() ;
    static G4Gravitino * Gravitino() ; 
};