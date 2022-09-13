'''
 A script to scan SLHA file and determine which particle is the NLSP for GMSB SUSY models
 Created: Mohamed Elashri, 23th Sep 2022
'''

# ask for input file
input_file = input("Enter input file name/path: ")

lines = []
with open (input_file, 'r') as file:
    for line in file:
        lines.append(line)
print("The stau mass is",lines[47].split()[1],"GeV") # print the stau mass   


# loop over lines 38 to 56 and print the mass of the NLSP (the smallest mass) 
masses = []
pdgs = []
for i in range(38,53):
    masses.append(lines[i].split()[1])
    pdgs.append(lines[i].split()[0])
print("The NLSP mass is",min(masses),"GeV")
print("The NLSP pdg is",pdgs[masses.index(min(masses))])

# if the NLSP is 1000022, print that it is Neutralino
if pdgs[masses.index(min(masses))] == "1000022":
    print("The NLSP is Neutralino")
if pdgs[masses.index(min(masses))] == "1000015":
    print("The NLSP is Stau")
if pdgs[masses.index(min(masses))] != "1000015" and pdgs[masses.index(min(masses))] != "1000022":    
    print("The NLSP is not Neutralino or Stau")        