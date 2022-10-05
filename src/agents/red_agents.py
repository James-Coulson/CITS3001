# Imports
from random import randint, sample
import networkx as nx
from numpy.random import binomial
from .abstract_agent import Agent

class UserRedAgent(Agent):
	#
	#	User play agent
	#
	def initialize(self, energy: float = 1.0, is_gray: bool = False):
		return super().initialize(energy, is_gray)
		
	def update(self, G: nx.Graph, weights: list):
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
		
	def update(self, G: nx.Graph, weights: list):
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