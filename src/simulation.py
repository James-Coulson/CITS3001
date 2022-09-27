#
#	Methods used to perform a simulation on a given graph
#

# ----- Imports ----- #

# Expernal imports
import random as rd
import networkx as nx
from statistics import mean, stdev
import matplotlib.pyplot as plt

# Local imports
from .constants import *
from .plotting.graph_plotting import plot_graph
from src.agents.abstract_agent import Agent
from src.agents.blue_agents import RandomBlueAgent
from src.agents.red_agents import RandomRedAgent

# ----- Simulation Methods ----- #

def run_simulation(G: nx.Graph, blue_agent: Agent = RandomBlueAgent(), red_agent: Agent = RandomRedAgent(), max_time: int = 100, uncertainty_int: list = [-0.5, 0.5], plot_frequency: int = None, 
				   colortype = MAP_TEAMS, print_summary: bool = False, plot_statistics: bool = False):
	"""
	Runs the simulation on a given graph

	Parameters:
		G: The given graph
		blue_agent: Blue agent to be used. (default: RandomBlueAgent())
		red_agent: Red agent to be used. (default: RandomRedAgent())
		max_time: The maximum number of interations of the simulation (default: 100)
		uncertainty_int: The uncertainty interval (default [-0.5, 0.5])
		plot_frequency: The frequency of the plot redrawing, if set to None a graph will not be plotted (default: None)
		colortype: The type of color mapping used for a plot (default: MAP_TEAMS))
		print_summary: Whether the summary's from the agents should be printed. (default: False)
		plot_statistics: Whether to plot statistics at the end of the simulation. (default: False)
	"""
	# Defining pos
	pos = nx.spring_layout(G)
	
	# Defining theta min
	theta_min = uncertainty_int[0]

	# Obtaining weights of the graph
	weights = nx.get_edge_attributes(G, 'weight')

	# Player to move variable
	player_to_move = RED

	# Calling intialize for both agents
	blue_agent.initialize()
	red_agent.initialize()

	# Defining statistics variables
	time = list()
	stats = {"time": list(), "uncertainty_avg_up_stdev": list(), "uncertainty_avg": list(), "uncertainty_avg_down_stdev": list(),
			 "willvote_prop": list()}

	# Perform simulation
	for t in range(max_time):
		# ---------------- Player moves ---------------- #
		# Getting player moves
		if player_to_move == RED:
			move = red_agent.update(G, [1] * len(G.nodes()))
		elif player_to_move == BLUE:
			move = blue_agent.update(G, [1] * len(G.nodes()))
		else:
			raise ValueError(f"Invalid player to move value. value:{player_to_move}")

		# Increment player's energy
		red_agent.energy += RED_TEAM_ENERGY_RECOV_RATE
		blue_agent.energy += BLUE_TEAM_ENERGY_RECOV_RATE

		# Print agent summary
		if print_summary:
			if player_to_move == RED:
				print(f"Red Team Summary:\n{red_agent.get_summary()}")
			elif player_to_move == BLUE:
				print(f"Blue Team Summary:\n{blue_agent.get_summary()}")
			else:
				raise ValueError(f"Invalid player to move value. value:{player_to_move}")

		# Increment player_to_move
		player_to_move = (player_to_move + 1) % 2

		# ---------------- Perform time increment ---------------- #

		# Performing diffusion
		uncertainties = nx.get_node_attributes(G, 'uncertainty')

		# Perform diffusion on each node
		for node in list(uncertainties.keys()):
			# Calculate decay
			decay = gamma * (theta_min - uncertainties[node])

			# Calculating diffusion
			diffusion = 0
			for n in G.neighbors(node):
				diffusion += weights[(node, n) if node < n else (n, node)] * (uncertainties[n] - uncertainties[node])

			# Updating uncertainty
			uncertainties[node] += (decay + c * diffusion) * dt

		# Setting new uncertainties
		nx.set_node_attributes(G, uncertainties, 'uncertainty')

		# Uncertainties of the nodes
		uncertainty = nx.get_node_attributes(G, "uncertainty")

		# Defining uncertainty interval width
		uncert_width = uncertainty_int[1] - uncertainty_int[0]

		# Will vote attributes
		willvote = nx.get_node_attributes(G, 'willvote')

		# Changes whether each node will vote or not
		for n in list(willvote.keys()):
			# If the uncertainty is above zero, may change
			if uncertainty[n] > 0:
				change = uncertainty[n] / (uncert_width)
				if change > rd.uniform(uncertainty_int[0], uncertainty_int[1]):
					willvote[n] = not willvote[n]
		
		# Sets the new willvote attributes
		nx.set_node_attributes(G, willvote, "willvote")

		# Recording statistics
		avg_uncert = mean(uncertainty.values())
		stdev_uncert = stdev(uncertainty.values())
		stats["uncertainty_avg"].append(avg_uncert)
		stats["uncertainty_avg_up_stdev"].append(avg_uncert + stdev_uncert)
		stats["uncertainty_avg_down_stdev"].append(avg_uncert - stdev_uncert)
		stats["willvote_prop"].append(sum(willvote.values()) / len(willvote.values()))
		stats["time"].append(t)

		# Call plot_graph
		if plot_frequency is not None and t % plot_frequency == 0:
			plot_graph(G, pos=pos, block=False, colortype = colortype)

	# Printing simulation ended
	print("Simulation ended")
	plt.show()

	if plot_statistics:
		# Plotting uncertainty chart
		plt.title("Uncertainty vs. Time")
		plt.xlabel("Time $t$")
		plt.ylabel("Avg. Uncertainty")
		plt.plot(stats["time"], stats["uncertainty_avg_down_stdev"], label="Avg. Uncertainty - 1 stdev")
		plt.plot(stats["time"], stats["uncertainty_avg"], label="Avg. Uncertainty")
		plt.plot(stats["time"], stats["uncertainty_avg_up_stdev"], label="Avg. Uncertainty + 1 stdev")
		plt.legend()
		plt.show()

		# Plotting voting percentage
		plt.title("Proportion of nodes that will vote vs. Time")
		plt.xlabel("Time $t$")
		plt.ylabel("Proportion will vote $\%$")
		plt.plot(stats["time"], stats["willvote_prop"], label="Proportion will vote")
		plt.legend()
		plt.show()

	return G