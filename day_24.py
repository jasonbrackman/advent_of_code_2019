from typing import List, Set, Tuple, Dict

GRID_SIZE = 5


def _powers_of_two() -> Dict[Tuple[int, int], int]:
    results = dict()

    current = 1
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            results[(row, col)] = current
            current *= 2

    return results


def _update_icon(pos: Tuple[int, int], state: List[str]) -> str:
    bug_count = 0

    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for (row, col) in dirs:
        new_row = pos[0] + row
        new_col = pos[1] + col

        if 0 <= new_row < GRID_SIZE and 0 <= new_col < GRID_SIZE:
            bug_count += state[new_row][new_col] == '#'
    # Rules
    # A bug (#) dies (becoming an empty space) unless there is exactly one bug adjacent to it.
    # An empty (.) space becomes infested with a bug if exactly one or two bugs are adjacent to it.
    # Otherwise, a bug or empty space remains the same.

    original = state[pos[0]][pos[1]]

    if original == "#" and bug_count != 1:
        return '.'

    elif original == "." and bug_count in (1, 2):
        return '#'

    return original


def spin(state: List[str]) -> int:
    seen: Set[str] = set()
    while True:
        new_state: List[str] = []
        for row in range(GRID_SIZE):
            line = ""
            for col in range(GRID_SIZE):
                line += _update_icon((row, col), state)
            new_state.append(line)

        if str(new_state) in seen:
            # Reached the Winner! Calculate rating and return
            rating = biodiversity_rating(new_state)
            return rating

        seen.add(str(new_state))
        state = new_state


def biodiversity_rating(state: List[str]) -> int:
    """calculate the biodiversity rating"""
    powers_of_two = _powers_of_two()
    total = 0
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if state[row][col] == "#":
                total += powers_of_two[(row, col)]

    return total


def run() -> None:
    puzzle = [
        "#.#..",
        ".....",
        ".#.#.",
        ".##..",
        ".##.#",
    ]

    # Test puzzle
    # puzzle = [
    # "....#",
    # "#..#.",
    # "#..##",
    # "..#..",
    # "#....",
    # ]

    part01 = spin(puzzle)
    assert part01 == 32776479


if __name__ == "__main__":
    run()
