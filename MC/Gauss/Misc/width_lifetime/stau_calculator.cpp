// stau_calculator.cpp
// Author: Mohamed Elashri <mail@elashri.com>
// Date: 2023-04-13
// Compile: g++ -o stau_calculator stau_calculator.cpp
// Usage: ./stau_calculator <lifetime_in_ns>
// i.e:
// ./stau_calculator width 1GeV
// ./stau_calculator width 1MeV
// ./stau_calculator lifetime 1s
// ./stau_calculator lifetime 1ns

// stau_calculator.cpp

#include <iostream>
#include <cstdlib>
#include <iomanip>
#include <stdexcept>
#include <string>
#include <regex>

// Physical constants
const double hbar_Planck = 6.582119569e-16; // eV s, reduced Planck constant
const double MeV = 1.0e6;                  // eV, 1 MeV in eV
const double GeV = 1.0e9;                  // eV, 1 GeV in eV
const double s = 1.0;                      // s, 1 second in s
const double ns = 1.0e-9;                  // s, 1 nanosecond in s

void calculateWidthAndLifetime(double inputWidth, double inputLifetime_s, double inputLifetime_ns, double& outputWidth, double& outputLifetime_s, double& outputLifetime_ns) {
    if (inputWidth > 0) {
        outputWidth = inputWidth;
        outputLifetime_s = hbar_Planck / inputWidth;
        outputLifetime_ns = outputLifetime_s / ns; // Convert output lifetime to ns
    } else if (inputLifetime_s > 0) {
        outputLifetime_s = inputLifetime_s;
        outputWidth = hbar_Planck / inputLifetime_s;
        outputLifetime_ns = outputLifetime_s / ns; // Convert output lifetime to ns
    } else if (inputLifetime_ns > 0) {
        outputLifetime_ns = inputLifetime_ns;
        outputLifetime_s = inputLifetime_ns * ns;
        outputWidth = hbar_Planck / outputLifetime_s;
    } else {
        outputWidth = -1;
        outputLifetime_s = -1;
        outputLifetime_ns = -1;
    }
}

int main(int argc, char* argv[]) {
    if (argc < 3) {
        std::cerr << "Usage: " << argv[0] << " <type: width | lifetime> <value_with_unit>" << std::endl;
        return 1;
    }

    std::string inputType(argv[1]);
    std::string inputValueWithUnit(argv[2]);

    std::regex valueRegex("(\\d+(\\.\\d+)?)([a-zA-Z]+)");
    std::smatch match;

    if (!std::regex_match(inputValueWithUnit, match, valueRegex)) {
        std::cerr << "Error: invalid input value format" << std::endl;
        return 1;
    }

    double inputValue = std::stod(match[1]);
    std::string unit = match[3];

    double inputWidth = -1;
    double inputLifetime_s = -1;
    double inputLifetime_ns = -1;

        if (inputType == "width") {
            if (unit == "GeV") {
                inputWidth = inputValue * GeV;
            } else if (unit == "MeV") {
                inputWidth = inputValue * MeV;
            } else {
                std::cerr << "Error: invalid width unit" << std::endl;
                return 1;
        }
        } 
        
        else if (inputType == "lifetime") {
        if (unit == "s") {
            inputLifetime_s = inputValue;
        } else if (unit == "ns") {
            inputLifetime_ns = inputValue;
        } else {
            std::cerr << "Error: invalid lifetime unit" << std::endl;
            return 1;
        }
        } 
    
        else {
            std::cerr << "Error: invalid input type" << std::endl;
            return 1;
        }

    double outputWidth, outputLifetime_s, outputLifetime_ns;

    calculateWidthAndLifetime(inputWidth, inputLifetime_s, inputLifetime_ns, outputWidth, outputLifetime_s, outputLifetime_ns);

    std::cout << "Stau width in MeV: " << outputWidth / MeV << " MeV" << std::endl;
    std::cout << "Stau width in GeV: " << outputWidth / GeV << " GeV" << std::endl;
    std::cout << "Stau lifetime in s: " << outputLifetime_s << " s" << std::endl;
    std::cout << "Stau lifetime in ns: " << outputLifetime_ns << " ns" << std::endl;

    return 0;
}

