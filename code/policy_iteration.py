from grid_utils import check_directions
from grid_utils import is_wall
from utility_utils import get_expected_utility_for_direction
from visualize import visualise_utility
from visualize import visualise_utility_with_arrows
from visualize import visualise_utility_estimates
from visualize import visualise_rewards

DISCOUNT_FACTOR = 0.99
DEBUG_MODE = False
THRESHOLD = 0.001
#THRESHOLD = 1e-6

#rewards of the states as shown in the report. use visualize_rewards to visualise this grid with colours
rewards = [
	[1, "wall", 1, -0.05, -0.05, 1],
	[-0.05, -1, -0.05, 1, "wall", -1],
	[-0.05, -0.05, -1, -0.05, 1, -0.05],
	[-0.05, -0.05, -0.05, -1, -0.05, 1],
	[-0.05, "wall", "wall", "wall", -1, -0.05],
	[-0.05, -0.05, -0.05, -0.05, -0.05, -0.05],
]

#utility to be used when calculating current state utility. initialised to 0 for all states.
utility_old = [
	[0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0],
]

#utility to be assigned when calculating the next state. will be copied to utility old after each iteration
utility_new = [
	[0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0],
]

#initial policy for all non-wall states. starts with "up" and keeps walls as "wall"
policy = [
	["up", "wall", "up", "up", "up", "up"],
	["up", "up", "up", "up", "wall", "up"],
	["up", "up", "up", "up", "up", "up"],
	["up", "up", "up", "up", "up", "up"],
	["up", "wall", "wall", "wall", "up", "up"],
	["up", "up", "up", "up", "up", "up"],
]

#copy of previous policy. used to check if policy changed after improvement
policy_old = [
	["up", "wall", "up", "up", "up", "up"],
	["up", "up", "up", "up", "wall", "up"],
	["up", "up", "up", "up", "up", "up"],
	["up", "up", "up", "up", "up", "up"],
	["up", "wall", "wall", "wall", "up", "up"],
	["up", "up", "up", "up", "up", "up"],
]

utility_history = [[row[:] for row in utility_old]]

#main loop for policy iteration. alternates between policy evaluation and policy improvement until policy converges
iteration = 0
while True:
    #policy evaluation loop for the current fixed policy. runs until utility convergence
    while True:
        utility_new = [[0 for _ in row] for row in rewards]
        delta = 0

        for x in range(len(rewards)):										#loop through all states in the grid
            for y in range(len(rewards[x])):
                if is_wall(rewards, x, y):
                    continue

                possible_directions = check_directions(rewards, x, y)		#check which directions are possible to move to from the current state. will be used to calculate expected utility for each direction
                utility_from_action = get_expected_utility_for_direction(   #get the expected utility from taking the action specified by the current policy in the current state. up initially
                    utility_old, possible_directions, x, y, policy[x][y], debug=DEBUG_MODE
                )
                #update the utility for the current state using the value iteration formula
                utility_new[x][y] = rewards[x][y] + DISCOUNT_FACTOR * utility_from_action

                #calculate the difference between the new utility and the old utility for the current state. this will be used to check for convergence. note that this uses the max difference across all states, not the average difference
                diff = abs(utility_new[x][y] - utility_old[x][y])
                delta = max(delta, diff)

        utility_old = [row[:] for row in utility_new]
        utility_history.append([row[:] for row in utility_old])
        iteration += 1

        if delta < THRESHOLD:
            print(f"Policy evaluation converged after {iteration} iterations.") #note this is an accumulating value, does not reset after each policy improvement step
            break

    #policy improvement step. choose the best action in each state using current utilities
    for x in range(len(rewards)):
        for y in range(len(rewards[x])):
            if is_wall(rewards, x, y):
                policy[x][y] = "wall"
                continue

            possible_directions = check_directions(rewards, x, y)
            best_direction = None
            best_utility = float("-inf")

            for direction in ["up", "down", "left", "right"]:
                expected_utility = get_expected_utility_for_direction(
                    utility_old, possible_directions, x, y, direction, debug=DEBUG_MODE
                )
                if expected_utility > best_utility:
                    best_utility = expected_utility
                    best_direction = direction

            policy[x][y] = best_direction
        
    if policy != policy_old:
        policy_old = [row[:] for row in policy]
    else:
        print("Policy iteration converged.")
        break

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