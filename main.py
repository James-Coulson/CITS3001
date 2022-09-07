# External imports
import networkx as nx
import matplotlib.pyplot as plt
import random as rd

# Local imports
from src.constants import *

def setup_graph(num_nodes: int, prob: float = 0.1, new_edges: int = 3, weights: list = [0.9, 0.05, 0.03, 0.02], type_: int = ERDOS_RENYI, seed: int = None) -> nx.Graph:
	# Generating Erdos Renyi Graph
	if type_ == ERDOS_RENYI: G = nx.erdos_renyi_graph(num_nodes, prob, seed)
	elif type_ == BARABASI_ALBERT: G = nx.barabasi_albert_graph(num_nodes, new_edges, seed)
	
	# Defining team probabilites
	weights = [0, weights[0], 1 - weights[3] - weights[2], 1 - weights[3]]	# Green, red, blue, gray

	# Generating attributes for green, red, blue, and gray nodes
	attrs = dict()
	for i in range(num_nodes):
		rand = rd.uniform(0, 1)
		if rand < weights[1]:
			attrs[i] = {'team': 'green'}
		elif rand < weights[2]:
			attrs[i] = {'team': 'red'}
		elif rand < weights[3]:
			attrs[i] = {'team': 'blue'}
		else:
			attrs[i] = {'team': 'gray'}

	# Generating uncertainty level
	for i in range(num_nodes):
		attrs[i]['uncertainty'] = rd.uniform(0, 1)

	# Generating opinion level
	# -- We are assuming that the opinion sways from Red (0) and Blue (1)
	for i in range(num_nodes):
		attrs[i]['opinion'] = rd.uniform(0, 1)

	# Setting node attributes
	nx.set_node_attributes(G, attrs)
	
	print(attrs)

	# Return graph
	return G

def get_color_map(G: nx.Graph) -> list:
	# Defining color_map
	color_map = list()

	# Getting color_map
	for i in range(len(G.nodes)):
		color_map.append(G.nodes[i]['team'])
		
	# Return color_map
	return color_map

def plot_graph(G: nx.Graph, block: bool = True):
	# Get color_map
	color_map = get_color_map(G)
	
	# Drawing graph
	nx.draw(G, node_color=color_map)

	# Blocking
	if block: plt.show()

G = setup_graph(10, new_edges = 4, type_ = BARABASI_ALBERT)
plot_graph(G)