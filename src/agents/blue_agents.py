# Imports
from random import randint
import networkx as nx
from numpy.random import binomial
from .abstract_agent import Agent


class RandomBlueAgent(Agent):
	#
	#	A completely random agent
	#
	def initialize(self, energy: float = 1.0, is_gray: bool = False):
		return super().initialize(energy, is_gray)
		
	def update(self, G: nx.Graph, weights: list):
		if self.energy > 0.3:
			move = 'connect' if binomial(1, 0.5) else 'educate'
			
			if move == 'connect':
				# Generating node 1 and 2
				node1 = list(G.nodes)[randint(0, len(G.nodes()) - 1)]
				node2 = list(G.nodes)[randint(0, len(G.nodes()) - 1)]
				
				# Ensuring node 1 and node 2 are not the same
				while node2 == node1:
					node2 = list(G.nodes)[randint(0, len(G.nodes()) - 1)]
				
				# Returning moce
				return {'move': move, 'nodes': [node1, node2]}
			else:
				
				# Generate node to educate
				node = list(G.nodes)[randint(0, len(G.nodes()) - 1)]

				# Returning move
				return {'move': move, 'node': node}
		else:
			return {"move": 'gray'}

		return {'move': None}

	def get_summary(self) -> dict:
		return "Not a whole lot going on in here ........ cause it's random"

	def get_grey_agent(self):
		return RandomBlueAgent()


class SmartBlueAgent(Agent):
	#
	#	A completely random agent
	#
	def initialize(self, energy: float = 1.0, is_gray: bool = False):
		return super().initialize(energy, is_gray)
		
	def update(self, G: nx.Graph, weights: list):
		if self.energy > 0.1:
			move = 'connect' if binomial(1, 0.5) else 'educate'
			
			if move == 'connect':
				# Generating node 1 and 2
				node1 = list(G.nodes)[randint(0, len(G.nodes()) - 1)]
				node2 = list(G.nodes)[randint(0, len(G.nodes()) - 1)]
				
				# Ensuring node 1 and node 2 are not the same
				while node2 == node1:
					node2 = list(G.nodes)[randint(0, len(G.nodes()) - 1)]
				
				# Returning moce
				return {'move': move, 'nodes': [node1, node2]}
			else:
				willvotes = nx.get_node_attributes(G, 'willvote')
				max_weight = 0
				node = None
				for i in G.nodes():		# for each node
					node_weight = 0
					for j in G.edges(i, data="weight"):		# Gets the edge weights for the node
						node_weight += j[2]
					
					# If total weight is higher than current max and node will not vote, assigns new target
					if node_weight > max_weight and not willvotes[i]:
						max_weight = node_weight
						node = i

				# Returning move
				return {'move': move, 'node': node}

		return {'move': None}

	def get_summary(self) -> dict:
		return "Not a whole lot going on in here ........ cause it's random"

	def get_grey_agent(self):
		return SmartBlueAgent()