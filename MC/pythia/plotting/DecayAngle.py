from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
pp   = PdfPages('plots/DecayAnglePlot.pdf')
tmp1 = plt.figure(1)
tmp1.set_size_inches(8.00,6.00)
plot = open('data/DecayAnglePlot-0.dat')
plot = [line.split() for line in plot]
valx = [float(x[0]) for x in plot]
valy = [float(x[1]) for x in plot]
vale = [float(x[2]) for x in plot]
plt.hist(valx, vale, weights=valy, histtype='bar', color='red', label=r'Stau (100 GeV), ctau = 100 cm')
plt.xlim(-1.800e+02, 1.800e+02)
#plt.ylim(0.000e+00, 7.569e+04)
plt.ticklabel_format(axis='y', style='sci', scilimits=(-2, 3))
plt.legend(frameon=False, loc='best')
plt.title(r'Decay (kink) Angle Distribution')
plt.xlabel(r'angle (degrees)', ha='right', x=1)
plt.ylabel(r'Entries', ha='right', y=1)

ax = plt.gca()
ax.text(0.03, 0.97, 'LHCb Simulation', transform=ax.transAxes, size=18, fontweight='bold', verticalalignment='top', horizontalalignment='left')

plt.tight_layout()
pp.savefig(tmp1)
plt.clf()
pp.close()
