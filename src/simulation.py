#
#	Methods used to perform a simulation on a given graph
#

# ----- Imports ----- #

# Expernal imports
import random as rd
import networkx as nx

# Local imports
from .constants import *

# ----- Simulation Methods ----- #

def run_simulation(G: nx.Graph, max_time: int = 100, uncertainty_int: list = [-0.5, 0.5]):
	# Defining theta min
	theta_min = uncertainty_int[0]
	
	# Obtaining weights of the graph
	weights = nx.get_edge_attributes(G, 'weight')

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

		# Uncertainties of the nodes
		uncertainty = nx.get_node_attributes(G, "uncertainty")

		# PLACEHOLDER UNMAX, UNMIN
		unmax = 0.4
		unmin = -0.4

		# Will vote attributes
		willvote = nx.get_node_attributes(G, 'willvote')

		# Changes whether each node will vote or not
		for n in list(willvote.keys()):
			# If the uncertainty is above zero, may change
			if uncertainty[n] > 0:
				change = uncertainty[n] / (unmax - unmin)
				if change > rd.uniform(unmax, unmin):
					willvote[n] = not willvote[n]
		
		# Sets the new willvote attributes
		nx.set_node_attributes(G, willvote, "willvote")
					
	return G