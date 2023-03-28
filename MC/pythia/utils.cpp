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
bool is_valid_decay(int id1, int id2) {
    return ((abs(id1) == 15 && abs(id2) == 1000039) || (abs(id1) == 1000039 && abs(id2) == 15));
}

double kink3d_angle(double theta_stau, double theta_tau, double phi_stau, double phi_tau) {
    double kink_angle = std::acos(std::sin(theta_stau) * std::sin(theta_tau) * (std::cos(phi_stau) * std::cos(phi_tau) + std::sin(phi_stau) * std::sin(phi_tau)) + std::cos(theta_stau) * std::cos(theta_tau));
    // convert the kink angle to degrees
    kink_angle = kink_angle * 180 / M_PI;
    return kink_angle;
}

double decay_length(const Pythia8::Event& event, int index) {
    return event[index].vDec().pAbs();
}

double kink_angle_phi(double phi_stau, double phi_tau) {
    double delta_phi = phi_tau - phi_stau;
    // Normalize the angle difference to be within the range [-pi, pi]
    while (delta_phi > M_PI) delta_phi -= 2 * M_PI;
    while (delta_phi < -M_PI) delta_phi += 2 * M_PI;
    delta_phi = delta_phi * 180 / M_PI;
    return delta_phi;
}

double kink_angle_theta(double theta_stau, double theta_tau) {
    double delta_theta = theta_tau - theta_stau;
    delta_theta = delta_theta * 180 / M_PI;
    return delta_theta;
}

int get_stau_mass_from_cmnd_file(const std::string &cmnd_filename) {
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
        std::cerr << "Unable to open file " << cmnd_filename << std::endl;
    }

    return num;
}

int get_stau_length_from_cmnd_file(const std::string &cmnd_filename) {
    std::ifstream cmnd_file(cmnd_filename);
    std::string line;
    int stau_length = 0;

    if (cmnd_file.is_open()) {
        std::regex ctau_regex("1000015:tau0\\s+=\\s+([0-9]+)");

        while (getline(cmnd_file, line)) {
            std::smatch matches;
            if (std::regex_search(line, matches, ctau_regex) && matches.size() > 1) {
                stau_length = std::stoi(matches[1].str());
                break;
            }
        }
        cmnd_file.close();
    } else {
        std::cerr << "Unable to open file " << cmnd_filename << std::endl;
    }

    return stau_length;
}