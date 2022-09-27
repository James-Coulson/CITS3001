#
#	Different moves that the red / blue agents can make
#

# ------ Imports ------ #

# External imports
import networkx as nx
import matplotlib.pyplot as plt
import random as rd

# Local imports
from .constants import *

# ----- Red Team Moves ----- #

# Removes the node from the graph (Red)
def kill(G: nx.Graph, node: int,  blue_weights: list, red_weights: list) -> nx.Graph:
	# Removes the node from the graph
	G.remove_node(node)
	
	# Removing connection of the agents to the green population
	red_weights[node] = 0
	blue_weights[node] = 0
	return G

# Broadcasts propaganda to nodes that are connected to the agent - potential to lose edges (Red)
# TODO: implement weight for losing edge connection into parameters
def propaganda(G: nx.Graph, red_weights: list, potency: int, uncertainty_int: list) -> nx.Graph:
	
	# Iterates over each connection to red agent
	for i in range(len(red_weights)):
		# Potentially loses a connection
		if rd.uniform(0, 1) < (potency * RED_TEAM_POTENCY_CHANGE):
			red_weights[i] = 0
	
	# Gets the node attributes
	willvotes = nx.get_node_attributes(G, 'willvote')
	uncertainties = nx.get_node_attributes(G, 'uncertainty')

	# Iterates over nodes to increase or decrease uncertainty
	for i in range(len(willvotes)):
		# If the node will vote, increases uncertiainty
		if willvotes[i]:
			uncertainties[i] += (potency * RED_TEAM_POTENCY_CHANGE)
		# If node will not vote, decreases uncertainty
		elif not willvotes[i]:
			uncertainties[i] -= (potency * RED_TEAM_POTENCY_CHANGE)
		
		# Ensures the uncertainty is kept within the allowed range
		if uncertainties[i] < uncertainty_int[0]:
			uncertainties[i] = uncertainty_int[0]
		elif uncertainties[i] < uncertainty_int[1]:
			uncertainties[i] = uncertainty_int[1]
		
	# Setting new uncertainties and willvotes
	nx.set_node_attributes(G, uncertainties, 'uncertainty')
	nx.set_node_attributes(G, willvotes, 'willvote')

	return G

# ----- Blue Team Moves ----- #

# Educates a node, causing it to be certain to vote and removes connection to red
def educate(G: nx.Graph, uncertainty_int: list, node: int, red_weights: list) -> nx.Graph:
	# Gets the node attributes
	willvotes = nx.get_node_attributes(G, 'willvote')
	uncertainties = nx.get_node_attributes(G, 'uncertainty')

	# Assigns new variables
	willvotes[node] = True
	uncertainties[node] = uncertainty_int[0]
	red_weights[node] = 0

	# Sets the new willvote/uncertainty attributes
	nx.set_node_attributes(G, willvotes, "willvote")
	nx.set_node_attributes(G, uncertainties, "willvote")

	return G

# Connects two green nodes together and assigns it a high weight value
def connect(G: nx.Graph, nodes: list) -> nx.Graph:
	# Adds to edge to graph
	edge_weight = rd.uniform(0.7, 1.0)
	G.add_edge(nodes[0], nodes[1], weight=edge_weight)

	return G