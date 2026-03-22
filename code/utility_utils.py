def get_expected_utility_for_direction(
    utility_old, possible_directions, x, y, direction, debug=False
):
    direction = direction.lower()
    valid_directions = {"up", "down", "left", "right"}

    if direction not in valid_directions:
        raise ValueError(
            f"Invalid direction '{direction}'. Expected one of {sorted(valid_directions)}"
        )

    def utility_after_move(move_direction):
        if move_direction in possible_directions:
            if move_direction == "up":
                return utility_old[x - 1][y]
            if move_direction == "down":
                return utility_old[x + 1][y]
            if move_direction == "left":
                return utility_old[x][y - 1]
            return utility_old[x][y + 1]
        return utility_old[x][y]

    if direction == "up":
        expected_utility = (
            0.8 * utility_after_move("up")
            + 0.1 * utility_after_move("left")
            + 0.1 * utility_after_move("right")
        )
    elif direction == "down":
        expected_utility = (
            0.8 * utility_after_move("down")
            + 0.1 * utility_after_move("left")
            + 0.1 * utility_after_move("right")
        )
    elif direction == "left":
        expected_utility = (
            0.8 * utility_after_move("left")
            + 0.1 * utility_after_move("up")
            + 0.1 * utility_after_move("down")
        )
    else:
        expected_utility = (
            0.8 * utility_after_move("right")
            + 0.1 * utility_after_move("up")
            + 0.1 * utility_after_move("down")
        )

    if debug:
        print(
            f"[DEBUG] cell=({x}, {y}) direction={direction} "
            f"expected={expected_utility:.4f}"
        )

    return expected_utility


def get_highest_expected_utility(utility_old, possible_directions, x, y, debug=False):
    expected_by_direction = {
        direction: get_expected_utility_for_direction(
            utility_old, possible_directions, x, y, direction
        )
        for direction in ["up", "down", "left", "right"]
    }

    best_expected_utility = max(expected_by_direction.values())

    if debug:
        print(
            f"[DEBUG] cell=({x}, {y}) dirs={possible_directions} "
            f"expected={expected_by_direction} best={best_expected_utility:.4f}"
        )

    return best_expected_utility