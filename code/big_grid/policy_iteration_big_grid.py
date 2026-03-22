import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/..')

from grid_utils import check_directions
from grid_utils import is_wall
from utility_utils import get_expected_utility_for_direction
from visualize import visualise_utility
from visualize import visualise_utility_with_arrows
from visualize import visualise_utility_estimates
from visualize import visualise_rewards
from big_array import get_big_rewards_grid
from big_array import get_random_big_rewards_grid

DISCOUNT_FACTOR = 0.99
DEBUG_MODE = False
THRESHOLD = 0.001
#THRESHOLD = 1e-6

rewards = get_random_big_rewards_grid(rows=100, cols=100)
#rewards = get_big_rewards_grid()

utility_old = [[0 for _ in row] for row in rewards]
utility_new = [[0 for _ in row] for row in rewards]

policy = [
	["wall" if rewards[x][y] == "wall" else "up" for y in range(len(rewards[x]))]
	for x in range(len(rewards))
]
policy_old = [row[:] for row in policy]

utility_history = [[row[:] for row in utility_old]]

iteration = 0
while True:
    while True:
        utility_new = [[0 for _ in row] for row in rewards]
        delta = 0

        for x in range(len(rewards)):
            for y in range(len(rewards[x])):
                if is_wall(rewards, x, y):
                    continue

                possible_directions = check_directions(rewards, x, y)
                utility_from_action = get_expected_utility_for_direction(
                    utility_old, possible_directions, x, y, policy[x][y], debug=DEBUG_MODE
                )
                utility_new[x][y] = rewards[x][y] + DISCOUNT_FACTOR * utility_from_action

                diff = abs(utility_new[x][y] - utility_old[x][y])
                delta = max(delta, diff)

        utility_old = [row[:] for row in utility_new]
        utility_history.append([row[:] for row in utility_old])
        iteration += 1

        if delta < THRESHOLD:
            print(f"Policy evaluation converged after {iteration} iterations.")
            break

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
visualise_rewards(rewards, start_position=(0, 0))
visualise_utility(utility_old, rewards_grid=rewards, start_position=(0, 0))
visualise_utility_with_arrows(utility_old, rewards_grid=rewards, start_position=(0, 0))
visualise_utility_estimates(utility_history, tracked_states)
