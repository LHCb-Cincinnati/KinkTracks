import xslha

# Read the SLHA file
slha_file = "path/to/your/slha/file.slha"
spc = xslha.read(slha_file)

# Define the stau PDG IDs [it does not have the (-)]
stau_pdg_ids = [1000015]

# Check for the presence of stau particles and extract their information
for pdg_id in stau_pdg_ids:
    if pdg_id in spc.blocks['MASS'].keys():
        mass = spc.blocks['MASS'][pdg_id]
        print(f"Stau with PDG ID {pdg_id} found:")
        print(f"\tMass: {mass}")

        # Extract decay information, if available
        if pdg_id in spc.decays.keys():
            decay_info = spc.decays[pdg_id]
            total_width = decay_info.totalwidth
            print(f"\tTotal width: {total_width}")

            # Print decay channels
            print(f"\tDecay channels:")
            for decay in decay_info.decays:
                branching_ratio = decay.br
                decay_products = decay.ids
                print(f"\t\tBranching ratio: {branching_ratio}, Decay products: {decay_products}")
        else:
            print("\tDecay information not available.")
    else:
        print(f"Stau with PDG ID {pdg_id} not found in the SLHA file.")
