import xslha

# Read the SLHA file
slha_file = "path/to/your/slha/file.slha"
spc = xslha.read(slha_file)

# Extract particle masses
masses = spc.blocks['MASS']

# Filter out superpartners and gravitino
superpartners = {pdg_id: mass for pdg_id, mass in masses.items() if abs(pdg_id) > 1000000}
gravitino_mass = superpartners.get(1000039, None)

# Check if gravitino is the LSP
if gravitino_mass is not None:
    lsp_pdg_id = min(superpartners, key=superpartners.get)
    lsp_mass = superpartners[lsp_pdg_id]

    if lsp_pdg_id == 1000039:
        print("Gravitino is the LSP.")

        # Check if stau is the NLSP
        del superpartners[1000039]
        nlsp_pdg_id = min(superpartners, key=superpartners.get)
        nlsp_mass = superpartners[nlsp_pdg_id]

        if nlsp_pdg_id in [1000015, 2000015]:
            print("Stau is the NLSP.")
        else:
            print(f"The NLSP is not stau. PDG ID of the NLSP: {nlsp_pdg_id}")
    else:
        print("Gravitino is not the LSP.")
else:
    print("Gravitino not found in the SLHA file.")
