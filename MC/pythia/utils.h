/*
Name: utils.h
Description: This file contains the utility functions used in the pythia analysis (header)
Author: Mohamed Elashri <mohamed.elashri@cern.ch>
Date: 2022-06-09
*/


#pragma once
#include "Pythia8/Pythia.h"
#include <iostream>
#include <vector>
#include <iostream>
#include <cmath>
#include <fstream>
#include <regex>
#include <string>


using namespace Pythia8;

bool is_valid_decay(int id1, int id2);

double kink3d_angle(double theta_stau, double theta_tau, double phi_stau, double phi_tau);

double kink_angle_phi(double phi_stau, double phi_tau);

double kink_angle_theta(double theta_stau, double theta_tau);

double decay_length(const Pythia8::Event& event, int index);

int get_stau_mass_from_cmnd_file(const std::string &cmnd_filename);

int get_stau_length_from_cmnd_file(const std::string &cmnd_filename);