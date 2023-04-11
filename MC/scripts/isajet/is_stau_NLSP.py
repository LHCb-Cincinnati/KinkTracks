import xslha

# Read the SLHA file
slha_file = "path/to/your/slha/file.slha"
spc = xslha.read(slha_file)

# Extract particle masses
masses = spc.blocks['MASS']

# Filter out superpartners, gravitino, and negative masses
superpartners = {int(pdg_id): mass for pdg_id, mass in masses.items() if abs(int(pdg_id)) > 1000000 and mass > 0}
gravitino_mass = superpartners.get(1000039, None)

# Determine the LSP
lsp_pdg_id = min(superpartners, key=superpartners.get)
lsp_mass = superpartners[lsp_pdg_id]

if lsp_pdg_id == 1000039:
    print("Gravitino is the LSP.")
else:
    print(f"Gravitino is not the LSP. The LSP is a particle with PDG ID: {lsp_pdg_id} and mass: {lsp_mass}")

# Check if stau is the NLSP
if gravitino_mass is not None:
    del superpartners[1000039]

nlsp_pdg_id = min(superpartners, key=superpartners.get)
nlsp_mass = superpartners[nlsp_pdg_id]

if nlsp_pdg_id in [1000015, 2000015]:
    print("Stau is the NLSP.")
else:
    print(f"The NLSP is not stau. PDG ID of the NLSP: {nlsp_pdg_id}")
