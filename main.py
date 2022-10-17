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
uncertainty_int = [-1, 1]

# Setting the colortype
colortype = MAP_WILLVOTE

# Whether labels for uncertainty and willvote are shown
plot_labels = True

# Generate graph
G = generate_graph(num_green, prob = prob, new_edges = new_edges, uncertainty_int = uncertainty_int, type_ = type_)

# Plot initial graph
plot_graph(G, uncertainty_int, colortype = colortype, plot_labels=plot_labels)

# Runs simulation
# run_simulation(G, max_time = 300, verbose=True, plot_frequency = 1, uncertainty_int = uncertainty_int, colortype = MAP_WILLVOTE, print_summary=False, plot_statistics=True, red_agent=RandomRedAgent(), blue_agent=SmartBlueAgent())


# # ------------------ Trained Smart Red Agent vs Random Blue Agent ------------------ #
# red = SmartRedAgent()
# red.initialize(**{
# 			"score_kill_loss": 0,
# 			"score_kill_weights": 0.8254243013257517,
# 			"score_kill_numnodes": 0,
# 			"score_prop_vote": 0.23159485544034947,
# 			"score_prop_weights": 0.005033958841327069,
# 			"score_prop_loss": 0.7820928399402409,
# 			"score_prop_potency": 1
# 		})

# run_simulation(G, max_time = 300, verbose=True, plot_frequency = 1, uncertainty_int = uncertainty_int, colortype = MAP_WILLVOTE, print_summary=False, plot_statistics=True, red_agent=red, blue_agent=RandomBlueAgent())


# # ------------------ Trained Smart Blue Agent vs Random Red Agent ------------------ #
# blue = SmartBlueAgent()
# blue.initialize(**{
# 			"score_edu_redweights": 1,
# 			"score_edu_edges": 1,
# 			"score_edu_unc": 0.0703925524875619,
# 			"score_con_dist": 1,
# 			"score_con_weight": -1
# 		})

# run_simulation(G, max_time = 300, verbose=True, plot_frequency = 1, uncertainty_int = uncertainty_int, colortype = MAP_WILLVOTE, print_summary=False, plot_statistics=True, red_agent=RandomRedAgent(), blue_agent=blue)


# ------------------ Trained Smart Blue Agent vs Trained Smart Red Agent ------------------ #
blue = SmartBlueAgent()
blue.initialize(**{
			"score_edu_redweights": 1,
			"score_edu_edges": 1,
			"score_edu_unc": 0.0703925524875619,
			"score_con_dist": 1,
			"score_con_weight": -1
		})

red = SmartRedAgent()
red.initialize(**{
			"score_kill_loss": 0,
			"score_kill_weights": 0.8254243013257517,
			"score_kill_numnodes": 0,
			"score_prop_vote": 0.23159485544034947,
			"score_prop_weights": 0.005033958841327069,
			"score_prop_loss": 0.7820928399402409,
			"score_prop_potency": 1
		})

run_simulation(G, max_time = 300, verbose=True, plot_frequency = 1, uncertainty_int = uncertainty_int, colortype = MAP_WILLVOTE, print_summary=False, plot_labels=plot_labels, plot_statistics=True, red_agent=red, blue_agent=blue)


# Plot final graph
plot_graph(G, uncertainty_int, colortype=colortype, plot_labels=plot_labels)
