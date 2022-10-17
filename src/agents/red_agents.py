# Imports
from random import randint, sample
import networkx as nx
from numpy.random import binomial
from .abstract_agent import Agent
from ..constants import *
from math import ceil

class UserRedAgent(Agent):
	#
	#	User play agent
	#
	def initialize(self, energy: float = 1.0, is_gray: bool = False):
		return super().initialize(energy, is_gray)
		
	def update(self, G: nx.Graph, weights: list, oppweights: list):
		# Printing agent summary
		print(f"------ It's your turn (Red) -------")
		if self.is_gray: print("     !! This is the gray agent !!")
		print(f"You have {round(self.energy, 5)} / {self.max_energy} energy")
		print("There have two possible moves\n  - 'propaganda'\n  - 'kill'")

		while True:
			# Creating new line
			print("")

			# Getting user move and checking it is valid
			move = input("What move would you like to make: ")
			if move not in ['propaganda', 'kill']:
				print(f"{move} is not a valid move")
				continue
			
			if move == 'propaganda':
				# TODO: Add potency messages
				potency = int(input("Potency: "))
				if potency < 1 or potency > 5:
					print(f"{potency} is not a valid potency")
					continue

				return {'move': move, 'potency': potency}
			
			elif move == 'kill':
				node = int(input("Node: "))
				if node not in list(G.nodes):
					print(f"{node} is not a valid node")
					continue

				return {'move': move, 'node': node}

			# Something went wrong if you get here
			print("!!!! Something went wrong. You should be here. !!!!")
			break
		
		return {'move': None}

	def get_summary(self) -> dict:
		return "Not a whole lot going on in here ........ cause it's random"
	
	def get_grey_agent(self):
		return UserRedAgent()

class RandomRedAgent(Agent):
	#
	#	A completely random agent
	#
	def initialize(self, energy: float = 1.0, is_gray: bool = False, move_prob: float = 0.3):
		self.move_prob = move_prob
		return super().initialize(energy, is_gray)
		
	def update(self, G: nx.Graph, weights: list, oppweights: list):
		if self.energy > 0.1:
			move = 'kill' if binomial(1, self.move_prob) and len(G.nodes()) > 30 else 'propaganda'
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
	#	A Smart Agent
	#
	def initialize(self, energy: float = 1.0, is_gray: bool = False, score_kill_loss: float = 0.01, score_kill_weights: float = 0.83, score_kill_numnodes: float = 0.1, 
	score_prop_vote: float = 0.23, score_prop_weights: float = 0.005, score_prop_loss: float = 0.78, score_prop_potency: float = 1.0):
		self.score_kill_weights = score_kill_weights
		self.score_kill_loss = score_kill_loss
		self.score_kill_numnodes = score_kill_numnodes
		self.score_prop_vote = score_prop_vote
		self.score_prop_weights = score_prop_weights
		self.score_prop_loss = score_prop_loss
		self.score_prop_potency = score_prop_potency
		return super().initialize(energy, is_gray)
	
	

	def update(self, G: nx.Graph, weights: list, oppweights: list):

		# Scores the moves against eachother and decides the optimum move
		def score(self, G: nx.Graph, weights: list, moves: list, willvotes: dict, potency: int, node: int):
			# Holds the current score for each move
			moves_scores = dict.fromkeys(moves, 0.0)

			# Scoring Kill move
			moves_scores['kill'] -= RED_TEAM_FOLLOWER_LOSS_PROB * self.score_kill_loss
			moves_scores['kill'] += G.degree(node, "weight") * self.score_kill_weights
			moves_scores['kill'] -= len(G.nodes()) * self.score_kill_numnodes

			# Scoring Propaganda move
			moves_scores['propaganda'] += (sum(willvotes.values()) / len(willvotes.values())) * self.score_prop_vote
			moves_scores['propaganda'] += sum(weights) * self.score_prop_weights
			moves_scores['propaganda'] -= RED_TEAM_POTENCY_CHANGE * self.score_prop_loss
			moves_scores['propaganda'] += potency * self.score_prop_potency

			return max(moves_scores, key=moves_scores.get)


		if self.energy > 0.1:

			# Getting the most important node for kill
			willvotes = nx.get_node_attributes(G, 'willvote')
			max_weight = 0
			node = None
			for i in G.nodes():		# for each node
				if G.degree(i, "weight") > max_weight and willvotes[i]:
					node = i
					max_weight = G.degree(i, "weight")

			# Propaganda potency depends on the proportion of people who are voting
			potency = ceil(sum(willvotes.values()) / len(willvotes.values()) * 5)

			move = score(self, G, weights, ['kill', 'propaganda'], willvotes, potency, node)

			# Chooses the node with the highest total weight of it's edges and will vote to kill
			if move == 'kill':

				if node is not None:
					return {'move': move, 'node': node}
			return {'move': move, 'potency': potency}
		
		return {'move': None}

	def get_summary(self) -> dict:
		return "SMART AGENT"		# TODO:  statistics
	
	def get_grey_agent(self):
		return RandomRedAgent()
