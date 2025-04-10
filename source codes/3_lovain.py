import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from community import community_louvain

# Load and prepare graph
filepath = r"C:\Users\ASUS\Documents\Assignment2\map.osm"
G = ox.graph_from_xml(filepath)
original_graph = ox.project_graph(G)  # Convert to UTM

# Convert to undirected graph for Louvain algorithm
undirected_graph = nx.Graph(original_graph.to_undirected())
largest_cc = max(nx.connected_components(undirected_graph), key=len)
subgraph = undirected_graph.subgraph(largest_cc)

# Detect communities using Louvain algorithm
partition = community_louvain.best_partition(subgraph)
communities = list(set(partition.values()))

# Create colormap for communities
cmap = plt.cm.get_cmap('tab20', len(communities))
community_colors = [cmap(partition[node]) for node in subgraph.nodes]

# Create figure with zoom controls
fig, ax = plt.subplots(figsize=(12, 12))

# Plot communities
ox.plot_graph(
    original_graph.subgraph(largest_cc),
    ax=ax,
    node_color=community_colors,
    node_size=40,
    edge_linewidth=0.5,
    edge_color='gray',
    bgcolor='k',
    show=False
)

# Set initial view to full graph extent
nodes = original_graph.subgraph(largest_cc).nodes
x_coords = [nodes[node]['x'] for node in nodes]
y_coords = [nodes[node]['y'] for node in nodes]
buffer = 100  # meters
initial_xlim = (min(x_coords) - buffer, max(x_coords) + buffer)
initial_ylim = (min(y_coords) - buffer, max(y_coords) + buffer)

ax.set_xlim(initial_xlim)
ax.set_ylim(initial_ylim)

# Add zoom buttons
ax_zoom_in = plt.axes([0.8, 0.05, 0.1, 0.075])
ax_zoom_out = plt.axes([0.65, 0.05, 0.1, 0.075])

btn_in = Button(ax_zoom_in, 'Zoom In')
btn_out = Button(ax_zoom_out, 'Zoom Out')

def zoom(factor):
    """Zoom by a given factor (e.g., 0.8 for zoom in, 1.2 for zoom out)."""
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()

    x_center = (xlim[0] + xlim[1]) / 2
    y_center = (ylim[0] + ylim[1]) / 2

    x_width = (xlim[1] - xlim[0]) * factor / 2
    y_height = (ylim[1] - ylim[0]) * factor / 2

    ax.set_xlim([x_center - x_width, x_center + x_width])
    ax.set_ylim([y_center - y_height, y_center + y_height])
    plt.draw()

def zoom_in(event):
    zoom(0.8)  # Zoom in (scale down)

def zoom_out(event):
    zoom(1.2)  # Zoom out (scale up)

btn_in.on_clicked(zoom_in)
btn_out.on_clicked(zoom_out)
partition = community_louvain.best_partition(subgraph)
communities = list(set(partition.values()))

# Compute and print modularity
modularity_score = community_louvain.modularity(partition, subgraph)
print(f"Modularity score: {modularity_score:.4f}")
plt.title('Louvain Community Detection on Road Network', color='white')
plt.show()
