# Imports
from random import randint, sample
import networkx as nx
from numpy.random import binomial

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
				node_weights = []

				for i in G.nodes():		# for each node
					node_weight = 0
					for j in G.edges(i, data="weight"):		# Gets the edge weights for the node
						node_weight += j[2]
					if not willvotes[i]:	# Only counts node if it holds the opinion not to vote
						node_weights.append([node_weight, i])

				# Gets the nodes with the highest edge weights
				node_weights.sort()
				best_weights = node_weights[-BLUE_TEAM_EDUCATE_AMOUNT:]
				nodes = []
				for i in best_weights:
					nodes.append(i[1])

				# Returning move
				return {'move': move, 'nodes': nodes}

		return {'move': None}

	def get_summary(self) -> dict:
		return "Not a whole lot going on in here ........ cause it's random"

	def get_grey_agent(self):
		return SmartBlueAgent()