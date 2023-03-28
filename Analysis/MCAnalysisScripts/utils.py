'''
Name: utils.py
Description: This is a utils file for defined functions that are used in other scripts. related with kink track search analysis
Author: Mohamed Elashri
Date: 2023-03-28
'''

# General imports
import os
import re
import math
import matplotlib 
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from ROOT import TH1F, TCanvas

# LHCb imports
from Gaudi.Configuration import *
import GaudiPython




def is_valid_decay(mother, daughter):
    """
    This code checks if a decay is valid. 
    The decay is valid if the mother is a stau- or stau+ and the daughter is a tau- or tau+.
    The mother must have an end vertex, and the other daughter must be a gravitino
    The function returns True if the decay is valid, False otherwise
    
    Parameters
    ----------
    mother : Particle
        The BSM mother particle of the decay
    daughter : Particle
        The SM decay product of the decay  
        
    Returns
    ----------
    True if the decay is valid, False otherwise      
    """
    # Check that both mother and daughter exist
    if mother and daughter:
        # Check that the mother is a stau-/stau+ and the daughter is a tau- or tau-
        if abs(mother.particleID().pid()) == 1000015 and abs(daughter.particleID().pid()) == 15:
            # Check that the mother has at least one end vertex
            if mother.endVertices() and len(mother.endVertices()) > 0:
                # Check that the other daughter is a gravintino
                other_daughter = [
                    child for child in mother.endVertices()[0].products() if child != daughter
                ]
                if other_daughter and other_daughter[0].particleID().pid() == 1000039:
                    return True
    return False




def decay_length_from_vertices(production_vertex, decay_vertex):
    """
    Calculates the decay length of a particle from its production and decay
    vertices. The decay length is defined as the distance between the
    production and decay vertices.
    
    Parameters
    ----------
    production_vertex : Vertex
        The production vertex of the particle
    decay_vertex : Vertex
        The decay vertex of the particle
        
    Returns
    -------
    decay_length : float
        The decay length of the particle        
    """
    if production_vertex is None:
        raise ValueError("production_vertex is None")
    if decay_vertex is None:
        raise ValueError("decay_vertex is None")
    position_diff = decay_vertex.position() - production_vertex.position()
    decay_length = position_diff.R()
    return decay_length



def calculate_kink_angle_phi(mother, daughter):
    """
    Calculate the kink angle of a tau lepton in the phi direction.
    
    This code calculates the angle between the tau lepton and the stau. 
    It is calculated in the phi direction. The phi angle is measured 
    with respect to the beam direction (z-axis).
    
    Parameters
    ----------
    mother : Particle
        The stau particle
    daughter : Particle
        The tau lepton particle
    
    Returns
    -------
    kink_angle : float
        The kink angle in the phi direction in degrees
    """
    try:
        stau_phi = mother.momentum().phi()
        tau_phi = daughter.momentum().phi()
        kink_angle = stau_phi - tau_phi
        # convert the angles to degrees
        kink_angle = kink_angle * 180 / 3.14159265359
    except AttributeError:
        kink_angle = -999
    return kink_angle


def calculate_kink_angle_theta(mother, daughter):
    """
    Calculate the kink angle of a tau lepton in the theta direction.
    
    This code calculates the angle between the tau lepton and the stau. 
    It is calculated in the theta direction. The theta angle is measured 
    with respect to the beam direction (z-axis).
    
    Parameters
    ----------
    mother : Particle
        The stau particle
    daughter : Particle
        The tau lepton particle
    
    Returns
    -------
    kink_angle : float
        The kink angle in the theta direction in degrees
    """
    try:
        stau_theta = mother.momentum().theta()
        tau_theta = daughter.momentum().theta()
        kink_angle = stau_theta - tau_theta
        # convert the angles to degrees
        kink_angle = kink_angle * 180 / 3.14159265359
    except:
        kink_angle = -999
    return kink_angle


def calculate_3d_kink_angle(mother, daughter):
    """
    Function to calculate the 3D kink angle between the momentum vectors of two particles.
    This function takes two particles as arguments, and returns the 3D kink angle between their
    momentum vectors. If either particle is missing momentum information, the function returns
    None.
    
    Arguments:
        mother: Particle object representing the mother particle
        daughter: Particle object representing the daughter particle
        
    Returns:
        Float representing the 3D kink angle between the two particles, or None if either particle
        is missing momentum information
    
    The function will return None if any of the following conditions are met:
    * The angle cannot be calculated due to a division by zero error
    * The angle cannot be calculated due to a math domain error
    * The angle cannot be calculated due to a ValueError exception
    * The angle cannot be calculated due to a ZeroDivisionError exception
    * The angle cannot be calculated due to a TypeError exception
    
    """
    try:
        theta_mother = mother.momentum().theta()
        theta_daughter = daughter.momentum().theta()
        phi_mother = mother.momentum().phi()
        phi_daughter = daughter.momentum().phi()
    except:
        return None
    try:
        cos_kink_angle = (math.sin(theta_mother) * math.sin(theta_daughter) * 
                          (math.cos(phi_mother) * math.cos(phi_daughter) + math.sin(phi_mother) * math.sin(phi_daughter)) +
                          math.cos(theta_mother) * math.cos(theta_daughter))
        kink_angle = math.acos(cos_kink_angle)
        kink_angle = kink_angle * 180 / 3.14159265359
    except:
        return None
    return kink_angle


def calculate_3d_kink_angle(mother, daughter):
    """
    
    """
    try:
        theta_mother = mother.momentum().theta()
        theta_daughter = daughter.momentum().theta()
        phi_mother = mother.momentum().phi()
        phi_daughter = daughter.momentum().phi()
    except:
        return None
    try:
        cos_kink_angle = (math.sin(theta_mother) * math.sin(theta_daughter) * 
                          (math.cos(phi_mother) * math.cos(phi_daughter) + math.sin(phi_mother) * math.sin(phi_daughter)) +
                          math.cos(theta_mother) * math.cos(theta_daughter))
        kink_angle = math.acos(cos_kink_angle)
        kink_angle = kink_angle * 180 / 3.14159265359
    except:
        return None
    return kink_angle
