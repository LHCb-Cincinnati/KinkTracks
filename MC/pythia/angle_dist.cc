#include "Pythia8/Pythia.h"
#include <iostream>
#include <vector>
#include <iostream>
#include <cmath>
#include <fstream>
#include <regex>
#include <string>


using namespace Pythia8;

bool is_valid_decay(int id1, int id2) {
    return ((abs(id1) == 15 && abs(id2) == 1000039) || (abs(id1) == 1000039 && abs(id2) == 15));
}

double kink_angle(double theta_stau, double theta_tau, double phi_stau, double phi_tau) {
    double kink_angle = std::acos(std::sin(theta_stau) * std::sin(theta_tau) * (std::cos(phi_stau) * std::cos(phi_tau) + std::sin(phi_stau) * std::sin(phi_tau)) + std::cos(theta_stau) * std::cos(theta_tau));
    // convert the kink angle to degrees
    kink_angle = kink_angle * 180 / M_PI;
    return kink_angle;
}

int main() {
    // Generator
    Pythia pythia;
    Event& event = pythia.event;
    // Read in pythia commands from file.
    pythia.readFile("kink.cmnd");

    // Variables Initialization.
    int ndecay_g_accepted = 0; // number of gravitino decay accepted
    int ndecay_s_accepted = 0; // number of taus decay accepted
    int n_staus = 0; // Total number of staus
    int n_staus_accepted = 0; // Total number of staus in LHCb acceptance

    // Initialize.
    pythia.init();
    int stau = 1000015;
    cout << "Lifetime used [mm] =" << scientific << pythia.particleData.tau0(stau) << endl;
    int nEvents = pythia.mode("Main:numberOfEvents");
    //int nAbort = pythia.mode("Main:timesAllowErrors");
    // Histograms
    Hist angel3D("kink angle", 50., 0, 180);

    // Begin event loop.
    for (int iEvent = 0; iEvent < nEvents; ++iEvent) {
        if (iEvent % 1000 == 0) std::cout << "Event: " << iEvent << std::endl;
        if (!pythia.next()) continue;

        // Loop over all stau decays in the event.
        for (int i = 0; i < event.size(); ++i) {
            int idAbs = event[i].idAbs(); // call particles by ID
            double eta = event[i].eta(); //  eta (pseudorapidity)

            if (idAbs == stau || idAbs == -stau) { // if the particle is stau or anti stau
                n_staus++;
                if (eta > 1.9 && eta < 5.1) {  // if the particle is in the LHCb eta range
                    n_staus_accepted++;
                    // Find the daughters of the stau.
                    int iDau1 = event[i].daughter1();
                    int iDau2 = event[i].daughter2();

                    // Check if the decay is valid (stau decays to tau and gravitino)
                    if (is_valid_decay(event[iDau1].id(),                     event[iDau2].id())) {
                        double theta_stau = event[i].theta();
                        double theta_tau = (event[iDau1].idAbs() == 15) ? event[iDau1].theta() : event[iDau2].theta();
                        double phi_stau = event[i].phi();
                        double phi_tau = (event[iDau1].idAbs() == 15) ? event[iDau1].phi() : event[iDau2].phi();

                        double kink_ang = kink_angle(theta_stau, theta_tau, phi_stau, phi_tau);
                        cout << "Kink angle: " << kink_ang << endl;
                        ndecay_s_accepted++;
                        angel3D.fill(kink_ang);

                        // Count the decay products
                        if (event[iDau1].idAbs() == 1000039 || event[iDau2].idAbs() == 1000039) {
                            ndecay_g_accepted++;
                        }
                    }
                }
            }
        }
    }

    // Statistics.
    pythia.stat();
    cout << " Number of gravitinos daughters accepted: " << ndecay_g_accepted << endl; // total number of gravitino produced
    cout << " Number of taus daughters accepted: " << ndecay_s_accepted << endl; // total number of taus produced
    cout << "Total number of staus is: " << n_staus << endl;
    cout << "Total number of staus accepted is: " << n_staus_accepted << endl;


    HistPlot hpl("DecayAngle");
    hpl.frame( "DecayAnglePlot", "Decay (kink) Angle Distribution", "angle (degrees)","Entries");
    // in hpl.add read the $num in Stau ($num GeV) from the number in SLHA:file = SLHA/GMSB_mtau_$numGeV.slha from the kink.cmnd file
    std::string cmnd_filename = "kink.cmnd";
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

    if (num != 0) {
        std::stringstream title;
        title << "Stau (" << num << " GeV), ctau = <> mm";
        hpl.add(angel3D, "h,red", title.str());
    } else {
        std::cerr << "Could not find Stau mass in " << cmnd_filename << std::endl;
    }
    hpl.plot();

    // Done.
    return 0;
}

