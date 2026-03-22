import matplotlib.pyplot as plt
import matplotlib.patches as patches


def _is_wall_cell(rewards_grid, row, col):
    return rewards_grid is not None and rewards_grid[row][col] == "wall"


def _best_neighbor_direction(grid, row, col, rewards_grid=None):
    rows = len(grid)
    cols = len(grid[0])

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    best_direction = None
    best_value = None

    for delta_row, delta_col in directions:
        next_row = row + delta_row
        next_col = col + delta_col

        if next_row < 0 or next_row >= rows or next_col < 0 or next_col >= cols:
            continue
        if _is_wall_cell(rewards_grid, next_row, next_col):
            continue

        next_value = grid[next_row][next_col]
        if best_value is None or next_value > best_value:
            best_value = next_value
            best_direction = (delta_row, delta_col)

    return best_direction


def visualise_rewards(grid, start_position=(3, 2)):
    rows = len(grid)
    cols = len(grid[0])

    fig, ax = plt.subplots(figsize=(cols * 1.2, rows * 1.2))
    ax.set_xlim(0, cols)
    ax.set_ylim(0, rows)
    ax.set_aspect("equal")
    ax.axis("off")

    for r in range(rows):
        for c in range(cols):
            value = grid[r][c]

            if value == "wall":
                color = "grey"
            elif value == 1:
                color = "green"
            elif value == -1:
                color = "orange"
            else:
                color = "white"

            rect = patches.Rectangle((c, rows - 1 - r), 1, 1,
                                      linewidth=1, edgecolor="black", facecolor=color)
            ax.add_patch(rect)

            if (r, c) == start_position:
                label = "Start"
            elif value == "wall":
                label = "Wall"
            else:
                label = str(value)

            ax.text(c + 0.5, rows - 1 - r + 0.5, label,
                    ha="center", va="center", fontsize=10, fontweight="bold")

    plt.tight_layout()
    plt.show()


def visualise_utility(grid, rewards_grid=None, start_position=(3, 2)):
    rows = len(grid)
    cols = len(grid[0])

    values = [value for row in grid for value in row]
    min_value = min(values)
    max_value = max(values)

    fig, ax = plt.subplots(figsize=(cols * 1.2, rows * 1.2))
    ax.set_xlim(0, cols)
    ax.set_ylim(0, rows)
    ax.set_aspect("equal")
    ax.axis("off")

    for r in range(rows):
        for c in range(cols):
            value = grid[r][c]

            is_wall_cell = rewards_grid is not None and rewards_grid[r][c] == "wall"

            if is_wall_cell:
                color = "grey"
            else:
                if max_value == min_value:
                    normalized_value = 0.5
                else:
                    normalized_value = (value - min_value) / (max_value - min_value)

                color = plt.cm.Blues(normalized_value)

            rect = patches.Rectangle(
                (c, rows - 1 - r),
                1,
                1,
                linewidth=1,
                edgecolor="black",
                facecolor=color,
            )
            ax.add_patch(rect)

            if is_wall_cell:
                label = "Wall"
            elif (r, c) == start_position:
                label = f"Start\n{value:.3f}"
            else:
                label = f"{value:.3f}"

            ax.text(
                c + 0.5,
                rows - 1 - r + 0.5,
                label,
                ha="center",
                va="center",
                fontsize=10,
                fontweight="bold",
            )

    ax.set_title("Utility Table")
    plt.tight_layout()
    plt.show()


def visualise_utility_with_arrows(grid, rewards_grid=None, start_position=(3, 2)):
    rows = len(grid)
    cols = len(grid[0])

    values = [value for row in grid for value in row]
    min_value = min(values)
    max_value = max(values)

    fig, ax = plt.subplots(figsize=(cols * 1.2, rows * 1.2))
    ax.set_xlim(0, cols)
    ax.set_ylim(0, rows)
    ax.set_aspect("equal")
    ax.axis("off")

    for r in range(rows):
        for c in range(cols):
            value = grid[r][c]
            is_wall = _is_wall_cell(rewards_grid, r, c)

            if is_wall:
                color = "grey"
            else:
                if max_value == min_value:
                    normalized_value = 0.5
                else:
                    normalized_value = (value - min_value) / (max_value - min_value)

                color = plt.cm.Blues(normalized_value)

            rect = patches.Rectangle(
                (c, rows - 1 - r),
                1,
                1,
                linewidth=1,
                edgecolor="black",
                facecolor=color,
            )
            ax.add_patch(rect)

            if is_wall:
                label = "Wall"
            elif (r, c) == start_position:
                label = f"Start\n{value:.3f}"
            else:
                label = ""

            ax.text(
                c + 0.5,
                rows - 1 - r + 0.5,
                label,
                ha="center",
                va="center",
                fontsize=9,
                fontweight="bold",
            )

            if not is_wall:
                best_direction = _best_neighbor_direction(
                    grid, r, c, rewards_grid=rewards_grid
                )
                if best_direction is not None:
                    delta_row, delta_col = best_direction
                    center_x = c + 0.5
                    center_y = rows - 1 - r + 0.5

                    arrow_dx = delta_col * 0.28
                    arrow_dy = -delta_row * 0.28

                    ax.arrow(
                        center_x - arrow_dx * 0.4,
                        center_y - arrow_dy * 0.4,
                        arrow_dx,
                        arrow_dy,
                        width=0.01,
                        head_width=0.12,
                        head_length=0.10,
                        length_includes_head=True,
                        color="black",
                        zorder=3,
                    )

    ax.set_title("Utility Table (Best Neighbor Arrows)")
    plt.tight_layout()
    plt.show()


def visualise_utility_estimates(utility_history, tracked_states):
    if not utility_history:
        raise ValueError("utility_history cannot be empty")
    if not tracked_states:
        raise ValueError("tracked_states cannot be empty")

    iterations = list(range(len(utility_history)))
    number_of_states = len(tracked_states)

    if number_of_states <= 20:
        color_map = plt.cm.get_cmap("tab20", number_of_states)
    else:
        color_map = plt.cm.get_cmap("nipy_spectral", number_of_states)

    fig, ax = plt.subplots(figsize=(7, 5))

    for index, (row, col) in enumerate(tracked_states):
        utility_trace = [grid[row][col] for grid in utility_history]
        label = f"({row + 1},{col + 1})"
        color = color_map(index)

        ax.plot(
            iterations,
            utility_trace,
            linestyle="-",
            linewidth=1.4,
            color=color,
            label=label,
        )

    ax.set_xlabel("Number of iterations")
    ax.set_ylabel("Utility estimates")
    ax.set_xlim(0, iterations[-1])
    ax.grid(axis="y", linestyle=":", alpha=0.35)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.legend(
        loc="center left",
        bbox_to_anchor=(1.02, 0.5),
        fontsize=7,
        frameon=False,
        ncol=1,
    )

    plt.tight_layout(rect=[0, 0, 0.78, 1])
    plt.show()
