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

#ifndef G4Gravitino_h 
#define G4Gravitino_h 1 

#include "globals.hh"
#include "G4ios.hh"
#include "G4ParticleDefinition.hh"

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