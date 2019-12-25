from day_09 import IntCodeMachine, parse_instructions
from collections import deque
from itertools import combinations, permutations
from typing import Set, Tuple, List


class Node:
    def __init__(self, state, parent):
        self.state = state
        self.parent = parent


class Ascii:
    dirs = {
        "^": [(0, -1), (0, 1)],
        ">": [(-1, 0), (1, 0)],
        "v": [(0, -1), (0, 1)],
        "<": [(-1, 0), (1, 0)],
    }

    def __init__(self, instructions, override=1):
        self.grid = []
        self.current_pos = {(-1, -1): "?"}
        self.scaffolding: Set[Tuple[int, int]] = set()
        self.crossovers: Set[Tuple[int, int]] = set()
        self.space_dust = 0

        self.m = IntCodeMachine(instructions, override, silent=True)

    def extract_grid(self):
        line = ""
        while True:
            results = self.m.op_codes()
            if results is None:
                break
            op, code = results
            code = int(code)
            if code == 10:
                if len(line) > 1:
                    self.grid.append(list(line))
                line = ""
            else:
                line += chr(code)

    def identify_crossovers(self):
        total = 0
        for r in range(len(self.grid)):
            for c in range(len(self.grid[0])):
                if 0 <= r < len(self.grid) - 1 and 0 <= c < len(self.grid[0]) - 1:
                    if (
                        self.grid[r][c]
                        == self.grid[r - 1][c]
                        == self.grid[r + 1][c]
                        == self.grid[r][c - 1]
                        == self.grid[r][c + 1]
                        == "#"
                    ):
                        self.crossovers.add((r, c))
                        total += r * c

        return total

    def set_current_pos(self):
        for r in range(len(self.grid)):
            for c in range(len(self.grid[0])):

                if self.grid[r][c] == "#":
                    self.scaffolding.add((r, c))
                elif self.grid[r][c] in self.dirs.keys():
                    self.current_pos = {(r, c): self.grid[r][c]}
                    self.grid[r][c] = "#"

    def goal(self, visited: List[str], node: Node) -> List:
        if len(self.scaffolding) == len(visited):
            items = format_search_results(node)
            return is_pattern(items)
        return []

    @staticmethod
    def add_positions(pos1, pos2):
        return pos1[0] + pos2[0], pos1[1] + pos2[1]

    @staticmethod
    def sub_positions(pos1, pos2):
        return abs(pos1[0] - pos2[0] + pos1[1] - pos2[1])

    def successors(self, position):

        k, v = [(k, v) for k, v in position.items()][0]
        dirs = list(self.dirs.keys())
        index = dirs.index(v)

        succs = []
        directions = {
            "^": ["<", ">"],
            "v": ["<", ">"],
            ">": ["^", "v"],
            "<": ["^", "v"],
        }

        for (x, y), direction in zip(self.dirs[v], directions[dirs[index]]):
            moves = []
            xn, yn = self.add_positions(k, (x, y))
            while True:

                if 0 <= xn < len(self.grid) and 0 <= yn < len(self.grid[0]):
                    if self.grid[xn][yn] == "#":
                        moves.append((xn, yn))
                        xn, yn = self.add_positions((xn, yn), (x, y))
                    else:
                        break
                else:
                    break

            if moves:
                succs.append({direction: moves})
        return succs

    def display(self, visited=None):
        for r in range(len(self.grid)):
            for c in range(len(self.grid[0])):
                icon = (
                    self.grid[r][c]
                    if self.current_pos.get((r, c), None) is None
                    else self.current_pos[(r, c)]
                )
                icon = "X" if visited is not None and (r, c) in visited else icon
                print(icon, end="")
            print()


def do_search(machine):
    frontier = deque([Node(machine.current_pos, None)])
    cached = {str(machine.current_pos)}
    visited = set()
    while frontier:
        node = frontier.pop()
        if winners := machine.goal(visited, node):
            return node, winners

        for child in machine.successors(node.state):
            if str(child) not in cached:
                cached.add(str(child))
                for k, v in child.items():
                    if v:
                        for item in v:
                            visited.add(item)
                        new = {v[-1]: k}
                        frontier.append(Node(new, node))


def format_search_results(node):
    # need to convert this now into movement instructions
    final_list = []
    while node.parent:
        final_list.append(node.state)
        node = node.parent
    final_list.append(node.state)
    final_list = list(reversed(final_list))
    dirs = list(Ascii.dirs.keys())
    items = []
    for (a, b) in zip(final_list, final_list[1:]):
        k1, v1 = [(k, v) for k, v in a.items()][0]
        k2, v2 = [(k, v) for k, v in b.items()][0]

        icon = "R" if dirs[(dirs.index(v1) + 1) % len(dirs)] == v2 else "L"
        distance = Ascii.sub_positions(k1, k2)
        items.append(f"{icon},{distance}")
    return items


def is_pattern(items: List[str]) -> List:
    patterns = {
        2: zip(items, items[1:]),
        3: zip(items, items[1:], items[2:]),
        4: zip(items, items[1:], items[2:], items[3:]),
        5: zip(items, items[1:], items[2:], items[3:], items[4:]),
    }

    results = set()
    for k, v in patterns.items():
        repeats = [r for r in v]
        if len(repeats) != len(set(repeats)):
            for i in set(repeats):
                if repeats.count(i) > 1:
                    results.add(i)

    return three_combos_used(items, results)


def three_combos_used(directions, patterns, r_length=3) -> List:
    winners = []

    full_string = "".join(directions)

    combos = combinations(patterns, r_length)

    for combo in combos:

        perms = permutations(combo)
        for perm in perms:
            new_string = str(full_string)
            for f in perm:
                par_string = "".join(f)
                if par_string in new_string:
                    new_string = new_string.replace(par_string, " ")
            if new_string.strip() == "":
                main = (
                    str(full_string)
                    .replace("".join(combo[0]), "A")
                    .replace("".join(combo[1]), "B")
                    .replace("".join(combo[2]), "C")
                )
                function_a = combo[0]
                function_b = combo[1]
                function_c = combo[2]

                winners.append(
                    [
                        ",".join(list(main)),
                        ",".join(function_a),
                        ",".join(function_b),
                        ",".join(function_c),
                    ]
                )

    return winners


def run():
    instructions = parse_instructions(r"./data/day_17.txt")

    # Part 01
    ascii = Ascii(instructions)
    ascii.extract_grid()
    ascii.set_current_pos()
    part01 = ascii.identify_crossovers()
    assert part01 == 4408

    # Gather info for part2
    results = do_search(ascii)

    program_routines = [] if results is None else results[1][0]
    program_routines.append("n")

    # Part 2 needs to run the program in a specific way
    ascii = Ascii(instructions, 2)
    for routine in program_routines:
        for c in list(routine):
            ascii.m.input(ord(c))
        ascii.m.input(ord("\n"))

    while True:
        results = ascii.m.op_codes()
        if results is None:
            part02 = ascii.m.buffer
            break
    assert part02 == 862452


if __name__ == "__main__":
    run()
