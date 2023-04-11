import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from scipy.optimize import curve_fit


'''
In the exponential decay function provided:

y = a * np.exp(-b * x) + c

x represents the decay length, and
y represents the probability density (or number of entries, in your histogram) at a given length x. 

The parameters a, b, and c have the following meanings:

<a>: This parameter represents the amplitude or the scaling factor of the exponential decay.
It determines the initial value of the probability density (or the number of entries) when x = 0.
A higher value of a indicates that there are more particles with shorter decay lengths.

<b>: This parameter represents the decay constant or rate of decay. 
It determines how quickly the probability density (or the number of entries) decreases as the decay length increases.
A higher value of b means that the particle's decay length distribution decreases more rapidly, and the particle is more likely to decay closer to the origin.
A smaller value of b indicates a slower decay, and the particle is more likely to travel longer distances before decaying.

<c>: This parameter represents the offset or background level of the exponential decay. It shifts the entire distribution up or down along the y-axis. 
In the context of particle decay length, c can represent the constant background noise or unrelated events that are always present 
in the data, regardless of the decay length x.

'''


ln = '10'
ms = '100' 
def exp_func(x, a, b, c):
    return a * np.exp(-b * x) + c


pp = PdfPages('DecayLength_'+ ms + 'GeV_'+ ln+ 'mm_fit.pdf')
tmp1 = plt.figure(1)
tmp1.set_size_inches(8.00, 6.00)
plot = open('../DecayLength_'+ ms + 'GeV_' + ln+ 'mm-0.dat')
plot = [line.split() for line in plot]
valx = [float(x[0]) for x in plot]
valy = [float(x[1]) for x in plot]
vale = [float(x[2]) for x in plot]
plt.hist(valx, vale, weights=valy, histtype='step', color='red', label=r'Stau (' + ms + 'GeV), ctau = ' + ln + ' mm')

# Fit the data
popt, pcov = curve_fit(exp_func, valx, valy, p0=[1, 1e-4, 1], maxfev=10000)
fit_y = exp_func(np.array(valx), *popt)
plt.plot(valx, fit_y, label=f'Fit: a={popt[0]:.2e}, b={popt[1]:.2e}, c={popt[2]:.2e}')


plt.xlim(0.000e+00, 1.000e+04)
#plt.ylim(0.000e+00, max(valy))
plt.ticklabel_format(axis='y', style='sci', scilimits=(-2, 3))
plt.legend(frameon=False, loc='best')
plt.title(r'Decay Length Distribution')
plt.xlabel(r'Length (mm)')
plt.ylabel(r'Entries')
pp.savefig(tmp1, bbox_inches='tight')
plt.clf()
pp.close()
