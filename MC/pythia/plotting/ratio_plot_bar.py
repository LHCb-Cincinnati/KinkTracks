import matplotlib.pyplot as plt
import numpy as np

# Read the particle counts from the file
particle_counts = {}
with open("data/particle_counts_10000mm.txt", "r") as f:
    for line in f:
        if line.startswith("#"):
            key, value = line[1:].strip().split(":")
            particle_counts[key.strip()] = int(value.strip())

# Calculate the ratios
ratios = {
    "StausInAcc": particle_counts["Stau in LHCb Acc"] / particle_counts["Total stau"],
    "GInAcc": particle_counts["Gravitino in LHCb Acc"] / particle_counts["Total gravitino"],
    "TauInAcc": particle_counts["Taus in LHCb Acc"] / particle_counts["Total tau"],
    "Tau < Stau": particle_counts["Tau from stau"] / particle_counts["Total stau"],
    "G < Stau": particle_counts["Gravitino from stau"] / particle_counts["Total stau"],
}

# Plot the ratios
fig, ax = plt.subplots()
bars = ax.bar(ratios.keys(), ratios.values(), color=["tab:blue", "tab:orange", "tab:green", "tab:red", "tab:purple"])
plt.xticks(rotation=45, ha="right")
plt.ylabel("Ratio")
plt.ylim(0, 0.2)
plt.title("Particle Ratios (Stau = 100 GeV, ctau = 10000 cm)")

# Display the rounded ratios on top of the bars
for bar, ratio in zip(bars, ratios.values()):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height(),
        f"{ratio:.2f}",
        ha="center",
        va="bottom",
        fontsize=8,
    )

# Improve the visual appearance
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()

# Show the plot
plt.savefig("plots/particles/particle_ratios_10000mm.pdf")
plt.show()
