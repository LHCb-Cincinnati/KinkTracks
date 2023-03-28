import matplotlib.pyplot as plt

def read_particle_counts(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
        counts = [int(line.strip().split()[-1]) for line in lines]
        return counts

ln = '10'
file_path = 'data/particle_counts_' + ln + 'mm.txt'

counts = read_particle_counts(file_path)

particles = [
    'Stau_total',
    'G_total',
    'Tau_total',
    'StauInAcc',
    'GInAcc',
    'TauInAcc',
    'Tau<Stau',
    'G<Stau'
]

# Set the color palette
colors = plt.cm.tab10.colors

# Increase the figure size
plt.figure(figsize=(15, 10))

bars = plt.bar(particles, counts, color=colors)
plt.ylabel('Number of Particles')
plt.title('Number of particles \nStau = 100 GeV, ctau = ' + ln + ' mm')
plt.xticks(rotation=45, ha='right')
plt.ylim(0, 35000)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Add the actual number on top of the bar itself
for bar in bars:
    height = bar.get_height()
    plt.gca().annotate('{0}'.format(height),
                       xy=(bar.get_x() + bar.get_width() / 2, height),
                       xytext=(0, 3),
                       textcoords="offset points",
                       ha='center', va='bottom')

plt.tight_layout()
plt.savefig('plots/particles/Stau_100GeV/particles_numbers_' + ln + 'mm.pdf')
plt.show()

