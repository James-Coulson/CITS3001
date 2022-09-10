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

def generate_graph(num_nodes: int, prob: float = 0.1, prob_vote: float = 0.5, uncertainty_int: list = [-0.5, 0.5], new_edges: int = 3, type_: int = ERDOS_RENYI, seed: int = None) -> nx.Graph:
	"""
	Setups up the initial graph to be used in the simulation

	Parameters:
		num_nodes: The number of nodes in the graph
		prob: The probability of connection, when using Erdos-Renyi to generate the graph (default: 0.1)
		new_edges: The number of new edges to be attached at each step of the Barabasi-Albert PA Algorithm (default: 3)
		prob_vote: Probability that a node has the opinion vote (default: 0.5)
		uncertainty_int: The uncertainty interval (default: [-0.5, 0.5])
		type_: The type of algoithm to be used to generate the graph, see Graph Generation Types in src/constants.py (default: ERDOS_RENYI)
		seed: A seed variable to be used for random processed (default, None)
	"""
	# ----- Initial Setup ----- #

	# Setting random seed
	rd.seed(seed)

	# ----- Generating Graph Topology ----- #

	# Generating Erdos Renyi Graph
	if type_ == ERDOS_RENYI: G = nx.erdos_renyi_graph(num_nodes, prob, seed)
	elif type_ == BARABASI_ALBERT: G = nx.barabasi_albert_graph(num_nodes, new_edges, seed)

	# ----- Generating Node Attributes ----- #

	# Defining node atttributes dictionary
	node_attrs = dict()

	# Generating attributes for green, red, blue, and gray nodes
	for i in range(num_nodes):
		node_attrs[i] = {'team': 'green'}

	# Generating uncertainty level
	for i in range(num_nodes):
		node_attrs[i]['uncertainty'] = rd.uniform(uncertainty_int[0], uncertainty_int[1])

	# Generating opinion
	for i in range(num_nodes):
		node_attrs[i]['willvote'] = True if rd.uniform(0, 1) > prob_vote else False

	# Setting node attributes
	nx.set_node_attributes(G, node_attrs)
	
	# ----- Generating Edge Weights ----- # 

	# Generating edge weights
	for pair in G.edges():
		G[pair[0]][pair[1]]['weight'] = rd.uniform(0, 1)

	# Return graph
	return G