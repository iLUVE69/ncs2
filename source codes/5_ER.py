import networkx as nx

# Create ER graph
n = 4217       # Number of nodes
m = 10576      # Number of edges
G = nx.gnm_random_graph(n, m, seed=42)

# Calculate clustering coefficients
global_clustering = nx.transitivity(G)
average_local_clustering = nx.average_clustering(G)

# Theoretical expectation (p = edge probability)
p = 2*m / (n*(n-1))  # For undirected graphs

print(f"Global Clustering Coefficient (Transitivity): {global_clustering:.6f}")
print(f"Average Local Clustering Coefficient: {average_local_clustering:.6f}")