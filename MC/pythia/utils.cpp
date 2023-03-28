/*
Name: utils.h
Description: This file contains the utility functions used in the pythia analysis (src)
Author: Mohamed Elashri <mohamed.elashri@cern.ch>
Date: 2022-06-09
*/
#include "utils.h"
#include "Pythia8/Pythia.h"
#include <cmath>
#include <iostream>
#include <vector>
#include <iostream>
#include <fstream>
#include <regex>
#include <string>


using namespace Pythia8;

// This function checks whether the decay of a particle with id1 into a particle with id2 is valid
// It checks whether the particle with id1 is a tau, gravitino and the particle with id2 is a tau or gravitino
// It returns true if the decay is valid, and false otherwise
// Function Name: is_valid_decay
// Parameters: id1, id2
// Return Value: true or false
bool is_valid_decay(int id1, int id2) {
    if (abs(id1) == 23 || abs(id1) == 24 || abs(id1) == 25) {
        if (abs(id2) == 11 || abs(id2) == 13 || abs(id2) == 15 || abs(id2) == 22) {
            return true;
        }
    }
    return false;
}


// this function calculates the kink angle for a tau lepton and a stau lepton
// the input parameters are the theta and phi angles for both the tau and the stau
// the output is the 3D kink angle in degrees
// Function Name: kink3d_angle
// Parameters: theta_stau, theta_tau, phi_stau, phi_tau
// Return Value: kink angle
double kink3d_angle(double theta_stau, double theta_tau, double phi_stau, double phi_tau) {
    double kink_angle = 0.0;

    if (std::sin(theta_stau) == 0.0 && std::sin(theta_tau) == 0.0) {
        // the case where the stau and tau are at the same place in the detector
        kink_angle = 0.0;
    } else if (std::sin(theta_stau) == 0.0 || std::sin(theta_tau) == 0.0) {
        // the case where the stau or tau are at the same place in the detector
        kink_angle = 90.0;
    } else {
        kink_angle = std::acos(std::sin(theta_stau) * std::sin(theta_tau) * (std::cos(phi_stau) * std::cos(phi_tau) + std::sin(phi_stau) * std::sin(phi_tau)) + std::cos(theta_stau) * std::cos(theta_tau));
        // convert the kink angle to degrees
        kink_angle = kink_angle * 180 / M_PI;
    }

    return kink_angle;
}



// Calculates the decay length of a particle in the event record
// Function Name: decay_length
// Parameters: event, index
// Return Value: decay length
double decay_length(const Pythia8::Event& event, int index) {
    // Check if particle exists
    if (index < 0 || index >= event.size()) {
        return -1;
    }

    // Check if particle has decayed
    if (!event[index].isFinal()) {
        return -1;
    }

    // Check if particle has a decay vertex
    if (!event[index].hasDecayVertex()) {
        return -1;
    }

    // Calculate decay length
    return event[index].vDec().pAbs();
}



// This function takes the phi angle of a stau and a tau and
// returns the difference between the two angles in degrees.
// If the angles are in the range [0,2*pi], then the return
// value will be in the range [-180,180]. The function
// accounts for the fact that the phi angle is periodic
// and that the angles may be outside the range [0,2*pi].
// Function Name: kink_angle_phi
// Parameters: phi_stau, phi_tau
// Return Value: delta_phi

double kink_angle_phi(double phi_stau, double phi_tau) {
    // The phi angle difference between the tau and stau
    double delta_phi = phi_tau - phi_stau;
    // Normalize the angle difference to be within the range [-pi, pi]
    while (delta_phi > M_PI) delta_phi -= 2 * M_PI;
    while (delta_phi < -M_PI) delta_phi += 2 * M_PI;
    // Return the angle difference in degrees
    return delta_phi * 180 / M_PI;
}





//This function calculates the angle between the stau and tau tracks. This is done by comparing
//the azimuthal angle of the stau and tau tracks. The azimuthal angle is calculated by taking the
//difference in the polar angles of the stau and tau tracks. The result is then converted to degrees
//and returned to the calling function.
//Function Name: kink_angle_theta
//Parameters: theta_stau, theta_tau
//Return Value: delta_theta
double kink_angle_theta(double theta_stau, double theta_tau) {
    double delta_theta = theta_tau - theta_stau;
    delta_theta = delta_theta * 180 / M_PI;
    if (delta_theta > 180) {
        delta_theta = delta_theta - 360;
    }
    else if (delta_theta < -180) {
        delta_theta = delta_theta + 360;
    }
    return delta_theta;
}


int get_stau_mass_from_cmnd_file(const std::string &cmnd_filename) {
    // Read the stau mass from the cmnd file.
    // The cmnd file is a text file with a line that looks like
    // SLHA/GMSB_mtau_100GeV.slha
    // and we want to find the number 100.
    // Function Name: get_stau_mass_from_cmnd_file
    // Parameters: cmnd_filename
    // Return Value: stau mass
    std::ifstream cmnd_file(cmnd_filename);
    std::string line;
    int num = 0;

    if (cmnd_file.is_open()) {
        std::regex slha_regex("SLHA\\/GMSB_mtau_([0-9]+)GeV\\.slha");

        while (getline(cmnd_file, line)) {
            std::smatch matches;
            if (std::regex_search(line, matches, slha_regex) && matches.size() > 1) {
                num = std::stoi(matches[1].str());
                break;
            }
        }
        cmnd_file.close();
    } else {
        throw std::invalid_argument("Unable to open file " + cmnd_filename);
    }

    return num;
}




// This function returns the stau lifetime as stored in the cmnd file.
// It assumes that the lifetime is stored as a line of the form
// 1000015:tau0 = 1000
// where 1000 is the lifetime in mm.
// The function throws an exception if it cannot find the lifetime.
// Function Name: get_stau_length_from_cmnd_file
// Parameters: cmnd_filename
// Return Value: stau lifetime
int get_stau_length_from_cmnd_file(const std::string &cmnd_filename) {
    std::ifstream cmnd_file(cmnd_filename);
    std::string line;
    int stau_length = 0;

    if (!cmnd_file.is_open()) {
        throw std::runtime_error("Unable to open file " + cmnd_filename);
    }

    std::regex ctau_regex("1000015:tau0\\s+=\\s+([0-9]+)");

    while (getline(cmnd_file, line)) {
        std::smatch matches;
        if (std::regex_search(line, matches, ctau_regex) && matches.size() > 1) {
            stau_length = std::stoi(matches[1].str());
            break;
        }
    }
    cmnd_file.close();

    if (stau_length == 0) {
        throw std::runtime_error("No stau lifetime found in file " + cmnd_filename);
    }

    return stau_length;
}