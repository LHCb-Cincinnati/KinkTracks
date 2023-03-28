#include "Pythia8/Pythia.h"
#include <iostream>
#include <fstream>
#include "utils.h"

using namespace Pythia8;



int main() {
    // Generator
    Pythia pythia;
    Event& event = pythia.event;
    // Read in pythia commands from file.
    pythia.readFile("kink.cmnd");

    // Variables Initialization.
    int n_gravitinos = 0; // number of gravitino decay particles
    int n_gravitinosInAcc = 0; // number of gravitino decay in LHCb Acceptance
    int n_tauInAcc = 0; // number of taus decay in LHCb Acceptance
    int n_staus = 0; // Total number of staus
    int n_staus_accepted = 0; // Total number of staus in LHCb in LHCb Acceptance
    int n_taus = 0; // Total number of taus
    int n_taus_from_stau = 0; // Total number of taus from stau
    int n_gravitinos_from_stau = 0; // Total number of gravitinos from stau

    // Initialize.
    pythia.init();
    int stau = 1000015;
    int tau = 15;
    int gravitino = 1000039;
    cout << "Lifetime used [mm] =" << scientific << pythia.particleData.tau0(stau) << endl;
    int nEvents = pythia.mode("Main:numberOfEvents");

    // Histograms
    Hist angel("kink angle", 10., -180, 180);
    Hist length("Decay Length", 100., 0, 10000);

    // Begin event loop.
    for (int iEvent = 0; iEvent < nEvents; ++iEvent) {
        if (iEvent % 1000 == 0) std::cout << "Event: " << iEvent << std::endl;
        if (!pythia.next()) continue;

        // Loop over all stau decays in the event.
        for (int i = 0; i < event.size(); ++i) {
            int idAbs = event[i].idAbs(); // call particles by ID
            double eta = event[i].eta(); //  eta (pseudorapidity)

            if (idAbs == tau || idAbs == -tau) { // if the particle is tau or anti tau
                n_taus++;
                if (eta > 1.9 && eta < 5.1) { // if the particle is in the LHCb eta range
                    n_tauInAcc++;
                }
            }

            if (idAbs == gravitino) { // if the particle is gravitino
                n_gravitinos++;
                if (eta > 1.9 && eta < 5.1) { // if the particle is in the LHCb eta range
                    n_gravitinosInAcc++;
                }
            }

            if (idAbs == stau || idAbs == -stau) { // if the particle is stau or anti stau
                n_staus++;
                if (eta > 1.9 && eta < 5.1) {  // if the particle is in the LHCb eta range
                    n_staus_accepted++;
                    // Find the daughters of the stau.
                    int iDau1 = event[i].daughter1();
                    int iDau2 = event[i].daughter2();

                    // Check if the decay is valid (stau decays to tau and gravitino)
                    if (is_valid_decay(event[iDau1].id(), event[iDau2].id())) {
                        double kink_angle_rad = event[i].phi() - event[event[iDau1].idAbs() == 15 ? iDau1 : iDau2].phi();
                        double kink_angle = kink_angle_rad * 180.0 / 3.14159;
                        angel.fill(kink_angle);

                        // Count the gravitino decay products
                        if (event[iDau1].idAbs() == 1000039 || event[iDau2].idAbs() == 1000039) {
                            n_gravitinos_from_stau++;
                        }

                        //count the taus decay products
                        if (event[iDau1].idAbs() == 15 || event[iDau2].idAbs() == 15) {
                            n_taus_from_stau++;
                        }

                        // Calculate the decay length
                        double dist = event[i].vDec().pAbs();
                        length.fill(dist);
                    }
                }
            }
        }
    }
    cout << " Total Number of gravitinos peresent: " << n_gravitinos << endl; // total number of gravitino produced
    cout << " Number of total gravitinos in LHCb Acceptance: " << n_gravitinosInAcc << endl; // total number of gravitino produced
    cout << " Number of total taus  in LHCb Acceptance: " << n_tauInAcc << endl; // total number of taus produced
    cout << "Total number of staus is: " << n_staus << endl;
    cout << "Total number of staus in LHCb Acceptance is: " << n_staus_accepted << endl;
    cout << "Total number of taus is: " << n_taus << endl;
    cout << "Total number of taus from stau is: " << n_taus_from_stau << endl;
    cout << "Total number of gravitinos from stau is: " << n_gravitinos_from_stau << endl;

    HistPlot hpl("DecayAngle");
    hpl.frame( "DecayAnglePlot", "Decay (kink) Angle Distribution", "angle (degrees)","Entries");
    hpl.add(angel, "h,red", "Stau (100 GeV)");
    hpl.plot();
    HistPlot hpl2("DecayLength");
    hpl2.frame( "DecayLengthPlot", "Decay Length Distribution", "Length (mm)","Entries");
    hpl2.add(length, "h,blue", "Stau (100 GeV)");
    hpl2.plot();


    // Write the number of particles to a file
    std::ofstream outfile("particle_counts.txt");
    outfile << "# Total stau: " << n_staus << std::endl;
    outfile << "# Total gravitino: " << n_gravitinos << std::endl;
    outfile << "# Total tau: " << n_taus << std::endl;
    outfile << "# Stau in LHCb Acc: " << n_staus_accepted << std::endl;
    outfile << "# Gravitino in LHCb Acc: " << n_gravitinosInAcc << std::endl;
    outfile << "# Taus in LHCb Acc: " << n_tauInAcc << std::endl;
    outfile << "# Taus from stau: " << n_taus_from_stau << std::endl;
    outfile << "# Gravitino from stau: " << n_gravitinos_from_stau << std::endl;

    outfile.close();

    // Done.
    pythia.stat();
    return 0;
}
