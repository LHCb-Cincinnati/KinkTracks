from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
pp   = PdfPages('plots/DecayLengthPlot.pdf')
tmp1 = plt.figure(1)
tmp1.set_size_inches(8.00,6.00)
plot = open('data/DecayLengthPlot-0.dat')
plot = [line.split() for line in plot]
valx = [float(x[0]) for x in plot]
# convert mm to cm
valx = [x/10. for x in valx]
valy = [float(x[1]) for x in plot]
valy = [x/10. for x in valy]
vale = [float(x[2]) for x in plot]
vale = [x/10. for x in vale]
plt.hist( valx, vale, weights = valy, histtype='bar', color='blue', label=r'Stau (100 GeV) , ctau = 100 cm')
plt.ticklabel_format(axis='y', style='sci', scilimits=(-2,3))
plt.legend(frameon=False,loc='best')
plt.title(r'Decay Length Distribution')
plt.xlabel(r'Length (cm)', ha='right', x=1)
plt.ylabel(r'Entries', ha='right', y=1)
plt.text(100,850, 'LHCb Simulation', {'size': 18, 'fontweight' :'bold'})
plt.xlim(0, 1000)
plt.ylim(0, 1000)
pp.savefig(tmp1,bbox_inches='tight')
plt.clf()
pp.close()


