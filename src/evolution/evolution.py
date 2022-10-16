from src.graph_generation import generate_graph
from src.utility import clamp
from ..agents.red_agents import *
from ..agents.blue_agents import *
from ..simulation import run_simulation
from ..constants import *

from random import choice
from copy import deepcopy
import concurrent.futures as thr
from numpy.random import uniform, standard_normal
from numpy import mean
from multiprocessing.connection import wait
from threading import active_count
import matplotlib.pyplot as plt
from json import dumps
from time import process_time

# # For Erdos-Renyi graph generation
# type_ = ERDOS_RENYI
prob = 0.02

# For Barabasi-Albert graph generation
type_ = BARABASI_ALBERT
new_edges = 4

# Defining uncertainty interval
uncertainty_int = [-0.5, 1.0]

def evolution(training_agent: type, params: list, param_bounds: dict, agent_is_red: bool = True, pop_size: int = 50, num_gens: int = 20, sim_time_steps: int = 100,
			  plot: bool = False, verbose: bool = False):
	# Dictionary to store the parameters and utilities of agents for each generation
	training_results = dict()
	
	# File name to store training results
	# now = datetime.now()
	# time = now.strftime("%d/%m/%Y-%H-%M-%S")
	filename = f"training-results-{process_time()}.json"#f"Training_Results-{time}.txt"

	# Generating inital random population
	pop = dict()
	for i in range(pop_size):
		# Generating random parameters
		p = dict()
		for param in params:
			p[param] = uniform(param_bounds[param][0], param_bounds[param][1])

		# Genreating agent
		a = training_agent()
		a.initialize(**p)
		pop[a] = p
	
	# Performing optimisation
	executor = thr.ThreadPoolExecutor(max_workers=20)
	for i in range(num_gens):
		# Generate graph
		G = generate_graph(200, prob = prob, new_edges = new_edges, uncertainty_int = uncertainty_int, type_ = type_)
		res = dict()

		# Performing simulations with population
		results = dict()
		for agent in pop.keys():
			if agent_is_red:
				results[executor.submit(run_simulation, deepcopy(G), uncertainty_int = uncertainty_int, max_time=sim_time_steps, red_agent=agent, blue_agent=RandomBlueAgent())] = agent
			else:
				results[executor.submit(run_simulation, deepcopy(G), uncertainty_int = uncertainty_int, max_time=sim_time_steps, red_agent=RandomRedAgent(), blue_agent=agent)] = agent
		
		# Adding final proportions to dictionary
		for stats in thr.as_completed(results):
			res[results[stats]] = 1 - mean(stats.result()[1]['willvote_prop'][-int(sim_time_steps * 0.3)]) if agent_is_red else mean(stats.result()[1]['willvote_prop'][-int(sim_time_steps * 0.3)])

		# Sorting results
		res = dict(sorted(res.items(), key=lambda item: item[1]))

		# Get top third of population
		top_agents = dict()
		training_results[i] = dict()
		for agent in list(res.keys())[-int(pop_size * 0.1):]:
			top_agents[agent] = pop[agent]
			training_results[i][res[agent]] = pop[agent]

		if verbose:
			print(str(list(res.values())[-int(pop_size * 0.1):]))

		# Saving parameters to file
		with open(filename, 'w') as file:
			file.write(dumps(training_results))

		# Defining new population dict
		new_pop = dict()

		if plot and i % 5 == 0: # This will only work for a 1D agent
			for agent in list(pop.keys()):
				plt.scatter(res[agent], pop[agent]['move_prob'])
			
			plt.xlim(0, 1)
			plt.ylim(0, 1)
			plt.ylabel("Kill probability")
			plt.xlabel("% will not vote")
			plt.show()

		# Mutating population
		for j in range(pop_size):
			# Creating a new agent
			a = training_agent()

			# Randoming get parent
			parent = choice(list(top_agents.keys()))

			# Getting parameters of parent
			child_params = deepcopy(pop[parent])

			# Mutating parent params
			for key in child_params.keys():
				bounds = param_bounds[key]
				change = standard_normal() * (1 - i/num_gens) * (bounds[1] - bounds[0])
				child_params[key] += change
				child_params[key] = clamp(child_params[key], bounds[0], bounds[1])
			
			# Giving child new parameters
			a.initialize(**child_params)

			# Adding agent to new_pop
			new_pop[a] = child_params
		
		# Assigning new population
		pop = new_pop
			

# evolution(RandomRedAgent, plot=True, verbose=True, params=['move_prob'], param_bounds={'move_prob': [0, 1]})
evolution(SmartRedAgent, params=['score_kill_loss', 'score_kill_weights', 'score_kill_numnodes', 'score_prop_vote', 'score_prop_weights', 'score_prop_loss', 'score_prop_potency'], param_bounds={'score_kill_loss': [0, 1], 'score_kill_weights': [0, 1], 'score_kill_numnodes': [0, 1], 'score_prop_vote': [0, 1], 'score_prop_weights': [0, 1], 'score_prop_loss': [0, 1], 'score_prop_potency': [0, 1]}, plot=False, verbose=True)