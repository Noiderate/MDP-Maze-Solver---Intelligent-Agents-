from visualize import visualise_utility
from visualize import visualise_utility_with_arrows
from visualize import visualise_utility_estimates
from visualize import visualise_rewards
from grid_utils import is_wall
from grid_utils import check_directions
from utility_utils import get_highest_expected_utility

DISCOUNT_FACTOR = 0.99
DEBUG_MODE = False
THRESHOLD = 0.001
MAX_ITERATIONS = 10000

#rewards of the states as shown in the report. use visualize_rewards to visualise this grid with colours
rewards = [
	[     1, "wall",      1, -0.05, -0.05 ,     1],
	[ -0.05,    -1,  -0.05,      1, "wall",    -1],
	[ -0.05, -0.05,     -1, -0.05,      1 , -0.05],
	[ -0.05, -0.05,  -0.05,    -1, -0.05  ,     1],
	[ -0.05, "wall", "wall", "wall",    -1, -0.05],
	[ -0.05, -0.05,  -0.05, -0.05, -0.05  , -0.05],
]

#utility to be used when calculating current state utility. initialised to 0 for all states.
utility_old = [
	[ 0, 0, 0, 0, 0, 0],
	[ 0, 0, 0, 0, 0, 0],
	[ 0, 0, 0, 0, 0, 0],
	[ 0, 0, 0, 0, 0, 0],
	[ 0, 0, 0, 0, 0, 0],
	[ 0, 0, 0, 0, 0, 0],
]

#utility to be assigned when calculating the next state. will be copied to utility old after each iteration
utility_new = [
	[ 0, 0, 0, 0, 0, 0],
	[ 0, 0, 0, 0, 0, 0],
	[ 0, 0, 0, 0, 0, 0],
	[ 0, 0, 0, 0, 0, 0],
	[ 0, 0, 0, 0, 0, 0],
	[ 0, 0, 0, 0, 0, 0],
]


utility_history = [[row[:] for row in utility_old]]

#main loop for value iteration. will run until convergence or until max iterations is reached
for iteration in range(MAX_ITERATIONS):
    utility_new = [[0 for _ in row] for row in rewards]
    delta = 0

    for x in range(len(rewards)):										#loop through all states in the grid
        for y in range(len(rewards[x])):
            if is_wall(rewards, x, y):
                continue

            possible_directions = check_directions(rewards, x, y)		#check which directions are possible to move to from the current state. will be used to calculate expected utility for each direction				
            highest_utility_from_directions = get_highest_expected_utility(				#get the highest expected utility from the possible directions. this is the value iteration update step where we assume we will take the best action at each step					
                utility_old, possible_directions, x, y, debug=DEBUG_MODE
            )

            utility_new[x][y] = rewards[x][y] + DISCOUNT_FACTOR * highest_utility_from_directions 		#update the utility for the current state using the value iteration formula

			#calculate the difference between the new utility and the old utility for the current state. this will be used to check for convergence. note that this uses the max difference across all states, not the average difference
            diff = abs(utility_new[x][y] - utility_old[x][y])
            delta = max(delta, diff)

    utility_old = [row[:] for row in utility_new]
    utility_history.append([row[:] for row in utility_old])

    if delta < THRESHOLD:
        print(f"Converged after {iteration + 1} iterations.")
        break
else:
    print(f"Stopped after reaching MAX_ITERATIONS={MAX_ITERATIONS}.")

tracked_states = [
	(x, y)
	for x in range(len(rewards))
	for y in range(len(rewards[x]))
	if not is_wall(rewards, x, y)
]
#functions to visualise the utility grid, the utility grid with arrows showing the best action, and the utility estimates for the tracked states across iterations. these functions are defined in visualize.py and use matplotlib to create the visualisations
visualise_rewards(rewards)
visualise_utility(utility_old, rewards_grid=rewards)
visualise_utility_with_arrows(utility_old, rewards_grid=rewards)
visualise_utility_estimates(utility_history, tracked_states)



 