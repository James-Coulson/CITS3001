#
#	Methods used to perform a simulation on a given graph
#

# ----- Imports ----- #

# Expernal imports
from decimal import MAX_EMAX
import random as rd
from numpy.random import binomial
import networkx as nx
from statistics import mean, stdev
import matplotlib.pyplot as plt

# Local imports
from .constants import *
from .plotting.graph_plotting import plot_graph
from .agents.abstract_agent import Agent
from .agents.blue_agents import RandomBlueAgent
from .agents.red_agents import RandomRedAgent
from .moves import *
from .utility import clamp

# ----- Simulation Methods ----- #

def run_simulation(G: nx.Graph, blue_agent: Agent = RandomBlueAgent(), red_agent: Agent = RandomRedAgent(), max_time: int = 100, uncertainty_int: list = [-0.5, 0.5], plot_frequency: int = None, 
				   colortype = MAP_TEAMS, print_summary: bool = False, plot_statistics: bool = False, verbose: bool = False):
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
		verbose: Whether text should be printed during the game. (default: False)
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
	if not hasattr(blue_agent, 'energy'):
		blue_agent.initialize()
	if not hasattr(red_agent, 'energy'):
		red_agent.initialize()

	# Defining statistics variables
	stats = {"time": list(), "uncertainty_avg_up_stdev": list(), "uncertainty_avg": list(), "uncertainty_avg_down_stdev": list(),
			 "willvote_prop": list(), "blue_energy": list(), "red_energy": list()}

	# Red and Blue agent weights
	# TODO: Better calculation of weights, add more chance to not have connection
	red_weights = [rd.uniform(0,1)] * len(G.nodes())
	blue_weights = [rd.uniform(0,1)] * len(G.nodes())

	# Perform simulation
	for t in range(max_time):
		# ---------------- Player moves ---------------- #
		# Getting player moves
		if player_to_move == RED:
			move = red_agent.update(G, red_weights)
		elif player_to_move == BLUE:
			move = blue_agent.update(G, blue_weights)
		else:
			raise ValueError(f"Invalid player to move value. value:{player_to_move}")
		
		# Executes the player's move
		if player_to_move == RED:	# Red team moves
			if move['move'] == 'kill':
				G, energy = kill(G, red_agent, move['node'], blue_weights, red_weights)
				red_agent.energy += energy
			elif move['move'] == 'propaganda':
				G, energy = propaganda(G, red_agent, red_weights, move['potency'], uncertainty_int)
				red_agent.energy += energy
		elif player_to_move == BLUE:	# Blue team moves
			if move['move'] == 'educate':
				G, energy = educate(G, blue_agent, uncertainty_int, move['nodes'], red_weights)
				blue_agent.energy += energy
			elif move['move'] == 'connect':
				G, energy = connect(G, blue_agent, move['nodes'])		# ! Please note it uses a list of 2 nodes, thus the key 'nodes' instead of 'node'
				blue_agent.energy += energy
			elif move['move'] == 'gray':
				red = True if binomial(1, GREY_AGENT_RED_PROB) else False
				grey_agent = red_agent.get_grey_agent() if red else blue_agent.get_grey_agent()
				grey_agent.initialize(is_gray = True)
				
				# Getting move and interpreting move
				move = grey_agent.update(G, red_weights if red else blue_weights)
				
				if verbose:
					print(f"Created a grey agent that was red: {red}")

				if move['move'] == 'kill':
					G, energy = kill(G, grey_agent, move['node'], blue_weights, red_weights)
				elif move['move'] == 'propaganda':
					G, energy = propaganda(G, grey_agent, red_weights, move['potency'], uncertainty_int)
				if move['move'] == 'educate':
					G, energy = educate(G, grey_agent, uncertainty_int, move['nodes'], red_weights)
				elif move['move'] == 'connect':
					G, energy = connect(G, grey_agent, move['nodes'])		# ! Please note it uses a list of 2 nodes, thus the key 'nodes' instead of 'node'
		else:
			raise ValueError(f"Invalid player to move value. value:{player_to_move}")

		# Increment player's energy
		red_agent.energy = clamp(red_agent.energy + RED_TEAM_ENERGY_RECOV_RATE, 0, red_agent.max_energy)
		blue_agent.energy = clamp(blue_agent.energy + BLUE_TEAM_ENERGY_RECOV_RATE, 0, blue_agent.max_energy)

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

		# Getting new weights
		weights = nx.get_edge_attributes(G, 'weight')

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

		# Red Weights regenerate over time
		for i in range(len(red_weights)):
			red_weights[i] += RED_TEAM_WEIGHT_RECOV_RATE

		# Recording statistics
		avg_uncert = mean(uncertainty.values())
		stdev_uncert = stdev(uncertainty.values())
		stats["uncertainty_avg"].append(avg_uncert)
		stats["uncertainty_avg_up_stdev"].append(avg_uncert + stdev_uncert)
		stats["uncertainty_avg_down_stdev"].append(avg_uncert - stdev_uncert)
		stats["red_energy"].append(red_agent.energy)
		stats["blue_energy"].append(blue_agent.energy)
		stats["willvote_prop"].append(sum(willvote.values()) / len(willvote.values()))
		stats["time"].append(t)

		# Call plot_graph
		if plot_frequency is not None and t % plot_frequency == 0:
			plot_graph(G, uncertainty_int, pos=pos, block=False, colortype = colortype)

	# Printing simulation ended
	if verbose:
		print("Simulation ended")
	plt.show()

	# Plotting statistics
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

		# Plotting Energy Levels
		plt.title("Agent energy levels vs. Time")
		plt.xlabel("Time $t$")
		plt.ylabel("Energy Level")
		plt.plot(stats["time"], stats["red_energy"], label="Red energy")
		plt.plot(stats["time"], stats["blue_energy"], label="Blue energy")
		plt.legend()
		plt.show()

	return G, stats