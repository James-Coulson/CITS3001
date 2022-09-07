import networkx as nx
import matplotlib.pyplot as plt
import random as rd




def setup_graph(num_nodes: int, prob: float, seed=None) -> nx.Graph:
	# Generating Erdos Renyi Graph
	G = nx.erdos_renyi_graph(num_nodes, prob, seed)
	
	# Defining team probabilites
	weights = [0.4, 0.3, 0.3]
	weights = [0, weights[0], 1 - weights[2]]	# Green, red, blue

	# Generating array for green, red, and blue nodes
	attrs = dict()
	for i in range(num_nodes):
		rand = rd.uniform(0, 1)
		if rand < weights[1]:
			attrs[i] = {'team': 'green'}
		elif rand < weights[2]:
			attrs[i] = {'team': 'red'}
		else:
			attrs[i] = {'team': 'blue'}
	
	print(attrs)

	nx.set_node_attributes(G, attrs)
	
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

G = setup_graph(30, 0.2)
plot_graph(G)