# ----- Imports ----- #

# Local imports
from src.agents.blue_agents import SmartBlueAgent, RandomBlueAgent, UserBlueAgent
from src.agents.red_agents import SmartRedAgent, RandomRedAgent, UserRedAgent
from src.constants import *
from src.graph_generation import generate_graph
from src.plotting.graph_plotting import plot_graph
from src.simulation import run_simulation

# ----- Main ----- #

# Defining paramters
num_green = 100

# # For Erdos-Renyi graph generation
# type_ = ERDOS_RENYI
prob = 0.02

# For Barabasi-Albert graph generation
type_ = BARABASI_ALBERT
new_edges = 4

# Defining uncertainty interval
uncertainty_int = [-0.5, 1.0]

# Generate graph
G = generate_graph(100, prob = prob, new_edges = new_edges, uncertainty_int = uncertainty_int, type_ = type_)

# Plot initial graph
plot_graph(G, uncertainty_int, colortype = MAP_WILLVOTE)

# Runs simulation
run_simulation(G, max_time = 300, plot_frequency = 1, uncertainty_int = uncertainty_int, colortype = MAP_WILLVOTE, print_summary=False, plot_statistics=True, red_agent=UserRedAgent(), blue_agent=SmartBlueAgent())

# Plot final graph
plot_graph(G, uncertainty_int, colortype=MAP_WILLVOTE)
