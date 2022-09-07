# ----- Imports ----- #

# Local imports
from src.constants import *
from src.graph_generation import generate_graph
from src.plotting.graph_plotting import plot_graph

# ----- Main ----- #

# Generate graph
G = generate_graph(25, new_edges = 4, type_ = BARABASI_ALBERT)

# Plot graph
plot_graph(G)