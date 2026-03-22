import random


def get_big_rewards_grid():
    return [
        [-0.05, -0.05, "wall", -0.05, -0.05, -0.05, "wall", -0.05,     1, -0.05],
        ["wall",    -0.05, "wall", -0.05, "wall", -1, "wall", -0.05, "wall", -0.05],
        [-0.05, -0.05, -1, -0.05, "wall", -1, -1, -0.05, "wall", -0.05],
        [-0.05, "wall", -1, -1, "wall", "wall", "wall", -0.05, "wall", -1],
        [-0.05, -0.05, -0.05, -0.05, -0.05, -0.05, "wall", -0.05, -0.05, -0.05],
        ["wall", "wall", "wall", "wall", "wall", -0.05, "wall", "wall", "wall", -0.05],
        [-0.05, -0.05, -0.05, -0.05, "wall", -0.05, -0.05, -0.05, "wall", -0.05],
        [-0.05, "wall", "wall", -0.05, "wall", "wall", "wall", -0.05, "wall",    -0.05],
        [-0.05, -0.05, "wall", -0.05, -0.05, -0.05, "wall", -0.05, -0.05, -0.05],
        [    1, -0.05, "wall", "wall", "wall", -0.05, -0.05, -0.05, "wall",     1],
    ]


def get_random_big_rewards_grid(rows=30, cols=30, choices=None, weights=None, seed=None):
    if choices is None:
        choices = [1, -0.05, -1, "wall"]
    if weights is None:
        weights = [1, 8, 1, 4]

    rng = random.Random(seed)
    return [rng.choices(choices, weights=weights, k=cols) for _ in range(rows)]


# rewards = get_big_rewards_grid()
rewards = get_random_big_rewards_grid()


