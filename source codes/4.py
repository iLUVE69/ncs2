import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress

# Load and prepare graph
filepath = r"C:\Users\ASUS\Documents\Assignment2\map.osm"
G = ox.graph_from_xml(filepath)

# Convert to undirected graph and get largest component
G_undir = nx.Graph(G)
largest_cc = max(nx.connected_components(G_undir), key=len)
G_sub = G_undir.subgraph(largest_cc)

# Calculate Pearson degree assortativity coefficient
pearson_r = nx.degree_assortativity_coefficient(G_sub)
print(f"Pearson Degree Assortativity Coefficient: {pearson_r:.3f}")

# Calculate average neighbor degrees
avg_neighbor_deg = nx.average_neighbor_degree(G_sub)
degrees = dict(G_sub.degree())

# Prepare data for plotting
node_degrees = list(degrees.values())
neighbor_degrees = [avg_neighbor_deg[n] for n in degrees.keys()]

# Bin data for better visualization
degree_bins = np.logspace(np.log10(min(node_degrees)), 
                         np.log10(max(node_degrees)), 
                         20)
bin_centers = []
mean_neighbor_deg = []

for i in range(len(degree_bins)-1):
    mask = (node_degrees >= degree_bins[i]) & (node_degrees < degree_bins[i+1])
    if sum(mask) > 0:
        bin_centers.append(np.sqrt(degree_bins[i] * degree_bins[i+1]))  # Geometric mean
        mean_neighbor_deg.append(np.mean([neighbor_degrees[j] for j in np.where(mask)[0]]))

# Calculate linear regression
slope, intercept, r_value, p_value, std_err = linregress(np.log10(node_degrees), 
                                                       np.log10(neighbor_degrees))

# Create figure
plt.figure(figsize=(10, 6))

# Plot individual points
plt.scatter(node_degrees, neighbor_degrees, 
           alpha=0.3, c='blue', label='Individual Nodes')

# Plot binned averages
plt.plot(bin_centers, mean_neighbor_deg, 
        'r-', lw=2, marker='o', markersize=8, 
        label='Binned Averages')

# Plot regression line
x_reg = np.logspace(np.log10(min(node_degrees)), 
                  np.log10(max(node_degrees)), 100)
y_reg = 10**(slope * np.log10(x_reg) + intercept)
plt.plot(x_reg, y_reg, 'k--', 
        label=f'Fit: y ~ x^{slope:.2f} (R²={r_value**2:.2f})')

# Format plot
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Node Degree (log scale)')
plt.ylabel('Average Neighbor Degree (log scale)')
plt.title(f'Degree-Degree Correlations\nPearson r = {pearson_r:.3f}')
plt.grid(True, which='both', linestyle='--', alpha=0.5)
plt.legend()

plt.tight_layout()
plt.show()