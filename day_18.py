from __future__ import annotations
import helpers
from collections import deque, namedtuple
from typing import NamedTuple, Optional, List, TypeVar, Callable, Tuple
from dataclasses import dataclass


class Pos(NamedTuple):
    row: int
    col: int


class Maze:
    @classmethod
    def load_object_data(cls, instructions, part2=False):
        cls.maze: List[List[str]] = [list(line) for line in instructions]
        cls.rows = len(cls.maze)
        cls.cols = len(cls.maze[0])
        cls.keys = dict()

        for r in range(cls.rows):
            for c in range(cls.cols):
                icon = cls.maze[r][c]
                if icon.isalpha() and icon.islower():
                    cls.keys[icon] = Pos(r, c)
                elif icon == "@":
                    cls.current_pos = Pos(r, c)

        if part2 is True:
            # reshape data
            new = list("@#@###@#@")
            pos = cls.current_pos
            rows = [pos.row - 1, pos.row, pos.row + 1]
            cols = [pos.col - 1, pos.col, pos.col + 1]
            index = 0
            for r in rows:
                for c in cols:
                    icon = new[index]
                    cls.maze[r][c] = icon
                    index += 1

        return cls()

    def get_start_positions(self):
        positions = []
        for row in range(self.rows):
            for col in range(self.cols):
                icon = self.maze[row][col]
                if icon == "@":
                    positions.append(Pos(row, col))
        return positions

    def display(self, path=None):
        # Header:
        print(" ", end="  ")
        [print(f"{index:02}", end=" ") for index in range(self.cols)]
        print()

        for row in range(self.rows):
            print(f"{row:02}", end="  ")
            for col in range(self.cols):
                icon = "X" if path and Pos(row, col) in path else self.maze[row][col]
                icon = " " if icon == "." else icon
                print(icon, end="")
            print()

    def goal(self, keys):
        return len(keys) == len(self.keys)

    def successors(self, state: SearchState) -> Optional[List[Pos]]:
        neighbors = []
        for (r, c) in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
            row = state.pos.row + r
            col = state.pos.col + c
            if 0 <= row < self.rows and 0 <= col < self.cols:
                icon = self.maze[row][col]
                if icon == "#" or (
                    icon.isalpha() and icon.isupper() and icon.lower() not in state.keys
                ):
                    continue
                neighbors.append(Pos(row, col))

        return neighbors


T = TypeVar("T")


@dataclass
class Node:
    state: T
    parent: Optional[Node]
    steps: int


SearchState = namedtuple("SearchState", "pos, keys")


def bfs(maze, start_state, goal: Callable):
    frontier = deque([Node(SearchState(start_state, tuple()), None, 0)])
    visited = set()

    while frontier:
        node = frontier.popleft()
        state = node.state

        if goal(state.keys) is True:
            # print("Result:", node.steps, node.state.keys)
            return node

        for s in maze.successors(state):
            new_key = {k for k, v in maze.keys.items() if v == s}
            new_state = SearchState(s, tuple(set(state.keys) | new_key))
            if new_state not in visited:
                visited.add(new_state)
                frontier.append(Node(new_state, node, node.steps + 1))


def display_if_path(m, s):
    if s is None:
        print("Failed")
    else:
        path = []
        parent = s
        while parent:
            path.append(parent.state.pos)
            parent = parent.parent
        m.display(path=path)


def tests():
    t1 = """#########\n#b.A.@.a#\n#########""".split("\n")
    t2 = """########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################""".split(
        "\n"
    )
    t3 = """########################
#...............b.C.D.f#
#.######################
#.....@.a.B.c.d.A.e.F.g#
########################""".split(
        "\n"
    )
    t5 = """#################
#i.G..c...e..H.p#
########.########
#j.A..b...f..D.o#
########@########
#k.E..a...g..B.n#
########.########
#l.F..d...h..C.m#
#################""".split(
        "\n"
    )
    t4 = """########################
#@..............ac.GI.b#
###d#e#f################
###A#B#C################
###g#h#i################
########################""".split(
        "\n"
    )

    m = Maze.load_object_data(t1)
    r = bfs(m, m.current_pos, goal=m.goal)
    assert r.steps == 8

    m = Maze.load_object_data(t2)
    r = bfs(m, m.current_pos, goal=m.goal)
    assert r.steps == 86

    m = Maze.load_object_data(t4)
    r = bfs(m, m.current_pos, goal=m.goal)
    assert r.steps == 81

    m = Maze.load_object_data(t5)
    r = bfs(m, m.current_pos, goal=m.goal)
    assert r.steps == 136

    m = Maze.load_object_data(t3)
    r = bfs(m, m.current_pos, goal=m.goal)
    assert r.steps == 132
    print("Tests complete.")


def run():
    # part01
    instructions = helpers.get_lines(r"./data/day_18.txt")
    m = Maze.load_object_data(instructions)
    r = bfs(m, m.current_pos, goal=m.goal)
    assert r.steps == 5402


def tests2():
    t1 = """#######
#a.#Cd#
##...##
##.@.##
##...##
#cB#Ab#
#######""".split(
        "\n"
    )

    def goal(t: Tuple[str]):
        def g(keys):
            for key in keys:
                if key not in t:
                    return True
            return False

        return g

    k = set()
    m = Maze.load_object_data(t1, part2=True)
    print(m.display())
    g = goal(tuple(k))
    total = 0

    counter = 0
    positions = m.get_start_positions()
    while positions:
        pos = positions[counter % len(positions)]
        r = bfs(m, pos, goal=g)
        if r is not None:
            total += r.steps
            for item in r.state.keys:
                k.add(item)
            g = goal(tuple(k))
            print(r.state.pos, k)
            # positions[counter % len(positions)] = r.state.pos
        counter += 1

    print("Total:", total)


if __name__ == "__main__":
    # tests()
    # run()
    tests2()

    # instructions = helpers.get_lines(r"./data/day_18.txt")
    # m = Maze.load_object_data(instructions, part2=True)
    # m.display()
    # print(m.current_pos)

    # m = Maze(instructions, part2=True)
