# ----- Imports ----- #

# Local imports
from turtle import color
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

# Setting the colortype
colortype = MAP_WILLVOTE

# Whether labels for uncertainty and willvote are shown
plot_labels = True

# Generate graph
G = generate_graph(100, prob = prob, new_edges = new_edges, uncertainty_int = uncertainty_int, type_ = type_)

# Plot initial graph
plot_graph(G, uncertainty_int, colortype = colortype, plot_labels=plot_labels)

# Runs simulation
run_simulation(G, max_time = 300, plot_frequency = 1, uncertainty_int = uncertainty_int, colortype = colortype, print_summary=False, plot_labels=plot_labels, plot_statistics=False, red_agent=SmartRedAgent(), blue_agent=RandomBlueAgent())

# Plot final graph
plot_graph(G, uncertainty_int, colortype=colortype, plot_labels=plot_labels)
