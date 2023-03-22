## This file is used to calculate the lifetime needed for specific c*tau value


# Tell the use if you want to calculate tau or ctau
print("Do you want to calculate tau or ctau?")
choice = input("Enter 'tau' or 'ctau': ")

if choice == "ctau":
    tau = float(input("Enter the value of tau in s: "))
    ctau = tau * 299792458
    print("The value of ctau is: ", ctau, "m")
elif choice == "tau":
    ctau = float(input("Enter the value of c*tau in m: "))
    tau = ctau / 299792458
    print("The value of tau is: ", tau, "s")
else:
    print("You have entered a wrong choice")
