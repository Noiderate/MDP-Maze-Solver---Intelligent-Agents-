import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/..')

from visualize import visualise_utility
from visualize import visualise_utility_with_arrows
from visualize import visualise_utility_estimates
from visualize import visualise_rewards
from grid_utils import is_wall
from grid_utils import check_directions
from utility_utils import get_highest_expected_utility
from big_array import get_big_rewards_grid
from big_array import get_random_big_rewards_grid

DISCOUNT_FACTOR = 0.99
DEBUG_MODE = False
THRESHOLD = 0.001
MAX_ITERATIONS = 10000

#rewards = get_big_rewards_grid()
rewards = get_random_big_rewards_grid(rows=100, cols=100)

utility_old = [[0 for _ in row] for row in rewards]
utility_new = [[0 for _ in row] for row in rewards]

utility_history = [[row[:] for row in utility_old]]

for iteration in range(MAX_ITERATIONS):
    utility_new = [[0 for _ in row] for row in rewards]
    delta = 0

    for x in range(len(rewards)):
        for y in range(len(rewards[x])):
            if is_wall(rewards, x, y):
                continue

            possible_directions = check_directions(rewards, x, y)
            highest_utility_from_directions = get_highest_expected_utility(
                utility_old, possible_directions, x, y, debug=DEBUG_MODE
            )

            utility_new[x][y] = rewards[x][y] + DISCOUNT_FACTOR * highest_utility_from_directions

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
visualise_rewards(rewards, start_position=(0, 0))
visualise_utility(utility_old, rewards_grid=rewards, start_position=(0, 0))
visualise_utility_with_arrows(utility_old, rewards_grid=rewards, start_position=(0, 0))
visualise_utility_estimates(utility_history, tracked_states)
