#include "Pythia8/Pythia.h"
#include <vector>
#include <iostream>

using namespace Pythia8;

int main() {
    // Generator 
    Pythia pythia;
    Event& event = pythia.event;
    // Read in pythia commands from file.
    pythia.readFile("kink.cmnd");

    // Variables Initialization.
    int neta_accepted = 0 ;

    // Initialize.
    pythia.init();

    int nEvents = pythia.mode("Main:numberOfEvents");
    int nAbort = pythia.mode("Main:timesAllowErrors");
    // Histograms
    Hist angel("kink angle", 10.,-180,180);
    Hist length("kink angle", 10.,0,100);

    // Begin event loop.
    for (int iEvent = 0; iEvent < nEvents; ++iEvent) {
        if (iEvent%1000 == 0) std::cout << "Event: " << iEvent << std::endl;
        if (!pythia.next()) continue;

        // Loop over all stau decays in the event.
        for (int i = 0; i < event.size(); ++i) {
            int idAbs = event[i].idAbs(); // call particles by ID
            double eta = event[i].eta(); //  eta (pseudorapidity)
            if (idAbs == 1000015) { // if the particle is a stau
                if (eta > 2 && eta < 5) {  // if the particle is in the LHCb eta range
                neta_accepted++;
                // Find the first daughter of the stau.
                int iDau1 = event[i].daughter1();
                int iDau2 = event[i].daughter2();
            //cout << "First daughter: " << iDau1 << " Second daughter: " << iDau2 << endl;
            // calcalate the kink angle in degrees.
            double kink_angle_rad = event[iDau1].phi() - event[iDau2].phi();
            double kink_angle = kink_angle_rad * 180.0 / 3.14159;
            angel.fill(kink_angle);
            cout << "Kink angle: " << kink_angle << endl;
            // calculate the kink length.
            // calculate the decay length inside LHCb.
            double dist = event[i].vDec().pAbs();
            length.fill(dist);  
            cout << "Decay length: " << dist << endl;



                }

}
        }
    }
    // Statistics.
    pythia.stat();
    HistPlot hpl("DecayAngle");
    hpl.frame( "DecayAnglePlot", "Stau>tau (100 GeV)", "angle (degrees)","Entries");
    hpl.add(angel, "h,red", "KinkAngle");
    hpl.plot();
    HistPlot hpl2("DecayLength");
    hpl2.frame( "DecayLengthPlot", "Stau>tau (100 GeV)", "Length (MM)","Entries");
    hpl2.add(length, "h,red", "DecayLength");
    hpl2.plot();

    // Done.
    return 0;

}
