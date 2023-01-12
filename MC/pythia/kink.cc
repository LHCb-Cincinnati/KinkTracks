#include "Pythia8/Pythia.h"
#include <iostream>
#include <vector>
#include <iostream>
#include <cmath>

using namespace Pythia8;

int main() {
    // Generator
    Pythia pythia;
    Event& event = pythia.event;
    // Read in pythia commands from file.
    pythia.readFile("kink.cmnd");

    // Variables Initialization.
    int neta_accepted = 0 ;
    int ndecay1_accepted = 0 ;
    int ndecay2_accepted = 0 ;
    int ndecay3_accepted = 0 ;
    int ndecay4_accepted = 0 ;
    int ndecay_g_accepted = 0 ; // number of gravitino decay accepted
    int ndecay_s_accepted = 0 ; // number of taus decay accepted


    // Initialize.
    pythia.init();
    int stau = 1000015;
    cout << "Lifetime used [mm] =" << scientific << pythia.particleData.tau0(stau) << endl;
    int nEvents = pythia.mode("Main:numberOfEvents");
    //int nAbort = pythia.mode("Main:timesAllowErrors");
    // Histograms
    Hist angel("kink angle", 10.,-180,180);
    Hist length("Decay Length", 100.,0,10000);

    // Begin event loop.
    for (int iEvent = 0; iEvent < nEvents; ++iEvent) {
        if (iEvent%1000 == 0) std::cout << "Event: " << iEvent << std::endl;
        if (!pythia.next()) continue;

        // Loop over all stau decays in the event.
        for (int i = 0; i < event.size(); ++i) {
            int idAbs = event[i].idAbs(); // call particles by ID
            double eta = event[i].eta(); //  eta (pseudorapidity)
            
            if (idAbs == stau || idAbs == -stau) { // if the particle is stau or anti stau
                if (eta > 2 && eta < 5) {  // if the particle is in the LHCb eta range
                   neta_accepted++;
                // Find the daughters of the stau.
                   int iDau1 = event[i].daughter1();
                   int iDau2 = event[i].daughter2();
                // print which particle is the daughter
                // Todo: understand why daughter1 and daughter2 might be staus themselves
                   cout << "Daughter 1: " << event[iDau1].id() << endl;
                   cout << "Daughter 2: " << event[iDau2].id() << endl;

                // if event[iDau1].idAbs() == 15 and not event[iDau2].idAbs() == 1000015 or -1000015
                // then iDau1 is the tau and iDau2 is the gravitino
                // if event[iDau2].idAbs() == 15 and not event[iDau1].idAbs() == 1000015 or -1000015
                // then iDau2 is the tau and iDau1 is the gravitino
                // if event[iDau1].idAbs() == 15 and event[iDau2].idAbs() == 15
                // then both daughters are taus (which we want to write that this is invalid)
                if (event[iDau1].idAbs() == 15 && event[iDau2].idAbs() == 15) {
                    cout << "Both daughters are taus. This is invalid." << endl;
                }



            //cout << "First daughter: " << iDau1 << " Second daughter: " << iDau2 << endl;
            // calcaulte the kink angle if the first daughter is a tau
                   // if the first daughter is 15 and the second daughter is not 15
                    if (event[iDau1].idAbs() == 15 && event[iDau2].idAbs() != 15) {
                        double kink_angle_rad = event[i].phi() - event[iDau1].phi();
                        double kink_angle = kink_angle_rad * 180.0 / 3.14159;
                        cout << "Kink angle: " << kink_angle << endl;
                        ndecay_s_accepted++;
                        angel.fill(kink_angle);
                    }
            // calculate the kink angle if the second daughter is a tau
                   if (event[iDau2].idAbs() == 15 && event[iDau1].idAbs() != 15) {
                       double kink_angle_rad_2 = event[i].phi() - event[iDau2].phi();
                       double kink_angle_2 = kink_angle_rad_2 * 180.0 / 3.14159;
                       cout << "Kink angle: " << kink_angle_2<< endl;
                       ndecay_s_accepted++;
                       angel.fill(kink_angle_2);
                   }
                   // if either daughter is a gravitino, count them as a decay product
                   if (event[iDau1].idAbs() == 1000039 || event[iDau2].idAbs() == 1000039) {
                          ndecay_g_accepted++;
                   } 
            // calculate the decay length inside LHCb.
            //double dist = event[i].vDec().pAbs();
                   double dist = sqrt(pow(event[i].xDec(),2) + pow(event[i].yDec(),2) + pow(event[i].zDec(),2));
                   length.fill(dist);
                   cout << "Decay length: " << dist << endl;

                // determine if stau decays between 1000 mm and 2000 mm.
                   if (dist > 13000 && dist < 15300) {
                      ndecay1_accepted++;
                    }
                    if (dist > 15000 && dist < 18700) {
                      ndecay2_accepted++;
                    }
                    if (dist > 16300 && dist < 18700) {
                        ndecay3_accepted++;
                    }
                    if (dist > 7800 && dist < 9500) {
                        ndecay4_accepted++;
                    }

                }

}
        }
    }
    // Statistics.
    pythia.stat();
    cout << " Number of gravitinos daughters accepted: " << ndecay_g_accepted << endl; // total number of gravitino produced
    cout << " Number of taus daughters accepted: " << ndecay_s_accepted << endl; // total number of taus produced
    cout << endl << nEvents << " events generated. " << neta_accepted
    << " events passed eta cut." << endl;
    cout << endl << nEvents << " events generated. " << ndecay1_accepted
    << " events passed between M1-M2 + eta ." << endl;
    cout << endl << nEvents << " events generated. " << ndecay2_accepted
    << " events passed between M2-M5 + eta ." << endl;
    cout << endl << nEvents << " events generated. " << ndecay3_accepted
    << " events passed between M3-M5 + eta ." << endl;
    cout << endl << nEvents << " events generated. " << ndecay4_accepted
    << " events passed between T1-T3 + eta ." << endl;

    HistPlot hpl("DecayAngle");
    hpl.frame( "DecayAnglePlot", "Decay (kink) Angle Distribution", "angle (degrees)","Entries");
    hpl.add(angel, "h,red", "Stau (100 GeV)");
    hpl.plot();
    HistPlot hpl2("DecayLength");
    hpl2.frame( "DecayLengthPlot", "Decay Length Distribution", "Length (mm)","Entries");
    hpl2.add(length, "h,blue", "Stau (100 GeV)");
    hpl2.plot();

    // Done.
    return 0;

}
