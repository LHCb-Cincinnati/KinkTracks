## This file is used to calculate the lifetime needed for specific c*tau value

## let the user input the value of c*tau
ctau = float(input("Enter the value of c*tau in m: "))
## Now calculate the tau using speed of light in m/s
tau = ctau / 299792458
## now print the value of tau
print("The value of tau is: ", tau, "s")
## convert the value of tau to scintific notation
print("The value of tau in scintific notation is: ", "{:.2e}".format(tau), "s")