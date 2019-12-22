from day_09 import IntCodeMachine, parse_instructions

from typing import Set, Tuple


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

    def goal(self, visited):
        return len(self.scaffolding) == len(visited)

    def add_positions(self, pos1, pos2):
        return pos1[0] + pos2[0], pos1[1] + pos2[1]

    def successors(self, position):

        k, v = [(k, v) for k, v in position.items()][0]
        dirs = list(self.dirs.keys())
        index = dirs.index(v)

        succs = []
        for (x, y), direction in zip(
            self.dirs[v], [dirs[(index - 1) % len(dirs)], dirs[(index + 1) % len(dirs)]]
        ):
            moves = []
            xn, yn = self.add_positions(k, (x, y))

            while True:

                if 0 <= xn < len(self.grid) and 0 <= yn < len(self.grid[0]):
                    if self.grid[xn][yn] == "#":
                        moves.append((xn, yn))
                        xn, yn = self.add_positions((xn, yn), (x, y))
                    else:
                        if moves:
                            # are any intersections available?
                            for index, cross in enumerate(moves):
                                # can be in three directions
                                if cross in self.crossovers:
                                    succs.append(
                                        {direction: moves[: index + 1]}
                                    )  # forward
                                    cross_dirs = (
                                        ["<", ">"]
                                        if direction in ["^", "v"]
                                        else ["^", "v"]
                                    )
                                    print(direction, cross_dirs)

                                    for d in cross_dirs:
                                        if direction == d:
                                            raise Exception("Expected opposites...")
                                        succs.append({d: moves[: index + 1]})  # left

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


def test():
    test01 = """#######...#####
                #.....#...#...#
                #.....#...#...#
                ......#...#...#
                ......#...###.#
                ......#.....#.#
                ^########...#.#
                ......#.#...#.#
                ......#########
                ........#...#..
                ....#########..
                ....#...#......
                ....#...#......
                ....#...#......
                ....#####......""".split(
        "\n"
    )
    test01 = [list(x.strip()) for x in test01]
    direction = ["^", ">", "v", "<"]

    def get_start_pos_and_scaffolding():
        needle_pos = -1, -1
        scaffolding = set()
        for r in range(len(test01)):
            for c in range(len(test01[0])):
                print(test01[r][c], end="")
                if test01[r][c] in direction:
                    needle_pos = r, c
                elif test01[r][c] == "#":
                    scaffolding.add((r, c))
            print()
        return needle_pos, scaffolding

    visited = set()
    current_pos, scaffolding = get_start_pos_and_scaffolding()
    assert current_pos != (
        -1,
        -1,
    ), f"Expected something other than -1, -1, but got {current_pos}"
    assert len(scaffolding) == 76

    def goal():
        return len(visited) == len(scaffolding)

    def successors(pos):
        # can only go left or right
        ...


class Node:
    def __init__(self, state, parent):
        self.state = state
        self.parent = parent


def run():
    instructions = parse_instructions(r"./data/day_17.txt")

    ascii = Ascii(instructions)
    ascii.extract_grid()
    ascii.set_current_pos()
    part01 = ascii.identify_crossovers()
    assert part01 == 4408

    ascii.display()

    # BFS
    frontier = [Node(ascii.current_pos, None)]  # expecting {pos: direction icon}
    cached = {str(ascii.current_pos)}
    visited = set()
    while frontier:
        node = frontier.pop()
        if ascii.goal(visited):
            print("visited everything")
            return node

        added_something_new = False
        for child in ascii.successors(node.state):
            if str(child) not in cached:
                cached.add(str(child))
                for k, v in child.items():
                    if v:
                        for item in v:
                            if item not in visited:
                                visited.add(item)
                        new = {v[-1]: k}
                        frontier.append(Node(new, node))

    ascii.display(visited)

    # ascii = Ascii(instructions, 2)
    # routines = ["A,B,C", "R,2,L,2", "R,2,L,2", "R,2,L,2", "y"]
    # for routine in routines:
    #     for c in list(routine):
    #         ascii.m.input(ord(c))
    #     ascii.m.input(ord("\n"))
    #
    # while True:
    #     results = ascii.m.op_codes()
    #     if results is None:
    #         print(ascii.m.buffer)
    #         break
    #     op, code = results
    #     print(chr(code), end="")

    """Accepts movement routine.  Includes the ascii letters ord(A), ord(B), or ord(C), followed by an ord(\\n)"""


if __name__ == "__main__":
    # test()
    r = run()
    # need to convert this now into movement instructions
    while r.parent:
        print(r.state)
        r = r.parent
    print(r.state)
