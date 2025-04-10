import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import matplotlib.patches as mpatches

# Load and prepare graph
filepath = r"C:\Users\ASUS\Documents\Assignment2\map.osm"
G = ox.graph_from_xml(filepath)
original_graph = ox.project_graph(G)  # Convert to UTM coordinates

# Convert to simple undirected graph to find the largest connected component
undirected_simple = nx.Graph(original_graph.to_undirected())
largest_cc = max(nx.connected_components(undirected_simple), key=len)

# Extract directed subgraph from the original graph
subgraph_directed = original_graph.subgraph(largest_cc).copy()

# Compute HITS scores (hubs and authorities)
try:
    hits_hubs, hits_authorities = nx.hits(subgraph_directed, max_iter=1000, normalized=True)
except nx.PowerIterationFailedConvergence:
    print("HITS did not converge.")
    hits_hubs, hits_authorities = {}, {}

# Get top 5 hubs and authorities
top_5_authorities = sorted(hits_authorities, key=hits_authorities.get, reverse=True)[:5]
top_5_hubs = sorted(hits_hubs, key=hits_hubs.get, reverse=True)[:5]
top_5_nodes = list(set(top_5_authorities + top_5_hubs))  # Union for zoom and label

# Prepare graph for visualization
subgraph_original = original_graph.subgraph(largest_cc)

# Prepare node colors and sizes
node_colors = []
node_sizes = []
for node in subgraph_original.nodes():
    if node in top_5_authorities and node in top_5_hubs:
        node_colors.append('yellow')  # Both hub and authority
        node_sizes.append(70)
    elif node in top_5_authorities:
        node_colors.append('blue')  # Authority
        node_sizes.append(60)
    elif node in top_5_hubs:
        node_colors.append('green')  # Hub
        node_sizes.append(60)
    else:
        node_colors.append('#999999')  # Default color
        node_sizes.append(20)

# Create figure with zoom controls
fig, ax = plt.subplots(figsize=(10, 10))
ox.plot_graph(
    subgraph_original,
    ax=ax,
    node_color=node_colors,
    node_size=node_sizes,
    edge_linewidth=0.2,
    edge_color='gray',
    bgcolor='k',
    show=False
)

# Set initial zoom area around top nodes
x_coords = [subgraph_original.nodes[node]['x'] for node in top_5_nodes]
y_coords = [subgraph_original.nodes[node]['y'] for node in top_5_nodes]
buffer = 500  # meters
ax.set_xlim(min(x_coords) - buffer, max(x_coords) + buffer)
ax.set_ylim(min(y_coords) - buffer, max(y_coords) + buffer)

# Optional: Add labels to top nodes
for node in top_5_nodes:
    x = subgraph_original.nodes[node]['x']
    y = subgraph_original.nodes[node]['y']
    ax.text(x, y, str(node), fontsize=8, color='white')

# Add zoom buttons
ax_zoom_in = plt.axes([0.8, 0.05, 0.1, 0.075])
ax_zoom_out = plt.axes([0.65, 0.05, 0.1, 0.075])
btn_in = Button(ax_zoom_in, 'Zoom In')
btn_out = Button(ax_zoom_out, 'Zoom Out')

def zoom(factor):
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    x_center = (xlim[0] + xlim[1]) / 2
    y_center = (ylim[0] + ylim[1]) / 2
    x_width = (xlim[1] - xlim[0]) * factor / 2
    y_height = (ylim[1] - ylim[0]) * factor / 2
    ax.set_xlim(x_center - x_width, x_center + x_width)
    ax.set_ylim(y_center - y_height, y_center + y_height)
    plt.draw()

btn_in.on_clicked(lambda event: zoom(0.8))
btn_out.on_clicked(lambda event: zoom(1.25))

# Add legend
legend_handles = [
    mpatches.Patch(color='blue', label='Top Authority'),
    mpatches.Patch(color='green', label='Top Hub'),
    mpatches.Patch(color='yellow', label='Top Hub & Authority')
]
plt.legend(handles=legend_handles, loc='lower left', fontsize='small')

plt.title('Top 5 HITS Centrality Nodes (Use Mouse to Pan/Zoom)', color='white')
plt.show()
