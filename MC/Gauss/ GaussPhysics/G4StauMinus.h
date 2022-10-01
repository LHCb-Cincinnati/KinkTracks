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
// $Id: G4StauMinus.h,v 1.1 2008-11-27 16:02:08 robbep Exp $

#ifndef G4StauMinus_h
#define G4StauMinus_h 1 

#include "globals.hh"
#include "G4ios.hh"
#include "G4ParticleDefinition.hh"

/** @class  G4StauMinus G4StauMinus.h 
 *  
 *  Define the Stau minus in Geant
 * 
 *  @author Mohamed Elashri
 *  @date   2022-08-30
 */

// ######################################################################
// ###                       StauMinus                            ###
// ######################################################################

class G4StauMinus : public G4ParticleDefinition
{
 private:
  static G4StauMinus * theInstance ;
  G4StauMinus( ) { }
  ~G4StauMinus( ) { }

 public:
   static G4StauMinus* Definition();
   static G4StauMinus* StauMinusDefinition();
   static G4StauMinus* StauMinus();
};

#endif