# A program to scan range of values for some parameter of a SUSY model
# Model and parameter and value range to scan needs to be set by hand
# Created: Conor Henderson, 16th June 2022
# Last modified: Mohamed Elashri, 17th June 2022
#------------------------------------------------------------------------------
## Changlog:

# 16th June: Added the main script to scan the parameter space of the model
# 17th June: Added the support to create SLHA files as an output
#            Added code to delete existing SLHA/isa files before creating new ones
#------------------------------------------------------------------------------



# import packages
import glob
import os



# Get list for all isa/slha files already in directory
# isajet will through an error if the isa/slha filenames chosen exists, so we need to delete it
# before running the scan. 
# PS. This will delete all slha/isa files in the directory so take bakeup before running that
for file in os.listdir():
    if file.endswith(".isa") or file.endswith(".slha"):
        os.remove(file)

#when m_top is needed, use PDG value
m_top = 172.69

# Construction of command based on following interactive input of isasugra.x

# ENTER output filename in single quotes:
# test1.slha
#  ENTER SUSY Les Houches Accord filename [/ for none]:
# /
#  ENTER Isawig (Herwig interface) filename [/ for none]:
# /
#  ENTER 1 for mSUGRA:
#  ENTER 2 for mGMSB:
#  ENTER 3 for non-universal SUGRA:
#  ENTER 4 for SUGRA with truly unified gauge couplings:
#  ENTER 5 for non-minimal GMSB:
#  ENTER 6 for SUGRA+right-handed neutrino:
#  ENTER 7 for minimal anomaly-mediated SUSY breaking:
#  ENTER 8 for non-minimal AMSB:
#  ENTER 9 for mixed moduli-AMSB:
#  ENTER 10 for Hypercharged-AMSB:
#  ENTER 11 for NUHM from D-term:
#  ENTER 12 for general mirage mediation (GMM):
#  ENTER 13 for natural AMSB (nAMSB):
# 2
#  ENTER Lambda, M_mes, N_5, tan(beta), sgn(mu), M_t, C_gv:
# 100000,500000,3,10,+1,172.69,1
#  Run Isatools? Choose 2=all, 1=some, 0=none:
 # 0
#  To run RGEFLAV, enter filename Prefix [/ for none]:
#  RGEFLAV will open file Prefix.rgein, and print to files
#  Prefix.weakout, Prefix.gutout, Prefix.sqm2u, Prefix.sqm2d
# /



'''
Lambda:  The sccale of the SUSY breaking (10000-100000 GeV / typically 10–100 TeV)
M_mes:   Messenger mass scale > Lambda
N_5:      The equivalent number of 5+5bar messenger fields
tan_b:    tan(beta) he ratio (0-10)
sgn(mu):   +/-1,  sign of Higgsino mass term (default 1)
C_gv   >=1, The ratio of the gravitino mass to its value for a breaking scale of F_m
M_t     Top quark pole mass
'''




# now set up to scan range of values for some parameter

gmsb_lambda_scan_set = [0.1e5,0.5e5,1.0e5,1.5e5,2e5,3e5]
gmsb_lambda_scan_type = "L"

gmsb_M_mess_scan_set = [1e5,2e5,3e5,4e5,5e5,6e6,10e6]
gmsb_M_mess_scan_type = "M"

gmsb_tanBeta_scan_set = [10,20,30,40,50]
gmsb_tanBeta_scan_type = "tanB"


#***************
# helpful to use a generic scan set, just assign it to the desired one
#scan_set = gmsb_lambda_scan_set
#scan_type = gmsb_lambda_scan_type

scan_set = gmsb_M_mess_scan_set
scan_type = gmsb_M_mess_scan_type

#scan_set = gmsb_tanBeta_scan_set
#scan_type = gmsb_tanBeta_scan_type


# *****************
# also must assign the scan_variable to the right param inside the later scan loop!
# *****************


# for all others, we can just keep them fixed for this scan

# SUSY model - 2 is GMSB
susy_model_num=2
# if the SUSy model is different, the input params will be different
# and one will need to write a new arg set ...
# the following are specific for GMSB:
gmsb_Lambda = 3.0e5  
gmsb_M_mess = 6e5
gmsb_N_fields = 3
gmsb_tan_beta = 40
gmsb_sign_mu = +1 # or -1
gmsb_m_top = m_top
gmsb_cgv = 1

# if scanning, the param value above will be overwritten later


itrial = 0
for scan_val in scan_set:
    itrial+=1
 

    # *****************
    # also must assign the scan_variable to the right param inside the later scan loop!
    # *****************

    #gmsb_Lambda = scan_val
    gmsb_M_mess = scan_val
    #gmsb_tan_beta = scan_val
    
    #    print(itrial,": Lambda = ",gmsb_Lambda)

    filename = 'gmsb_scan_{0}_{1}.isa'.format(scan_type,itrial)
    slhafile = 'gmsb_scan_{0}_{1}.slha'.format(scan_type,itrial)

    gmsb_model_args = '{0},{1},{2},{3},{4},{5},{6}'.format(gmsb_Lambda,gmsb_M_mess,gmsb_N_fields,gmsb_tan_beta,gmsb_sign_mu,gmsb_m_top,gmsb_cgv)

    # a way to maybe switch more easily between differnt model arg sets
    susy_model_args = gmsb_model_args

    #arg_string = 'echo "{0}\n /\n /\n /\n {1}\n {2}\n 0\n /\n" | ./isasugra.x'.format(filename,susy_model_num,susy_model_args)
    arg_string = 'echo "{0}\n {1}\n /\n {2}\n {3}\n 0\n /\n" | ./isasugra.x'.format(filename,slhafile,susy_model_num,susy_model_args)
    #os.system('echo "test_auto2.isa\n /\n /\n 2\n 1e5,2e5,3,40,+1,172.69,1\n 0\n /\n" | ./isasugra.x')
    #os.system('echo "test_slha.isa\n test_slha.slha\n /\n 2\n 1e5,2e5,3,40,+1,172.69,1\n 0\n /\n" | ./isasugra.x')
    os.system(arg_string)

    # now grep the ISA output format (simpler than  SLHA format) to
    # see what happend

    # first, this line redisplays the input values for convenience
    os.system('grep -A 1 Lambda {0}'.format(filename))

    #then probe whatever results one wants - here, its the TAU1 mass
    os.system('grep M\(TAU1\) {0}'.format(filename))

print("Done")
