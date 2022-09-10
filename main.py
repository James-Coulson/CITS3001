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
prob = 0.02

# Defining uncertainty interval
uncertainty_int = [-0.4, 0.4]

# Generate graph
G = generate_graph(100, prob = prob, uncertainty_int = uncertainty_int, type_ = BARABASI_ALBERT)

# Plot initial graph
plot_graph(G, colortype = MAP_UNCERTAINTY)

# Runs simulation
run_simulation(G, max_time = 300, plot_frequency = 1, uncertainty_int = uncertainty_int, colortype = MAP_UNCERTAINTY)

# Plot final graph
plot_graph(G)
