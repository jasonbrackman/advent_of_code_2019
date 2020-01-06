from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional, Any
from collections import deque, namedtuple

Cell = namedtuple("Cell", "row, col, level, last_portal")


class Donut:
    def __init__(self, instructions, part2=False):
        self.maze: List[List[str]] = [list(i) for i in instructions]
        self.rows = len(self.maze)
        self.cols = len(self.maze[0])
        self.portals = dict()

        self.populate_portals()

        self.part2 = part2

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

    def neighbors_cell(self, cell):

        neighbors = []
        for (row2, col2) in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            row: int = cell.row + row2
            col: int = cell.col + col2
            if 0 <= row < self.rows and 0 <= col <= self.cols:
                icon = self.maze[row][col]

                if icon == ".":
                    neighbors.append(
                        Cell(
                            row=row,
                            col=col,
                            level=cell.level,
                            last_portal=cell.last_portal,
                        )
                    )

                elif icon.isalpha():
                    # we should not add a neighbor if level = 0 and we are jumping from an outer portal
                    for k, v in self.portals.items():
                        if (cell.row, cell.col) in v:
                            for a in v:
                                if a != (cell.row, cell.col):
                                    jump = (
                                        1
                                        if a[0] in (2, self.rows - 3)
                                        or a[1] in (2, self.cols - 4)
                                        else -1
                                    )

                                    c = Cell(
                                        row=a[0],
                                        col=a[1],
                                        level=cell.level + jump,
                                        last_portal=k,
                                    )

                                    if c.level >= 0:
                                        neighbors.append(c)

                    neighbors.append(
                        Cell(
                            row=row,
                            col=col,
                            level=cell.level,
                            last_portal=cell.last_portal,
                        )
                    )

        return neighbors

    def is_entry_or_exit(self, cell):
        row, col = cell[0], cell[1]
        for k, v in self.portals.items():
            if (row, col) in v:
                if k == ("Z", "Z") or k == ("A", "A"):
                    return True
        return False

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
                                if a != (row1, col1) or a[0] != row1 or a[1] != col1:
                                    neighbors.append((a[0], a[1]))
                    neighbors.append((row, col))

        return neighbors

    def get_starting_position(self):
        return self.portals[("A", "A")][0]

    def is_outer(self, pos):
        r1, c1 = pos[0], pos[1]
        if 0 <= r1 <= 2 or self.rows - 4 <= r1 < self.rows:
            return True
        if 0 <= c1 <= 2 or self.cols - 4 <= c1 < self.cols:
            return True

        return False


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


def bfs2(donut, pos):
    c = Cell(row=pos[0], col=pos[1], level=0, last_portal="")
    frontier = deque([Node(c, None, 0)])
    visited = set(c)

    while frontier:
        node = frontier.popleft()
        state = node.state
        if state.level == 0 and donut.goal((state.row, state.col)) is True:
            return node

        for cell in donut.neighbors_cell(state):
            if cell.level >= 0 and cell not in visited:
                visited.add(cell)
                inc = 0 if donut.maze[cell.row][cell.col].isalpha() else 1
                frontier.append(Node(cell, node, node.steps + inc))


def get_steps(instructions, part2=False):
    d = Donut(instructions, part2=part2)
    p = d.get_starting_position()
    r = bfs2(d, p) if part2 is True else bfs(d, p)

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

    t3 = prep_data(r"./data/day_20_test3.txt")
    results = get_steps(t3, part2=True)
    assert results == 396


def run():
    instructions = prep_data(r"./data/day_20.txt")

    results = get_steps(instructions)
    assert results == 410

    # part02
    results = get_steps(instructions, part2=True)
    assert results == 5084


if __name__ == "__main__":
    test()
    run()
