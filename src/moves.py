#
#	Different moves that the red / blue agents can make
#

# ------ Imports ------ #

# External imports
import networkx as nx
import matplotlib.pyplot as plt
import random as rd

from .agents.abstract_agent import Agent

# Local imports
from .constants import *
from .utility import clamp

# TODO: Have energy of the agent be checked and reduced when a move occurs

# ----- Red Team Moves ----- #

# Removes the node from the graph (Red)
def kill(G: nx.Graph, red_agent: Agent, node: int,  blue_weights: list, red_weights: list) -> nx.Graph:
	# Check red team has enough energy
	if red_agent.energy < -KILL_COST:
		return G, 0.0

	# Iterates over each connection to red agent
	for i in range(len(red_weights)):
		# Potentially loses a connection
		if rd.uniform(0, 1) < (3 * RED_TEAM_FOLLOWER_LOSS_PROB):
			red_weights[i] *= 0

	# Removes the node from the graph
	G.remove_node(node)
	
	# Removing connection of the agents to the green population
	red_weights[node] = 0
	blue_weights[node] = 0

	# Calcualting energy change
	energy = KILL_COST

	return G, energy

# Broadcasts propaganda to nodes that are connected to the agent - potential to lose edges (Red)
# TODO: implement weight for losing edge connection into parameters
def propaganda(G: nx.Graph, red_agent: Agent, red_weights: list, potency: int, uncertainty_int: list) -> nx.Graph:
	# Check red team has enough energy
	if red_agent.energy < -PROPAGANDA_COST:
		return G, 0.0

	# Iterates over each connection to red agent
	for i in range(len(red_weights)):
		# Potentially loses a connection
		if rd.uniform(0, 1) < (potency * RED_TEAM_FOLLOWER_LOSS_PROB):
			red_weights[i] *= 0.5
	
	# Gets the node attributes
	willvotes = nx.get_node_attributes(G, 'willvote')
	uncertainties = nx.get_node_attributes(G, 'uncertainty')

	# Iterates over nodes to increase or decrease uncertainty
	for i in G.nodes():
		# If the node will vote, increases uncertiainty
		if willvotes[i]:
			uncertainties[i] += (potency * RED_TEAM_POTENCY_CHANGE) * red_weights[i]
		# If node will not vote, decreases uncertainty
		elif not willvotes[i]:
			uncertainties[i] -= (potency * RED_TEAM_POTENCY_CHANGE) * red_weights[i] * 0.3
		
		# Ensures the uncertainty is kept within the allowed range
		uncertainties[i] = clamp(uncertainties[i], uncertainty_int[0], uncertainty_int[1])
		
	# Setting new uncertainties and willvotes
	nx.set_node_attributes(G, uncertainties, 'uncertainty')
	nx.set_node_attributes(G, willvotes, 'willvote')

	# Calculating energy change
	energy = PROPAGANDA_COST

	return G, energy

# ----- Blue Team Moves ----- #

# Educates some nodes, causing it to be certain to vote and removes connection to red
def educate(G: nx.Graph, blue_agent: Agent, uncertainty_int: list, nodes: list, red_weights: list) -> nx.Graph:
	# Check blue team has enough energy
	if blue_agent.energy < -EDUCATE_COST:
		return G, 0.0
	
	# Gets the node attributes
	willvotes = nx.get_node_attributes(G, 'willvote')
	uncertainties = nx.get_node_attributes(G, 'uncertainty')

	# Educates nodes from the list, making them certain and voting for blue
	for node in nodes:
		willvotes[node] = True
		uncertainties[node] = uncertainty_int[0]
		red_weights[node] = 0

	# Sets the new willvote/uncertainty attributes
	nx.set_node_attributes(G, willvotes, "willvote")
	nx.set_node_attributes(G, uncertainties, "uncertainty")

	# Calculating energy used
	energy = EDUCATE_COST

	return G, energy

# Connects two green nodes together and assigns it a high weight value
def connect(G: nx.Graph, blue_agent: Agent, nodes: list) -> nx.Graph:
	# Check blue team has enough energy
	if blue_agent.energy < -CONNECT_COST:
		return G, 0.0
	
	# Adds to edge to graph
	edge_weight = rd.uniform(0.7, 1.0)
	G.add_edge(nodes[0], nodes[1], weight=edge_weight)

	# Calculating energy used
	energy = CONNECT_COST

	return G, energy