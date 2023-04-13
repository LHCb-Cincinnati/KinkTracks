// stau_calculator.cpp
// Author: Mohamed Elashri <mail@elashri.com>
// Date: 2023-04-13
// Compile: g++ -o stau_calculator stau_calculator.cpp
// Usage: ./stau_calculator <lifetime_in_ns>
//         i.e ./stau_calculator 6.68e-1

#include <iostream>
#include <cstdlib>
#include <iomanip>

// Physical constants
const double hbar_Planck = 6.582119569e-16; // eV s, reduced Planck constant
const double MeV = 1.0e6;                  // eV, 1 MeV in eV
const double GeV = 1.0e9;                  // eV, 1 GeV in eV
const double s = 1.0;                      // s, 1 second in s
const double ns = 1.0e-9;                  // s, 1 nanosecond in s

void calculateWidthAndLifetime(double inputWidth, double inputLifetime_ns, double& outputWidth, double& outputLifetime_ns) {
    // Convert input lifetime from ns to s
    double inputLifetime = inputLifetime_ns * ns;

    // Check if width is given
    if (inputWidth > 0) {
        outputWidth = inputWidth;
        // Convert output lifetime to ns
        outputLifetime_ns = hbar_Planck / inputWidth / ns;
    // Check if lifetime is given
    } else if (inputLifetime > 0) {
        outputLifetime_ns = inputLifetime_ns;
        outputWidth = hbar_Planck / inputLifetime;
    // Neither width nor lifetime is given
    } else {
        outputWidth = -1;
        outputLifetime_ns = -1;
    }
}

// Main function
    // Start with a string of input lifetime.
    // The input lifetime is a string from the command line.
    // This string must be converted to a long integer.
    // The long integer is the input lifetime in nanoseconds.
    long input_lifetime_ns = 0;
    try {
        input_lifetime_ns = std::stol(argv[1]);
    } catch (...) {
        std::cerr << "Error: invalid input lifetime: " << argv[1] << std::endl;
        return 1;
    }

    // Check if the input lifetime is negative.
    if (input_lifetime_ns < 0) {
        std::cerr << "Error: negative input lifetime: " << argv[1] << std::endl;
        return 1;
    }

    // Check if the input lifetime is zero.
    // Warn the user that this might not be what they intended.
    if (input_lifetime_ns == 0) {
        std::cerr << "Warning: zero input lifetime: " << argv[1] << std::endl;
    }
    double inputWidth = -1;
    double inputLifetime_ns = std::atof(argv[1]); // Parse input lifetime value in ns from command-line argument
    double outputWidth, outputLifetime_ns;

    calculateWidthAndLifetime(inputWidth, inputLifetime_ns, outputWidth, outputLifetime_ns);

    std::cout << "Stau width in MeV: " << outputWidth / MeV << " MeV" << std::endl;
    std::cout << "Stau width in GeV: " << outputWidth / GeV << " GeV" << std::endl;
    std::cout << "Stau lifetime: " << outputLifetime_ns << " ns" << std::endl;

    return 0;
}