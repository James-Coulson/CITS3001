#
#
#

import networkx as nx

import matplotlib.pyplot as plt

from .constants import *

def run_simulation(G: nx.Graph, max_time: int = 100, uncertainty_int: list = [-0.5, 0.5]):
	# Defining theta min
	theta_min = uncertainty_int[0]
	
	# Obtaining weights of the graph
	weights = nx.get_edge_attributes(G, 'weight')

	Y1 = list()
	Y2 = list()
	X = list()

	# Perform simulation
	for t in range(max_time):
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

	return G