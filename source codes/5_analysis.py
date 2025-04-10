import osmnx as ox
import networkx as nx

# Load and prepare graph
filepath = r"C:\Users\ASUS\Documents\Assignment2\map.osm"
G = ox.graph_from_xml(filepath)

# Convert to undirected graph and get largest component
G_undir = nx.Graph(G)
largest_cc = max(nx.connected_components(G_undir), key=len)
G_sub = G_undir.subgraph(largest_cc)

# Get top 10 nodes by degree
degrees = dict(G_sub.degree())
top_nodes = sorted(degrees.items(), key=lambda x: x[1], reverse=True)[:10]

# Calculate local clustering coefficients for top nodes
local_clustering = nx.clustering(G_sub)
top_nodes_clustering = [(node, degrees[node], local_clustering[node]) 
                       for node, _ in top_nodes]

# Print results
print("Top 10 Nodes by Degree - Local Clustering Coefficients")
print("{:<10} {:<10} {:<25}".format("Node ID", "Degree", "Clustering Coefficient"))
print("-" * 45)
for node, degree, cc in top_nodes_clustering:
    print("{:<10} {:<10} {:<25.4f}".format(node, degree, cc))


# Method 1: Transitivity (recommended for road networks)
transitivity = nx.transitivity(G_sub)
print(f"Global Clustering Coefficient (Transitivity): {transitivity:.4f}")

# Method 2: Average Local Clustering Coefficient
avg_clustering = nx.average_clustering(G_sub)
print(f"Average Local Clustering (Global Metric): {avg_clustering:.4f}")