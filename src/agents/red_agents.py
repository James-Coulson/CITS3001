# Imports
from random import randint, sample
import networkx as nx
from numpy.random import binomial
from .abstract_agent import Agent

class RandomRedAgent(Agent):
	#
	#	A completely random agent
	#
	def initialize(self, energy: float = 1.0, is_gray: bool = False):
		return super().initialize(energy, is_gray)
		
	def update(self, G: nx.Graph, weights: list):
		if self.energy > 0.1:
			move = 'kill' if binomial(1, 0.3) and len(G.nodes()) > 30 else 'propaganda'
			# Chooses the node with the highest total weight of it's edges and will vote to kill
			if move == 'kill':
				node = list(G.nodes)[randint(0, len(G.nodes()) - 1)]
				return {'move': move, 'node': node}
			else:
				potency = randint(1, 5)
				return {'move': move, 'potency': potency}
		
		return {'move': None}

	def get_summary(self) -> dict:
		return "Not a whole lot going on in here ........ cause it's random"
	
	def get_grey_agent(self):
		return RandomRedAgent()

class SmartRedAgent(Agent):
	#
	#	A completely random agent
	#
	def initialize(self, energy: float = 1.0, is_gray: bool = False):
		return super().initialize(energy, is_gray)
		
	def update(self, G: nx.Graph, weights: list):
		if self.energy > 0.1:
			move = 'kill' if binomial(1, 0.7) and len(G.nodes()) > 30 else 'propaganda'
			# Chooses the node with the highest total weight of it's edges and will vote to kill
			if move == 'kill':
				willvotes = nx.get_node_attributes(G, 'willvote')
				max_weight = 0
				node = None
				for i in G.nodes():		# for each node
					node_weight = 0
					for j in G.edges(i, data="weight"):		# Gets the edge weights for the node
						node_weight += j[2]
					
					# If total weight is higher than current max and node will vote, assigns new target
					if node_weight > max_weight and willvotes[i]:
						max_weight = node_weight
						node = i

				if node is not None:
					return {'move': move, 'node': node}
				
				move = 'propoganda'
			
			potency = randint(1, 5)
			return {'move': move, 'potency': potency}
		
		return {'move': None}

	def get_summary(self) -> dict:
		return "SMART AGENT"		# TODO:  statistics
	
	def get_grey_agent(self):
		return RandomRedAgent()