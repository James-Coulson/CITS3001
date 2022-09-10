# ----- Imports ----- #

# Local imports
from src.constants import *
from src.graph_generation import generate_graph
from src.plotting.graph_plotting import plot_graph
from src.simulation import run_simulation

# ----- Main ----- #

# Generate graph
G = generate_graph(25, new_edges = 4, type_ = BARABASI_ALBERT)

# Runs simulation
run_simulation(G)

# Plot graph
plot_graph(G)

