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
    
    """
    if mother and daughter:
        if (mother.particleID().pid() == 1000015 or mother.particleID().pid() == -1000015) and (
            daughter.particleID().pid() == 15 or daughter.particleID().pid() == -15
        ):
            if mother.endVertices() and len(mother.endVertices()) > 0:
                other_daughter = [
                    child for child in mother.endVertices()[0].products() if child != daughter
                ]
                if other_daughter and other_daughter[0].particleID().pid() == 1000039:
                    return True
    return False


def decay_length_from_vertices(production_vertex, decay_vertex):
    """
    
    """
    position_diff = decay_vertex.position() - production_vertex.position()
    decay_length = position_diff.R()
    return decay_length

def calculate_kink_angle_phi(mother, daughter):
    """
    
    """
    stau_phi = mother.momentum().phi()
    tau_phi = daughter.momentum().phi()
    kink_angle = stau_phi - tau_phi
    # convert the angles to degrees
    kink_angle = kink_angle * 180 / 3.14159265359
    return kink_angle

def calculate_kink_angle_theta(mother, daughter):
    """
    
    """
    stau_theta = mother.momentum().theta()
    tau_theta = daughter.momentum().theta()
    kink_angle = stau_theta - tau_theta
    # convert the angles to degrees
    kink_angle = kink_angle * 180 / 3.14159265359
    return kink_angle

def calculate_3d_kink_angle(mother, daughter):
    """
    
    """
    theta_mother = mother.momentum().theta()
    theta_daughter = daughter.momentum().theta()
    phi_mother = mother.momentum().phi()
    phi_daughter = daughter.momentum().phi()
    
    cos_kink_angle = (math.sin(theta_mother) * math.sin(theta_daughter) * 
                      (math.cos(phi_mother) * math.cos(phi_daughter) + math.sin(phi_mother) * math.sin(phi_daughter)) +
                      math.cos(theta_mother) * math.cos(theta_daughter))
    
    kink_angle = math.acos(cos_kink_angle)
    kink_angle = kink_angle * 180 / 3.14159265359
    return kink_angle
