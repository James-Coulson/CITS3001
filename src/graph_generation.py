#
#	Methods used to generate graphs
#

# ------ Imports ------ #

# External imports
import networkx as nx
import matplotlib.pyplot as plt
import random as rd

# Local imports
from .constants import *

# ----- Graph Generation Methods ----- #

def generate_graph(num_nodes: int, prob: float = 0.1, new_edges: int = 3, probs_team: list = [0.9, 0.05, 0.03, 0.02], type_: int = ERDOS_RENYI, seed: int = None) -> nx.Graph:
	"""
	Setups up the initial graph to be used in the simulation

	Parameters:
		num_nodes: The number of nodes in the graph
		prob: The probability of connection, when using Erdos-Renyi to generate the graph (default: 0.1)
		new_edges: The number of new edges to be attached at each step of the Barabasi-Albert PA Algorithm (default: 3)
		probs_team: The probability of a node being in a specific team in order Green, Red, Blue, and Gray (default: [0.9, 0.05, 0.03, 0.02])
		type_: The type of algoithm to be used to generate the graph, see Graph Generation Types in src/constants.py (default: ERDOS_RENYI)
		seed: A seed variabnle to be used for random processed (default, None)
	"""
	# ----- Initial Setup ----- #

	# Setting random seed
	rd.seed(seed)

	# Defining team probabilites
	probs_team = [0, probs_team[0], 1 - probs_team[3] - probs_team[2], 1 - probs_team[3]]	# Green, red, blue, gray

	# ----- Generating Graph Topology ----- #

	# Generating Erdos Renyi Graph
	if type_ == ERDOS_RENYI: G = nx.erdos_renyi_graph(num_nodes, prob, seed)
	elif type_ == BARABASI_ALBERT: G = nx.barabasi_albert_graph(num_nodes, new_edges, seed)

	# ----- Generating Node Attributes ----- #

	# Defining node atttributes dictionary
	node_attrs = dict()

	# Generating attributes for green, red, blue, and gray nodes
	for i in range(num_nodes):
		rand = rd.uniform(0, 1)
		if rand < probs_team[1]:
			node_attrs[i] = {'team': 'green'}
		elif rand < probs_team[2]:
			node_attrs[i] = {'team': 'red'}
		elif rand < probs_team[3]:
			node_attrs[i] = {'team': 'blue'}
		else:
			node_attrs[i] = {'team': 'gray'}

	# Generating uncertainty level
	for i in range(num_nodes):
		node_attrs[i]['uncertainty'] = rd.uniform(0, 1)

	# Generating opinion level
	# -- We are assuming that the opinion sways from Red (0) and Blue (1)
	# 
	# To look at:
	#  - If a node is already assigned to a team the distribution should be skewed so 
	#    that they are more likely to share the opinion of their team
	for i in range(num_nodes):
		node_attrs[i]['opinion'] = rd.uniform(0, 1)

	# Setting node attributes
	nx.set_node_attributes(G, node_attrs)
	
	# ----- Generating Edge Weights ----- # 

	# Generating edge weights
	for pair in G.edges():
		G[pair[0]][pair[1]]['weight'] = rd.uniform(0, 1)

	# Return graph
	return G