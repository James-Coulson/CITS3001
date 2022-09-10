#
#
#
import random as rd
import networkx as nx


def run_simulation(G: nx.Graph, max_time: int = 100):
	for t in range(max_time):
		# Uncertainties of the nodes
		uncertainty = nx.get_node_attributes(G, "uncertainty")

		# TODO PLACEHOLDER UNMAX, UNMIN
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