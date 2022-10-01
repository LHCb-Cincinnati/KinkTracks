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

#ifndef G4StauPlus_h
#define G4StauPlus_h 1 

#include "globals.hh"
#include "G4ios.hh"
#include "G4ParticleDefinition.hh"

/** @class  G4StauPlus G4StauPlus.h
 *
 *  Define the Stau plus in Geant
 *
 *  @author Mohamed Elashri
 *  @date   2022-08-30
 */

// ######################################################################
// ###                       StauPlus                                 ###
// ######################################################################

class G4StauPlus : public G4ParticleDefinition
{
 private:
  static G4StauPlus * theInstance ;
  G4StauPlus( ) { }
  ~G4StauPlus( ) { }

 public:
   static G4StauPlus* Definition();
   static G4StauPlus* StauPlusDefinition();
   static G4StauPlus* StauPlus();
};

#endif