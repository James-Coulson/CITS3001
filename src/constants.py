#
#	Defining constants used in the program,
#

# ----- Graph Generation Types ----- #
# The types of algorithms that can be used to generate the initial graph topology
ERDOS_RENYI = 1
BARABASI_ALBERT = 2

# ---- Colour Mapping Types ----- #
# Color mapping types
MAP_TEAMS = 1
MAP_WILLVOTE = 2
MAP_UNCERTAINTY = 3

# ----- Graph Dynamic System Constants ----- #
# Constants used by the graph's dynamic system.
c = 1				# Rate of diffusion
gamma = 0.05		# Rate of decay
dt = 0.05			# Time increments

# ----- Agent Constants ----- #
# Constatnts used by the agents
RED_TEAM_ENERGY_RECOV_RATE = 0.1
BLUE_TEAM_ENERGY_RECOV_RATE = 0.2

# ----- Moves Constants ----- #
RED_TEAM_REMOVE_CONN = 0.02		# TODO: Implement as parameter
RED_TEAM_POTENCY_CHANGE = 0.2


