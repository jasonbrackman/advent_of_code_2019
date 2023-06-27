import copy
from collections import defaultdict
from typing import List, Dict, Tuple

# types
Grid = List[str]
Pos = Tuple[int, int]

# Constants
GRID_SIZE = 5
CENTER = (2, 2)


def _update_icon(pos: Pos, level: int, levels: Dict[int, Grid]) -> str:
    # if at edge, then explore to a HIGHER level and the lower is CENTER
    # if at CENTER, then explore to a LOWER level.

    # Rules
    #   A bug (#) dies (becoming an empty space) unless there is exactly one bug adjacent to it.
    #   An empty (.) space becomes infested with a bug if exactly one or two bugs are adjacent to it.
    #   Otherwise, a bug or empty space remains the same.

    # Therefore:
    # MOVING OUTWARD
    #   If no level HIGHER exists, but a current edge contains 1 or 2 bugs create a higher level with that
    #     side (adjacent to CENTER) contains a bug now.
    #   If a level HIGHER exists, then collect the outer edges bug count and use those counts depending on
    #     how the HIGHER level neighbours to CENTER is adjacent.
    #
    inner_data: Dict[Pos, int] = defaultdict(int)
    outer_data: Dict[Pos, int] = defaultdict(int)

    if level - 1 in levels:
        # Peek into LOWER level
        # MOVING INWARD
        #   if no level LOWER exists, count it as a '.' to the CURRENT level
        #   if a level LOWER exists, count all bugs for the adjacent edge.

        # collect info for each internal side
        inner_grid = levels[level - 1]
        # Store INVERSE: Top, down, left, right
        inner_data[(-1, 0)] = inner_grid[0].count("#")
        inner_data[(1, 0)] = inner_grid[GRID_SIZE - 1].count("#")
        inner_data[(0, -1)] = sum([line[0] == "#" for line in inner_grid])
        inner_data[(0, 1)] = sum([line[GRID_SIZE - 1] == "#" for line in inner_grid])

    if level + 1 in levels:
        if pos[0] in (0, GRID_SIZE - 1) or pos[1] in (0, GRID_SIZE - 1):
            # Peek into a HIGHER level
            outer_grid = levels[level + 1]
            # Top, down, left, right
            #         1,2
            #   2,1 | 2,2 | 2,3
            #         3,2
            outer_data[(1, 0)] = int(outer_grid[1][2] == "#")
            outer_data[(-1, 0)] = int(outer_grid[3][2] == "#")
            outer_data[(0, 1)] = int(outer_grid[2][1] == "#")
            outer_data[(0, -1)] = int(outer_grid[2][3] == "#")

    # - - - - - - - - - -
    state = levels[level]
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    bug_count = 0
    for (row, col) in dirs:
        new_row = pos[0] + row
        new_col = pos[1] + col
        # If the new pos is Center, we need to know where we came from to know the
        #  side of the inner grid to collect bugs
        if (new_row, new_col) == CENTER:
            bug_count += inner_data[(row, col)]

        elif 0 <= new_row < GRID_SIZE and 0 <= new_col < GRID_SIZE:
            bug_count += state[new_row][new_col] == "#"
        else:
            # must be at edge / but what edge.
            bug_count += outer_data[(row, col)]

    # Rules
    # A bug (#) dies (becoming an empty space) unless there is exactly one bug adjacent to it.
    # An empty (.) space becomes infested with a bug if exactly one or two bugs are adjacent to it.
    # Otherwise, a bug or empty space remains the same.
    original = state[pos[0]][pos[1]]

    if original == "#":
        return "." if bug_count != 1 else original

    if original == ".":
        return "#" if bug_count in (1, 2) else original

    return original


def spin(levels: Dict[int, List[str]]) -> int:
    for _ in range(200):
        # should new state create an inward level if missing?
        min_level = min(levels.keys())
        max_level = max(levels.keys())
        levels[min_level - 1] = ["....."] * 5
        levels[max_level + 1] = ["....."] * 5
        new_state: Dict[int, List[str]] = {}
        for level, _ in levels.items():
            new_state[level] = []
            for row in range(GRID_SIZE):
                line = ""
                for col in range(GRID_SIZE):
                    if (row, col) == CENTER:
                        line += "?"
                    else:
                        line += _update_icon((row, col), level, levels)
                new_state[level].append(line)

        levels = copy.deepcopy(new_state)

    return calc_bug_count(levels)


def calc_bug_count(levels):
    bug_count = 0
    for level, grid in levels.items():
        bug_count += sum([g.count("#") for g in grid])
    return bug_count


def run() -> None:
    start = [
        "#.#..",
        ".....",
        ".#.#.",
        ".##..",
        ".##.#",
    ]
    levels: Dict[int, Grid] = {
        0: start,
    }
    r = spin(levels)
    assert r == 2017


if __name__ == "__main__":
    run()
