#
#	Methods used to plot graphs
#

# ----- Imports ----- #

# External imports
from typing import Callable
import networkx as nx
import matplotlib.pyplot as plt

# ----- Graph PLotting Methods ----- #

def plot_graph(G: nx.Graph, layout_function: Callable = nx.spring_layout, block: bool = True):
	"""
	Function used to render a graph

	Parameters:
		G: Graph object to be drawn
		layout_function: A callable to be used to determine the layout of the nodes in the graph (default: nx.spring_layout) 
		block: Whether the process should block after rendering the graph (default: True)
	"""
	# Get color_map
	color_map = list(nx.get_node_attributes(G, 'team').values())
	
	# Defining pos
	pos = layout_function(G)

	# Drawing graph
	nx.draw_networkx_nodes(G, pos, nodelist=G.nodes(), node_color=color_map)

	weights = nx.get_edge_attributes(G, 'weight')
	nx.draw_networkx_edges(G, pos, edgelist = weights.keys(), width = list(weights.values()))

	# Blocking
	if block: plt.show()