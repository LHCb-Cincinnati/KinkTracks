
# This script is plotting number of Events Produced that pass cuts vs Mass 
import matplotlib.pyplot as plt
import numpy as np


## for 100 cm 
x = [100, 150, 200, 250, 300]
y1 = [181,83,73,61,16]
y1 = [element / 10000 for element in y1]
plt.plot(x, y1,marker='.', linestyle='solid', color='r', label='100  cm')


## for 1000 cm 
y2 = [163,123,116,90,86]
y2 = [element / 10000 for element in y2]
plt.plot(x, y2,marker='.', linestyle='solid', color='g', label='1000 cm')

## for 10000 cm 
y3 = [16,25,16,15,11]
y3 = [element / 10000 for element in y3]
plt.plot(x, y3,marker='.', linestyle='solid', color='m', label='10000 cm')



plt.yscale('log')
plt.title('LHCb Acceptance (M1-M2) vs Mass')
plt.xlabel('Mass (GeV)')
plt.ylabel('Acceptance')
plt.legend()
plt.savefig('acc_LHCb.pdf')  
plt.show()
