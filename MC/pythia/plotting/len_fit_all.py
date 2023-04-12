## Author: Mohamed Elashri
## Description: A script to fit all the different combinations of parameters for decay length distribution
## Date: 04/11/2023
## Email: mail@elashri.com

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from scipy.optimize import curve_fit

ln_values = [10, 100, 1000, 10000]
ms_values = [100, 150, 200, 250, 300]
def exp_func(x, a, b, c):
    return a * np.exp(-b * x) + c

for ln in ln_values:
    for ms in ms_values:
        pp = PdfPages(f'DecayLength_{ms}GeV_{ln}mm_fit.pdf')
        tmp1 = plt.figure(1)
        tmp1.set_size_inches(8.00, 6.00)
        plot = open(f'data/decay_length_data/DecayLength_{ms}GeV_{ln}mm-0.dat')
        plot = [line.split() for line in plot]
        valx = [float(x[0]) for x in plot]
        valy = [float(x[1]) for x in plot]
        vale = [float(x[2]) for x in plot]
        plt.hist(valx, vale, weights=valy, histtype='step', color='red', label=fr'Stau ({ms} GeV), ctau = {ln} mm')

        # Fit the data
        popt, pcov = curve_fit(exp_func, valx, valy, p0=[1, 1e-4, 1], maxfev=10000)
        fit_y = exp_func(np.array(valx), *popt)
        plt.plot(valx, fit_y, label=f'Fit: a={popt[0]:.2e}, b={popt[1]:.2e}, c={popt[2]:.2e}')
        
        # Calculate and display lifetime
        lifetime = 1 / popt[1]
        # convert lifetime from mm to m
        lifetime = lifetime / 1000.0
        plt.text(0.55, 0.85, f'Lifetime: {lifetime:.2e}' ' m',
                 transform=plt.gca().transAxes,
                 fontsize=10,
                 verticalalignment='top',
                 bbox=dict(facecolor='white', alpha=0.8),
                 fontweight='bold')


        plt.xlim(0.000e+00, 1.000e+04)
        plt.ticklabel_format(axis='y', style='sci', scilimits=(-2, 3))
        plt.legend(frameon=False, loc='best')
        plt.title(r'Decay Length Distribution')
        plt.xlabel(r'Length (mm)')
        plt.ylabel(r'Entries')
        pp.savefig(tmp1, bbox_inches='tight')
        plt.clf()
        pp.close()
