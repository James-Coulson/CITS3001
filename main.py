# ----- Imports ----- #

# Local imports
from src.constants import *
from src.graph_generation import generate_graph
from src.plotting.graph_plotting import plot_graph
from src.simulation import run_simulation

# ----- Main ----- #

# Defining paramters
num_green = 100

# For Erdos-Renyi graph generation
type_ = ERDOS_RENYI
prob = 0.2

# Generate graph
G = generate_graph(20, prob = prob, type_ = BARABASI_ALBERT)

# Plot graph
plot_graph(G)

run_simulation(G, max_time=20)