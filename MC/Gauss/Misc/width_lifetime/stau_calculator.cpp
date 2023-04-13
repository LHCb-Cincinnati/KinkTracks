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
    double inputLifetime = inputLifetime_ns * ns; // Convert input lifetime from ns to s

    if (inputWidth > 0) {
        outputWidth = inputWidth;
        outputLifetime_ns = hbar_Planck / inputWidth / ns; // Convert output lifetime to ns
    } else if (inputLifetime > 0) {
        outputLifetime_ns = inputLifetime_ns;
        outputWidth = hbar_Planck / inputLifetime;
    } else {
        outputWidth = -1;
        outputLifetime_ns = -1;
    }
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cerr << "Usage: " << argv[0] << " <input_lifetime_ns>" << std::endl;
        return 1;
    }

    // Main function
    long input_lifetime_ns = 0;
    try {
        input_lifetime_ns = std::stol(argv[1]);
    } catch (const std::invalid_argument& e) {
        std::cerr << "Error: invalid input lifetime: " << argv[1] << std::endl;
        return 1;
    } catch (const std::out_of_range& e) {
        std::cerr << "Error: input lifetime out of range: " << argv[1] << std::endl;
        return 1;
    }

    if (input_lifetime_ns < 0) {
        std::cerr << "Error: negative input lifetime: " << argv[1] << std::endl;
        return 1;
    }

    if (input_lifetime_ns == 0) {
        std::cerr << "Warning: zero input lifetime: " << argv[1] << std::endl;
    }

    double inputWidth = -1;
    double outputWidth, outputLifetime_ns;

    calculateWidthAndLifetime(inputWidth, static_cast<double>(input_lifetime_ns), outputWidth, outputLifetime_ns);

    std::cout << "Stau width in MeV: " << outputWidth / MeV << " MeV" << std::endl;
    std::cout << "Stau width in GeV: " << outputWidth / GeV << " GeV" << std::endl;
    std::cout << "Stau lifetime: " << outputLifetime_ns << " ns" << std::endl;

    return 0;
}