#
#	Methods used to plot graphs
#

# ----- Imports ----- #

# External imports
from typing import Callable
import networkx as nx
import matplotlib.pyplot as plt
from colour import Color
from math import floor

# Internal imports
from ..constants import *

# ----- Graph PLotting Methods ----- #

def plot_graph(G: nx.Graph, uncertainty_int: list, layout_function: Callable = nx.spring_layout, block: bool = True, pos = None, colortype: int = MAP_TEAMS, plot_labels: bool = False):
	"""
	Function used to render a graph

	Parameters:
		G: Graph object to be drawn
		uncertainty_int: The uncertainty interval
		layout_function: A callable to be used to determine the layout of the nodes in the graph (default: nx.spring_layout) 
		block: Whether the process should block after rendering the graph (default: True)
		colortype: Determines how the colors of the graph represent the node attributes (default: MAP_TEAMS)
		pos: The position of the nodes in the graph (default: None)
	"""
	# Color mapping depending on option
	if colortype == MAP_TEAMS:	# Mapping according to team values
		color_map = list(nx.get_node_attributes(G, 'team').values())
	elif colortype == MAP_WILLVOTE:	# Mapping according to willvote values
		willvotes = list(nx.get_node_attributes(G, 'willvote').values())
		color_map = []
		# Blue if they are voting, red if not
		for i in willvotes:
			if i:
				color_map.append("blue")
			else:
				color_map.append("red")
	elif colortype == MAP_UNCERTAINTY:	# Mapping according to uncertainty of nodes
		uncertainties = list(nx.get_node_attributes(G, 'uncertainty').values())
		color_map = []
		colors = list(Color("green").range_to(Color("red"), 10))	# Creates a gradient from green to red
		# If certain, node is blue - otherwise, green to red (more certain = green)
		for i in uncertainties:
			if i <= 0:
				color_map.append("blue")
			else:
				color_map.append(str(colors[floor(i/(uncertainty_int[1] + 0.01) * 10)]))
	
	# Defining pos
	if pos is None: pos = layout_function(G)

	# Drawing graph
	nx.draw_networkx_nodes(G, pos, nodelist=G.nodes(), node_color=color_map)

	weights = nx.get_edge_attributes(G, 'weight')
	nx.draw_networkx_edges(G, pos, edgelist = weights.keys(), width = list(weights.values()))

	uncertainties = nx.get_node_attributes(G, "uncertainty")
	willvotes = nx.get_node_attributes(G, "willvote")

	if plot_labels:
		labels = dict()
		for node in G.nodes:
			if colortype == MAP_WILLVOTE:
				labels[node] = f"{uncertainties[node]: .2f}"
			else:
				labels[node] = f"{uncertainties[node]: .2f}\n{willvotes[node]}"
		nx.draw_networkx_labels(G, pos, labels=labels)

	# Blocking
	if block: 
		plt.show()
	else:
		plt.draw()
		plt.pause(0.05)
		plt.clf()