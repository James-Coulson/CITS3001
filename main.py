import networkx as nx
import matplotlib.pyplot as plt

def setup_graph(num_nodes: int, prob: float, seed=None) -> nx.Graph:
	# Generating Erdos Renyi Graph
	G = nx.erdos_renyi_graph(num_nodes, prob, seed)
	
	# Return graph
	return G

def plot_graph(G: nx.Graph, block: bool = True):
	# Drawing graph
	nx.draw(G)
	plt.show()

G = setup_graph(30, 0.4)
plot_graph(G)