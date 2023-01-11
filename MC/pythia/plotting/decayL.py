from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
from scipy.optimize import curve_fit

# Exponential function for fitting
def exponential_func(x, a, b):
    return a * np.exp(-b * x)

pp = PdfPages('DecayLength.pdf')
tmp1 = plt.figure(1)
tmp1.set_size_inches(8.00, 6.00)
plot = open('DecayLengthPlot-0.dat')
plot = [line.split() for line in plot]
valx = np.array([float(x[0]) for x in plot])  # Convert valx to a numpy array
valy = np.array([float(x[1]) for x in plot])  # Convert valy to a numpy array
#valy = [float(x[1]) for x in plot]
vale = [float(x[2]) for x in plot]

# Fit the data to an exponential function
params, params_covariance = curve_fit(exponential_func, valx, valy)
errors = np.sqrt(np.diag(params_covariance))

# Plot the data and the fit
plt.hist(valx, vale, weights=valy, histtype='step', color='blue', label=r'DecayLength')
plt.plot(valx, exponential_func(valx, params[0], params[1]), 'r', label='fit')
plt.xlim(0.000e+00, 1.000e+04)
plt.ylim(0.000e+00, 1.040e+02)
plt.ticklabel_format(axis='y', style='sci', scilimits=(-2, 3))
plt.legend(frameon=False, loc='best')
plt.title(r'Stau>tau (100 GeV)')
plt.xlabel(r'Length (mm)')
plt.ylabel(r'Entries')
pp.savefig(tmp1, bbox_inches='tight')
plt.clf()
pp.close()
