def is_wall(rewards, x, y):
    if x < 0 or x >= len(rewards):
        return True
    if y < 0 or y >= len(rewards[x]):
        return True
    return rewards[x][y] == "wall"


def check_directions(rewards, x, y):
    if is_wall(rewards, x, y):
        return []

    possible_directions = []

    if not is_wall(rewards, x - 1, y):
        possible_directions.append("up")
    if not is_wall(rewards, x + 1, y):
        possible_directions.append("down")
    if not is_wall(rewards, x, y - 1):
        possible_directions.append("left")
    if not is_wall(rewards, x, y + 1):
        possible_directions.append("right")

    return possible_directions