#include "Pythia8/Pythia.h"
#include <iostream>
#include <vector>
#include <iostream>
#include <cmath>
#include <array>

using namespace Pythia8;


std::array<double, 3> spherical_to_cartesian(double r, double theta, double phi) {
    return {r * sin(theta) * cos(phi), r * sin(theta) * sin(phi), r * cos(theta)};
}

double dot_product(const std::array<double, 3>& a, const std::array<double, 3>& b) {
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
}

std::array<double, 3> cross_product(const std::array<double, 3>& a, const std::array<double, 3>& b) {
    return {a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]};
}

double kink_angle(double theta_stau, double theta_tau, double phi_stau, double phi_tau) {
    // Convert spherical coordinates to cartesian coordinates
    std::array<double, 3> stau_cartesian = spherical_to_cartesian(1, theta_stau, phi_stau);
    std::array<double, 3> tau_cartesian = spherical_to_cartesian(1, theta_tau, phi_tau);

    // Calculate the dot product and the magnitudes of the two vectors
    double dot = dot_product(stau_cartesian, tau_cartesian);
    double stau_magnitude = std::sqrt(dot_product(stau_cartesian, stau_cartesian));
    double tau_magnitude = std::sqrt(dot_product(tau_cartesian, tau_cartesian));

    // Calculate the cosine of the angle between the vectors
    double cos_angle = dot / (stau_magnitude * tau_magnitude);

    // Calculate the cross product and the magnitude of the cross product
    std::array<double, 3> cross = cross_product(stau_cartesian, tau_cartesian);
    double cross_magnitude = std::sqrt(dot_product(cross, cross));

    // Calculate the sine of the angle between the vectors
    double sin_angle = cross_magnitude / (stau_magnitude * tau_magnitude);

    // Calculate the signed angle
    double signed_angle = std::atan2(sin_angle, cos_angle);

    // Convert the signed angle to degrees
    signed_angle = signed_angle * 180 / M_PI;
    return signed_angle;
}

int main() {
    // Generator
    Pythia pythia;
    Event& event = pythia.event;
    // Read in pythia commands from file.
    pythia.readFile("kink.cmnd");

    // Variables Initialization.
    int neta_accepted = 0 ;
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

    // Begin event loop.
    for (int iEvent = 0; iEvent < nEvents; ++iEvent) {
        if (iEvent%1000 == 0) std::cout << "Event: " << iEvent << std::endl;
        if (!pythia.next()) continue;

        // Loop over all stau decays in the event.
        for (int i = 0; i < event.size(); ++i) {
            int idAbs = event[i].idAbs(); // call particles by ID
            double eta = event[i].eta(); //  eta (pseudorapidity)
            
            if (idAbs == stau || idAbs == -stau) { // if the particle is stau or anti stau
                if (eta > 1.9 && eta < 5.1) {  // if the particle is in the LHCb eta range
                   neta_accepted++;
                // Find the daughters of the stau.
                   int iDau1 = event[i].daughter1();
                   int iDau2 = event[i].daughter2();
                // print which particle is the daughter
                // Todo: understand why daughter1 and daughter2 might be staus themselves
                   //cout << "Daughter 1: " << event[iDau1].id() << endl;
                   //cout << "Daughter 2: " << event[iDau2].id() << endl;

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
                        double calculated_kink_angle = kink_angle(event[i].theta(), event[iDau1].theta(), event[i].phi(), event[iDau1].phi());
                        //cout << "Kink angle: " << calculated_kink_angle << endl;
                        ndecay_s_accepted++;
                        angel.fill(calculated_kink_angle);
                    }
            // calculate the kink angle if the second daughter is a tau
                   if (event[iDau2].idAbs() == 15 && event[iDau1].idAbs() != 15) {
                        double calculated_kink_angle_2 = kink_angle(event[i].theta(), event[iDau2].theta(), event[i].phi(), event[iDau2].phi());
                       //cout << "Kink angle: " << calculated_kink_angle_2<< endl;
                       ndecay_s_accepted++;
                       angel.fill(calculated_kink_angle_2);
                   }
                   // if either daughter is a gravitino, count them as a decay product
                   if (event[iDau1].idAbs() == 1000039 || event[iDau2].idAbs() == 1000039) {
                          ndecay_g_accepted++;
                   } 


                }

}
        }
    }
    // Statistics.
    pythia.stat();
    cout << " Number of gravitinos daughters accepted: " << ndecay_g_accepted << endl; // total number of gravitino produced
    cout << " Number of taus daughters accepted: " << ndecay_s_accepted << endl; // total number of taus produced
    cout << endl << nEvents << " events generated. " << neta_accepted << " events passed eta cut." << endl;

    HistPlot hpl("DecayAngle");
    hpl.frame( "DecayAnglePlot", "Decay (kink) Angle Distribution", "angle (degrees)","Entries");
    hpl.add(angel, "h,red", "Stau (100 GeV)");
    hpl.plot();

    // Done.
    return 0;

}