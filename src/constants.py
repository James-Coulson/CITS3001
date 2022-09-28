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
gamma = 0.01		# Rate of decay
dt = 0.05			# Time increments

# ----- Agent Constants ----- #
# Constants used by the agents
RED = 0									# Red team identifier
BLUE = 1								# Blue team identifier
RED_TEAM_ENERGY_RECOV_RATE = 0.1		# Rate of energy recovery for red team
BLUE_TEAM_ENERGY_RECOV_RATE = 0.1		# Rate of energy recovery for blue team
RED_TEAM_WEIGHT_RECOV_RATE = 0.05		# Rate of red edge weights recovery

# ----- Moves Constants ----- #
RED_TEAM_POTENCY_CHANGE = 0.1
RED_TEAM_FOLLOWER_LOSS_PROB = 0.02

# Move costs
KILL_COST = -0.7
PROPAGANDA_COST = -0.05
EDUCATE_COST = -0.3
CONNECT_COST = -0.05
