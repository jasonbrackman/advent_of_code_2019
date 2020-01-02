from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional, Any
from collections import deque


class Donut:
    def __init__(self, instructions):
        self.maze: List[List[str]] = [list(i) for i in instructions]
        self.rows = len(self.maze)
        self.cols = len(self.maze[0])
        self.portals = dict()

        self.populate_portals()

    def display(self):
        for row in range(self.rows):
            for col in range(self.cols):
                print(self.maze[row][col], end="")
            print()

    def get_portal_neighbors(self, row1, col1):
        neighbors = []

        for (row2, col2) in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            row: int = row1 + row2
            col: int = col1 + col2

            if 0 <= row < self.rows and 0 <= col < self.cols:
                t: str = self.maze[row][col]
                if t == ".":
                    neighbors.append((t, row, col))
                elif t.isalpha() and t.isupper():
                    neighbors.append((t, row, col))

        return neighbors

    def populate_portals(self):
        portals_new: Dict[Tuple, List[Tuple[int, int]]] = {}

        for row in range(self.rows):
            for col in range(self.cols):
                possible_portal = self.maze[row][col]
                key = None
                dot = []
                if possible_portal.isalpha() and possible_portal.isupper():
                    neighbors = self.get_portal_neighbors(row, col)
                    if neighbors:
                        for neighbor_ in neighbors:
                            neighbor, r, c = neighbor_
                            if neighbor == ".":
                                dot.append((r, c))
                            else:
                                key = tuple(sorted([possible_portal, neighbor]))

                    if key not in portals_new:
                        portals_new[key] = dot
                    else:
                        portals_new[key].extend(dot)

        self.portals = portals_new

    def goal(self, pos):
        return pos in self.portals[("Z", "Z")]

    def neighbors(self, pos):
        neighbors = []
        row1, col1 = pos
        for (row2, col2) in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            row: int = row1 + row2
            col: int = col1 + col2
            if 0 <= row < self.rows and 0 <= col <= self.cols:
                icon = self.maze[row][col]

                if icon == ".":
                    neighbors.append((row, col))
                elif icon.isalpha():
                    for v in self.portals.values():
                        if (row1, col1) in v:
                            for a in v:
                                if a != (row1, col1):
                                    neighbors.append(a)
                                    # print("JUMP=>", a)
                    neighbors.append((row, col))

        return neighbors

    def get_starting_position(self):
        return self.portals[("A", "A")][0]


def prep_data(path):
    with open(path) as f:
        lines = f.readlines()

    longest_line = max(len(line) for line in lines)
    return [list(line + " " * (longest_line - len(line))) for line in lines]


@dataclass
class Node:
    state: Any
    parent: Optional[Node]
    steps: int


def bfs(donut, current_position):
    frontier = deque([Node(current_position, None, 0)])
    visited = set(current_position)

    while frontier:
        node = frontier.popleft()
        pos = node.state

        if donut.goal(pos) is True:
            return node

        for neighbor in donut.neighbors(pos):
            if neighbor not in visited:
                visited.add(neighbor)
                inc = 0 if donut.maze[neighbor[0]][neighbor[1]].isalpha() else 1
                frontier.append(Node(neighbor, node, node.steps + inc))


def get_steps(instructions):
    d = Donut(instructions)
    current_position = d.get_starting_position()
    r = bfs(d, current_position)
    return r.steps


def trace_back(node):
    while node:
        print(node.state)
        node = node.parent


def test():
    t1 = prep_data(r"./data/day_20_test1.txt")
    results = get_steps(t1)
    assert results == 23
    t2 = prep_data(r"./data/day_20_test2.txt")
    results = get_steps(t2)
    assert results == 58


def run():
    instructions = prep_data(r"./data/day_20.txt")
    results = get_steps(instructions)
    assert results == 410


if __name__ == "__main__":
    test()
    run()
