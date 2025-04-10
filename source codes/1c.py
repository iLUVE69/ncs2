import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

# Define city or region
filepath = r"C:\Users\ASUS\Documents\Assignment2\map.osm"
G = ox.graph_from_xml(filepath)

# For each edge, compute an initial travel time based on length and an assumed speed
for u, v, k, data in G.edges(data=True, keys=True):
    # Basic travel time (assuming an average speed of 15 m/s)
    travel_time = data.get("length", 0) / 15.0
    # Increase weight for main roads (e.g., primary, secondary, trunk) by a congestion factor
    highway = data.get("highway", "")
    if isinstance(highway, list):
        highway = highway[0]
    if highway in ['primary', 'secondary', 'trunk']:
        travel_time *= 1.5  # Example adjustment for traffic during peak times
    data["travel_time"] = travel_time


N = G.number_of_nodes()
E = G.number_of_edges()
print(f"Number of nodes: {N}, Number of edges: {E}")

# Extract degrees and plot distribution
degrees = [d for n, d in G.degree()]
plt.figure(figsize=(8, 6))
plt.hist(degrees, bins=np.logspace(np.log10(min(degrees)), np.log10(max(degrees)), 50), color='skyblue', edgecolor='black')
plt.xscale('log')
plt.xlabel("Degree")
plt.ylabel("Frequency")
plt.title("Degree Distribution of the Road Network")
plt.show()