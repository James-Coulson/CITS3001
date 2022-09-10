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
G = generate_graph(5, prob = prob, type_ = BARABASI_ALBERT)

# Runs simulation
run_simulation(G, max_time=5)

# Plot graph
plot_graph(G)
