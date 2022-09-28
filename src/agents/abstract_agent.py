# ----- Imports ----- #

# External imports
from abc import ABC, abstractmethod
import networkx as nx

# ----- Main ----- #

class Agent(ABC):
	"""
	The abstract Agent class is defines the underlying structure of the blue, red, and grey agents
	"""
	
	@abstractmethod
	def initialize(self, energy: float = 1.0, is_gray: bool = False):
		"""
		The initialize function is used to initialise any internal logic that is used by the 
		agent. This function is called just before the simulation begins.

		The implementing calss should call self.super()

		Parameters:
			energy: Energy represents the maximum energy a team can have and should be a value between 0 and 1. (default: 1)
		"""
		self.energy = energy
		self.max_energy = energy
		self.is_gray = is_gray
		pass

	@abstractmethod
	def update(self, G: nx.Graph, weights: list):
		"""
		The update function is called at every time interval of teh simulation and is used to get
		the moves that the agent wants to perform in it's current move.

		Parameters:
			G: The current graph
			weights: The current weights of the Agent to each of the nodes in the graph.

		Returns:
			When called the function returns what move the agent wants to perform during its turn.
		"""
		pass

	@abstractmethod
	def get_summary(self) -> dict:
		"""
		The summary function is used to report data from the agent.

		Returns:
			When called a dictionary is returned which contains details about the current state of the agent.
		"""
		pass

	@abstractmethod
	def get_grey_agent():
		"""
		Called in order to produce a grey agent

		Returns:
			A grey agent
		"""
		pass