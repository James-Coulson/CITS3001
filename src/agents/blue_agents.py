# Imports
from random import randint, sample
import networkx as nx
from numpy.random import binomial
from math import inf

from src.constants import BLUE_TEAM_EDUCATE_AMOUNT
from .abstract_agent import Agent

class UserBlueAgent(Agent):
	#
	#	Agent used for user play
	#
	def initialize(self, energy: float = 1.0, is_gray: bool = False):
		return super().initialize(energy, is_gray)
		
	def update(self, G: nx.Graph, weights: list):
		# Printing agent summary
		print(f"------ It's your turn (Blue) -------")
		if self.is_gray: print("     !! This is the gray agent !!")
		print(f"You have {round(self.energy, 5)} / {self.max_energy} energy")
		print("There have three possible moves\n  - 'connect'\n  - 'educate'\n  - 'gray")

		while True:
			# Creating new line
			print("")

			# Getting user move and checking it is valid
			move = input("What move would you like to make: ")
			if move not in ['connect', 'educate', 'gray']:
				print(f"{move} is not a valid move")
				continue
				
			if move == 'connect':
				node1 = int(input("Node 1: "))
				if node1 not in list(G.nodes):
					print(f"{node1} is not a valid node")
					continue

				node2 = int(input("Node 2: "))
				if node2 not in list(G.nodes):
					print(f"{node2} is not a valid node")
					continue

				return {'move': move, 'nodes': [node1, node2]}

			elif move == 'educate':
				node1 = int(input("Node 1: "))
				if node1 not in list(G.nodes):
					print(f"{node1} is not a valid node")
					continue
				
				node2 = int(input("Node 2: "))
				if node2 not in list(G.nodes):
					print(f"{node2} is not a valid node")
					continue

				node3 = int(input("Node 3: "))
				if node3 not in list(G.nodes):
					print(f"{node3} is not a valid node")
					continue

				return {'move': move, 'nodes': [node1, node2, node3]}
			
			elif move == 'gray':
				return {'move': move}
			
			# Something went wrong if you get here
			print("!!!! Something went wrong. You should be here. !!!!")
			break

		
		print("------ Your turn has ended -------")

	def get_summary(self) -> dict:
		return "This is the user agent..."

	def get_grey_agent(self):
		return UserBlueAgent()


class RandomBlueAgent(Agent):
	#
	#	A completely random agent
	#
	def initialize(self, energy: float = 1.0, is_gray: bool = False):
		return super().initialize(energy, is_gray)
		
	def update(self, G: nx.Graph, weights: list, oppweights: list):
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
	def initialize(self, energy: float = 1.0, is_gray: bool = False, score_edu_redweights: float = 1.0, score_edu_edges: float = 0.05, score_edu_unc: float = 0.25,
	score_con_dist: float = 1.0, score_con_weight: float = 1.0):
		self.score_edu_redweights = score_edu_redweights
		self.score_edu_edges = score_edu_edges
		self.score_edu_unc = score_edu_unc
		self.score_con_dist = score_con_dist
		self.score_con_weight = score_con_weight
		return super().initialize(energy, is_gray)
		
	def update(self, G: nx.Graph, weights: list, oppweights: list):
		# Scores the two moves and returns the move with the highest score
		def score(G: nx.Graph, moves: list, weights: list, oppweights: list, willvotes: dict, uncertainties: dict, con_nodes: list, edu_nodes: list):
			# Holds the current score for each move
			moves_scores = dict.fromkeys(moves, 0.0)

			# Scoring educate move
			for i in edu_nodes:
				moves_scores['educate'] += oppweights[i] * self.score_edu_redweights
				moves_scores['educate'] += G.degree(i, 'weight') * self.score_edu_edges
				moves_scores['educate'] += uncertainties[i] * self.score_edu_unc
			

			# Scoring Propaganda move
			if con_nodes[0] is None or con_nodes[1] is None:
				return 'educate'
			moves_scores['connect'] += nx.shortest_path_length(G, con_nodes[0], con_nodes[1]) * self.score_con_dist
			moves_scores['connect'] += G.degree(con_nodes[1], 'weight') * self.score_con_weight

			return max(moves_scores, key=moves_scores.get)

		willvotes = nx.get_node_attributes(G, 'willvote')
		uncertainties = nx.get_node_attributes(G, 'uncertainty')

		# Node finding for connect
		rednode = None
		bluenode = None
		n1_uncertainty = -inf
		n2_uncertainty = inf
	
		for i in G.nodes():
			if not willvotes[i] and uncertainties[i] > n1_uncertainty:	# Weakest red team
				rednode = i
				n1_uncertainty = uncertainties[i]
			elif willvotes[i] and uncertainties[i] < n2_uncertainty:	# Strongest blue team 
				bluenode = i
				n2_uncertainty = uncertainties[i]

		con_nodes = [bluenode, rednode]

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
			move = score(G, ['connect', 'educate'], weights, oppweights, willvotes, uncertainties, con_nodes, edu_nodes)
			
			if move == 'connect':
				
				# Returning move
				return {'move': move, 'nodes': con_nodes}
			else:

				# Returning move
				return {'move': move, 'nodes': edu_nodes}

		return {'move': None}

	def get_summary(self) -> dict:
		return "Not a whole lot going on in here ........ cause it's random"

	def get_grey_agent(self):
		return SmartBlueAgent()