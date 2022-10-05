# Imports
from random import randint, sample
import networkx as nx
from numpy.random import binomial
from math import inf

from src.constants import BLUE_TEAM_EDUCATE_AMOUNT
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
				
				# Generates randomly node to educate
				nodes = sample(list(G.nodes), BLUE_TEAM_EDUCATE_AMOUNT)

				# Returning move
				return {'move': move, 'nodes': nodes}
		else:
			return {"move": 'gray'}

	def get_summary(self) -> dict:
		return "Not a whole lot going on in here ........ cause it's random"

	def get_grey_agent(self):
		return RandomBlueAgent()


class SmartBlueAgent(Agent):
	#
	#	A smart blue agent
	#
	def initialize(self, energy: float = 1.0, is_gray: bool = False, score_edu_redweights: float = 1.0, score_edu_edges: float = 1.0, score_edu_unc: float = 1.0):
		self.score_edu_redweights = score_edu_redweights
		self.score_edu_edges = score_edu_edges
		self.score_edu_unc = score_edu_unc
		return super().initialize(energy, is_gray)
		
	def update(self, G: nx.Graph, weights: list, oppweights: list):
		# Scores the two moves and returns the move with the highest score
		def score(G: nx.Graph, moves: list, weights: list, oppweights: list, willvotes: dict, con_nodes: list, edu_nodes: list):
			
			return 1


		willvotes = nx.get_node_attributes(G, 'willvote')
		uncertainties = nx.get_node_attributes(G, 'uncertainty')

		# Node finding for connect
		node1 = None
		node2 = None
		n1_uncertainty = -inf
		n2_uncertainty = inf
	
		for i in G.nodes():
			if not willvotes[i] and uncertainties[i] > n1_uncertainty:	# Weakest red team
				node1 = i
				n1_uncertainty = nx.get_node_attributes(G.node(i), 'uncertainty')
			elif willvotes[i] and uncertainties[i] < n2_uncertainty:	# Strongest blue team 
				node2 = i
				n2_uncertainty = nx.get_node_attributes(G.node(i), 'uncertainty')
		
		con_nodes = [node1, node2]

		edu_nodes = []
		
		# Creates a list with each nodes total weight to neighbours and their node num to sort
		node_weights = []
		for i in G.nodes():		# for each node
			if not willvotes[i]:	# Only counts node if it holds the opinion not to vote
				node_weights.append([G.degree(i, 'weight'), i])

		# Gets the nodes with the highest edge weights
		node_weights.sort()
		best_weights = node_weights[-BLUE_TEAM_EDUCATE_AMOUNT:]
		for i in best_weights:
			edu_nodes.append(i[1])



		if self.energy > 0.1:
			move = score(G, ['connect', 'educate'], weights, oppweights, willvotes, con_nodes, edu_nodes)
			
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

				# Returning move
				return {'move': move, 'nodes': nodes}

		return {'move': None}

	def get_summary(self) -> dict:
		return "Not a whole lot going on in here ........ cause it's random"

	def get_grey_agent(self):
		return SmartBlueAgent()