import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

# Load and prepare graph
filepath = r"C:\Users\ASUS\Documents\Assignment2\map.osm"
G = ox.graph_from_xml(filepath)
original_graph = ox.project_graph(G)
original_graph = ox.project_graph(original_graph)  # Convert to UTM coordinates
print("Number of nodes",len(G.nodes(data=True)))
print("Number of edges",len(G.edges(data=True)))
# Convert to simple undirected graph for analysis
undirected_simple = nx.Graph(original_graph.to_undirected())
largest_cc = max(nx.connected_components(undirected_simple), key=len)
subgraph_simple = undirected_simple.subgraph(largest_cc)

# Calculate Katz centrality
try:
    katz_centrality = nx.katz_centrality(subgraph_simple, alpha=0.005, beta=1.0, max_iter=1000)
except nx.PowerIterationFailedConvergence:
    katz_centrality = nx.katz_centrality(subgraph_simple, alpha=0.005, beta=1.0, max_iter=5000)

# Get top 5 nodes
top_5_nodes = sorted(katz_centrality, key=katz_centrality.get, reverse=True)[:5]


# Prepare visualization parameters
subgraph_original = original_graph.subgraph(largest_cc)
node_colors = ['r' if node in top_5_nodes else '#999999' for node in subgraph_original.nodes()]
node_sizes = [50 if node in top_5_nodes else 20 for node in subgraph_original.nodes()]

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

# Calculate initial zoom area
x_coords = [subgraph_original.nodes[node]['x'] for node in top_5_nodes]
y_coords = [subgraph_original.nodes[node]['y'] for node in top_5_nodes]
buffer = 500  # meters around points

ax.set_xlim(min(x_coords) - buffer, max(x_coords) + buffer)
ax.set_ylim(min(y_coords) - buffer, max(y_coords) + buffer)

# Add zoom buttons
ax_zoom_in = plt.axes([0.8, 0.05, 0.1, 0.075])
ax_zoom_out = plt.axes([0.65, 0.05, 0.1, 0.075])

btn_in = Button(ax_zoom_in, 'Zoom In')
btn_out = Button(ax_zoom_out, 'Zoom Out')

def zoom(factor):
    # Get current limits
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()

    # Compute center
    x_center = (xlim[0] + xlim[1]) / 2
    y_center = (ylim[0] + ylim[1]) / 2

    # Compute width and height
    x_width = (xlim[1] - xlim[0]) * factor / 2
    y_height = (ylim[1] - ylim[0]) * factor / 2

    # Set new limits centered around the current center
    ax.set_xlim(x_center - x_width, x_center + x_width)
    ax.set_ylim(y_center - y_height, y_center + y_height)
    plt.draw()

def zoom_in(event):
    zoom(0.8)  # Zoom in by reducing view

def zoom_out(event):
    zoom(1.25)  # Zoom out by increasing view


btn_in.on_clicked(zoom_in)
btn_out.on_clicked(zoom_out)

plt.title('Top 5 Katz Centrality Nodes (Use Mouse to Pan/Zoom)')
plt.show()