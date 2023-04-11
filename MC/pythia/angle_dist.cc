#include "Pythia8/Pythia.h"
#include <iostream>
#include <vector>
#include <iostream>
#include <cmath>
#include <fstream>
#include <regex>
#include <string>
#include "utils.h"

using namespace Pythia8;



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
    Hist angel2D_phi("kink angle (phi)", 50., -180, 180);
    Hist angel2D_theta("kink angle (theta)", 50., -180, 180);

// Begin event loop.
for (int iEvent = 0; iEvent < nEvents; ++iEvent) {
    if (iEvent % 1000 == 0) std::cout << "Event: " << iEvent << std::endl;
    if (!pythia.next()) continue;

        // Loop over all stau decays in the event.
        for (int i = 0; i < event.size(); ++i) {
            int idAbs = event[i].idAbs(); // call particles by ID
            double eta = event[i].eta(); //  eta (pseudorapidity)

            if (idAbs == stau || idAbs == -stau) { // if the particle is stau or anti stau
                // Find the mother(s) of the stau
                int iMother1 = event[i].mother1();
                int iMother2 = event[i].mother2();
                
                // Check if the mother is not a stau
                if ((iMother1 == 0 || event[iMother1].idAbs() != stau) &&
                    (iMother2 == 0 || event[iMother2].idAbs() != stau)) {
                    n_staus++;
                    if (eta > 1.9 && eta < 5.1) {  // if the particle is in the LHCb eta range
                        n_staus_accepted++;
                        // Find the daughters of the stau.
                        int iDau1 = event[i].daughter1();
                        int iDau2 = event[i].daughter2();

                        // Check if the decay is valid (stau decays to tau and gravitino)
                        if (is_valid_decay(event[iDau1].id(), event[iDau2].id())) {
                            double theta_stau = event[i].theta();
                            double theta_tau = (event[iDau1].idAbs() == 15) ? event[iDau1].theta() : event[iDau2].theta();
                            double phi_stau = event[i].phi();
                            double phi_tau = (event[iDau1].idAbs() == 15) ? event[iDau1].phi() : event[iDau2].phi();

                            double kink_ang = kink3d_angle(theta_stau, theta_tau, phi_stau, phi_tau);
                            double kink_ang_phi = kink_angle_phi(phi_stau, phi_tau);
                            double kink_ang_theta = kink_angle_theta(theta_stau, theta_tau);
                            //cout << "Kink angle: " << kink_ang << endl;
                            angel3D.fill(kink_ang);
                            angel2D_phi.fill(kink_ang_phi);
                            angel2D_theta.fill(kink_ang_theta);

                            // Count the decay products
                            // gravitino
                            if (event[iDau1].idAbs() == 1000039 || event[iDau2].idAbs() == 1000039) {
                                ndecay_g_accepted++;
                            }
                            // tau
                            if (event[iDau1].idAbs() == 15 || event[iDau2].idAbs() == 15) {
                                ndecay_s_accepted++;
                            }
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


int stau_mass = get_stau_mass_from_cmnd_file("kink.cmnd");
int stau_length = get_stau_length_from_cmnd_file("kink.cmnd");

if (stau_mass == 0) {
    std::cerr << "Could not find Stau mass in kink.cmnd" << std::endl;
} else {
    if (stau_length == 0) {
        std::cerr << "Could not find Stau length (ctau) in kink.cmnd" << std::endl;
    }
    std::stringstream title;
    title << "Stau (" << stau_mass << " GeV), ctau = " << stau_length << " mm";

    HistPlot hpl("DecayAngle");
    hpl.frame("DecayAnglePlot_" + std::to_string(stau_length) + "mm", "Decay (kink) Angle Distribution", "angle (degrees)", "Entries");
    hpl.add(angel3D, "h,red", title.str());
    hpl.plot();

    HistPlot hpl_phi("DecayAngle_phi");
    hpl_phi.frame("DecayAnglePlot_phi_" + std::to_string(stau_length) + "mm", "Decay (kink) Angle Distribution (phi)", "angle (degrees)", "Entries");
    hpl_phi.add(angel2D_phi, "h,red", title.str());
    hpl_phi.plot();

    HistPlot hpl_theta("DecayAngle_theta");
    hpl_theta.frame("DecayAnglePlot_theta_" + std::to_string(stau_length) + "mm", "Decay (kink) Angle Distribution (theta)", "angle (degrees)", "Entries");
    hpl_theta.add(angel2D_theta, "h,red", title.str());
    hpl_theta.plot();
}


    // Done.
    return 0;
}

