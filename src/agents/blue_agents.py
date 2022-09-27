# Imports
from random import randint
import networkx as nx
from numpy.random import binomial
from .abstract_agent import Agent


class RandomBlueAgent(Agent):
	#
	#	A completely random agent
	#
	def initialize(self, energy: float = 1.0):
		return super().initialize(energy)
		
	def update(self, G: nx.Graph, weights: list):
		if self.energy > 0.1:
			move = 'connect' if binomial(1, 0.5) else 'educate'
			
			if move == 'connect':
				# Generating node 1 and 2
				node1 = randint(0, len(G.nodes()) - 1)
				node2 = randint(0, len(G.nodes()) - 1)
				
				# Ensuring node 1 and node 2 are not the same
				while node2 == node1:
					node2 = randint(0, len(G.nodes()) - 1)
				
				# Returning moce
				return {'move': move, 'nodes': [node1, node2]}
			else:
				# Generate node to educate
				node = randint(0, len(G.nodes()) - 1)

				# Returning move
				return {'move': move, 'node': node}

		return {'move': None}

	def get_summary(self) -> dict:
		return "Not a whole lot going on in here ........ cause it's random"