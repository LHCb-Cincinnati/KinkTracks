import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import os


ln = '10000'

# Read data from the files
def read_data(filename):
    with open(filename) as f:
        data = [line.split() for line in f]
    valx = [float(x[0]) for x in data]
    valy = [float(x[1]) for x in data]
    vale = [float(x[2]) for x in data]
    return valx, valy, vale

valx_100, valy_100, vale_100 = read_data('../DecayLength_100GeV_'+ln+'mm-0.dat')
valx_150, valy_150, vale_150 = read_data('../DecayLength_150GeV_'+ln+'mm-0.dat')
valx_200, valy_200, vale_200 = read_data('../DecayLength_200GeV_'+ln+'mm-0.dat')
valx_250, valy_250, vale_250 = read_data('../DecayLength_250GeV_'+ln+'mm-0.dat')
valx_300, valy_300, vale_300 = read_data('../DecayLength_300GeV_'+ln+'mm-0.dat')

# Create the plot
pp = PdfPages('DecayLength_combined_' + ln + 'mm.pdf')
tmp1 = plt.figure(1)
tmp1.set_size_inches(25.00, 15.00)

plt.hist(valx_100, vale_100, weights=valy_100, histtype='step', color='red', label=r'Stau (100 GeV), ctau =' + ln + ' mm')
plt.hist(valx_150, vale_150, weights=valy_150, histtype='step', color='blue', label=r'Stau (150 GeV), ctau =' + ln + ' mm')
plt.hist(valx_200, vale_200, weights=valy_200, histtype='step', color='green', label=r'Stau (200 GeV), ctau =' + ln + ' mm')
plt.hist(valx_250, vale_250, weights=valy_250, histtype='step', color='orange', label=r'Stau (250 GeV), ctau =' + ln + ' mm')
plt.hist(valx_300, vale_300, weights=valy_300, histtype='step', color='purple', label=r'Stau (300 GeV), ctau =' + ln + ' mm')


plt.xlim(0.000e+00, 1.000e+04)
plt.ylim(0.000e+00, max(max(valy_100), max(valy_300)) * 1.1)  

plt.ticklabel_format(axis='y', style='sci', scilimits=(-2, 3))
plt.legend(frameon=False, loc='best')
plt.title(r'Decay Length Distribution')
plt.xlabel(r'Length (mm)')
plt.ylabel(r'Entries')

pp.savefig(tmp1, bbox_inches='tight')
plt.clf()
pp.close()
