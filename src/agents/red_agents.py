# Imports
from random import randint, sample
import networkx as nx
from numpy.random import binomial
from .abstract_agent import Agent

class RandomRedAgent(Agent):
	#
	#	A completely random agent
	#
	def initialize(self, energy: float = 1.0):
		return super().initialize(energy)
		
	def update(self, G: nx.Graph, weights: list):
		if self.energy > 0.1:
			move = 'kill' if binomial(1, 0.5) else 'propoganda'
			print(type(list(G.nodes())))
			node = list(G.nodes)[randint(0, len(G.nodes()) - 1)]
			return {'move': move, 'node': node}
		
		return {'move': None}

	def get_summary(self) -> dict:
		return "Not a whole lot going on in here ........ cause it's random"