#include "Pythia8/Pythia.h"
#include <iostream>
#include "TVirtualPad.h"
#include "TApplication.h"
#include "TH1.h"         
#include <TH1F.h>   
#include "TFile.h"
#include <TCanvas.h>
#include <TF1Convolution.h>
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

    // Begin event loop.
    for (int iEvent = 0; iEvent < nEvents; ++iEvent) {
        if (iEvent%1000 == 0) std::cout << "Event: " << iEvent << std::endl;
        if (!pythia.next()) continue;

        // Loop over all stau decays in the event.
        for (int i = 0; i < event.size(); ++i) {
            int idAbs = event[i].idAbs(); // call particles by ID
            double eta = event[i].eta(); //  eta (pseudorapidity)
            if (event[i].id() == 1000015) { // if the particle is a stau
                if (event[i].eta() > 2 && event[i].eta() < 5) {  // if the particle is in the LHCb eta range
                neta_accepted++;
                // Find the first daughter of the stau.
                int iDau1 = event[i].daughter1();
                int iDau2 = event[i].daughter2();
            cout << "First daughter: " << iDau1 << " Second daughter: " << iDau2 << endl;
            // calcalate the kink angle.
            double kink_angle = atan((event[iDau2].y() - event[iDau1].y()) / (event[iDau2].x() - event[iDau1].x()));
            cout << "Kink angle: " << kink_angle << endl;
            // calculate the kink length.
            double kink_length = sqrt(pow(event[iDau2].x() - event[iDau1].x(), 2) + pow(event[iDau2].y() - event[iDau1].y(), 2));
            cout << "Kink length: " << kink_length << endl;
            // calculate the decay length inside LHCb.
            double dist = event[i].vDec().pAbs();  

            










                }

}
        }
    }
    // Statistics.
    pythia.stat();

    // Done.
    return 0;

}