from __future__ import annotations

import sys
from collections import deque, namedtuple
import copy
from typing import List, Optional, TypeVar

from dataclasses import dataclass
import helpers

T = TypeVar("T")


@dataclass
class Node2:
    state: T
    parent: Optional[Node]

@dataclass
class Node:
    state: T
    parent: Optional[Node]
    steps: int

    def get_total(self):
        total = 0
        parent = self
        while parent:
            total += parent.steps
            parent = parent.parent
        return total


class Vault:
    def __init__(self, instructions):
        self.keys = dict()
        self.current_pos = tuple()
        self.map: List[List[str]] = [list(line) for line in instructions]

        self._init_object_data()

    def _init_object_data(self):
        row_length = len(self.map)
        col_length = len(self.map[0])
        for r in range(row_length):
            for c in range(col_length):
                icon = self.map[r][c]
                if icon.isalpha() and icon.islower():
                    self.keys[icon] = r, c
                elif icon == "@":
                    self.current_pos = r, c

    def goal(self, keys):
        return len(self.keys) == len(keys)

    def get_neighbors(self, state) -> List:
        neighbors = []
        r, c = state
        # check all four directions
        for (r1, c1) in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            row = r + r1
            col = c + c1
            if 0 <= row < len(self.map) and 0 <= col < len(self.map[0]):
                icon: str = self.map[row][col]
                if icon == "#" or ("A" <= icon < "Z" and icon.lower() in self.keys):
                    pass
                else:
                    neighbors.append((row, col))
        return neighbors

    def distance_to_next_keys(self):

        results = dict()
        for key, key_pos in self.keys.items():
            frontier = [Node(self.current_pos, None, steps=0)]
            visited = set()

            while frontier:
                node = frontier.pop()
                state = node.state
                if state == key_pos:
                    results[key] = node
                    break

                for neighbor in self.get_neighbors(state):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        frontier.append(Node(neighbor, node, steps=node.steps + 1))

        return results


def get_options(node: Node):
    r = node.state.distance_to_next_keys()
    return [(k, v.state, v.steps, node) for k, v in r.items()]


def run():
    lines = helpers.get_lines(r"./data/day_18.txt")
    result = get_shortest_steps_to_all_keys(Vault(lines))
    print("Part01:", result)


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
    t4 = """########################
#@..............ac.GI.b#
###d#e#f################
###A#B#C################
###g#h#i################
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

    r1 = get_shortest_steps_to_all_keys(Vault(t1))
    assert r1 == 8

    r2 = get_shortest_steps_to_all_keys(Vault(t2))
    assert r2 == 86

    r3 = get_shortest_steps_to_all_keys(Vault(t3))
    assert r3 == 132

    r4 = get_shortest_steps_to_all_keys(Vault(t4))
    assert r4 == 81

    r5 = get_shortest_steps_to_all_keys(Vault(t5))
    assert r5 == 136


def get_shortest_steps_to_all_keys(v):
    high_value = 5902
    visited = set()
    new_node = Node(state=v, parent=None, steps=0)

    options = deque(get_options(new_node))
    while options:
        # options = deque(sorted(options, key=lambda x: x[2]))
        if len(options) % 5_000 == 0:
            print('frontier:', len(options))
            print('visited:', len(visited))

        # Original Vault returned
        key, pos, steps, node = options.popleft()

        temp = copy.deepcopy(node.state)
        temp.keys.pop(key)
        temp.current_pos = pos

        new_node = Node(state=temp, parent=node, steps=steps)
        new_total = new_node.get_total()

        if not temp.keys:
            if new_total < high_value:
                print("Value lowered to:", new_total)
                high_value = new_total

        if new_total < high_value:
            o = get_options(new_node)
            for key, pos, steps, node in o:
                new_keys = tuple(sorted([k for k in node.state.keys if k != key]))
                if (key, pos, steps, new_keys, new_node.get_total()) in visited:
                    continue
                else:
                    visited.add((key, pos, steps, new_keys, new_node.get_total()))
                    options.append((key, pos, steps, node))

    print("Result:", high_value)
    return high_value


if __name__ == "__main__":

    print("Tests starting...")
    tests()
    print("Tests completed!")

    run()
