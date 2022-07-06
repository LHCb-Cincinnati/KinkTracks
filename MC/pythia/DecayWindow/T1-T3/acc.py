
# This script is plotting number of Events Produced that pass cuts vs Mass 
import matplotlib.pyplot as plt
import numpy as np


## for 100 cm 
x = [100,150,200,250,300]
y1 = [255,176,164,112,81]
y1 = [element / 10000 for element in y1]
plt.plot(x, y1,marker='.', linestyle='solid', color='r', label='100  cm')


## for 1000 cm 
y2 = [112,87,91,95,105]
y2 = [element / 10000 for element in y2]
plt.plot(x, y2,marker='.', linestyle='solid', color='g', label='1000 cm')

## for 10000 cm 
y3 = [15,18,10,8,7]
y3 = [element / 10000 for element in y3]
plt.plot(x, y3,marker='.', linestyle='solid', color='m', label='10000 cm')




plt.yscale('log')
plt.title('LHCb Acceptance (T1-T3) vs Mass')
plt.xlabel('Mass (GeV)')
plt.ylabel('Acceptance')
plt.legend()
plt.savefig('acc_LHCb.pdf')  
plt.show()
