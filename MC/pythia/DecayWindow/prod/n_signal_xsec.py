
# This script is plotting number of Events Produced that pass cuts vs Mass
import matplotlib.pyplot as plt
import numpy as np

## for 100 cm 
x = [100, 150, 200, 250, 300]
y1 = [4752,3091,3187,2475,1883]
y1 = [element / 10000 for element in y1]
xsec_prod = [7.063e-11,4.433e-11,8.102e-12,5.292e-12,3.627e-12]
xsec_prod = [element * 1e-3 for element in xsec_prod]

 # https://lhcb.web.cern.ch/speakersbureau/html/PerformanceNumbers.html
L = 5.7e15 # LHCb run 2 integrated lumniosity
N1 = L * np.multiply(y1,xsec_prod) 
plt.plot(x, N1,marker='x', linestyle='dashdot', color='r', label='100 cm')


## for 1000 cm 
y2 = [4752,3091,3187,2475,1883]
y2 = [element / 10000 for element in y2]
N2 = L * np.multiply(y2,xsec_prod) 
plt.plot(x, N2,marker='x', linestyle='dashdot', color='b', label='1000 cm')

## for 10000 cm 
y3 = [4752,3091,3187,2475,1883]
y3 = [element / 10000 for element in y3]

N3 = L * np.multiply(y3,xsec_prod) 
plt.plot(x, N3,marker='x', linestyle='dashdot', color='g', label='10000 cm')



plt.yscale('log')
plt.title('Number of Events Produced that pass LHCb eta vs Mass')
plt.xlabel('Mass (GeV)')
plt.ylabel('Number of Events')
plt.legend()
plt.savefig('nEvent_LHCb.pdf')  
plt.show()
