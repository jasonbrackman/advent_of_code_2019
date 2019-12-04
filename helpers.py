#  MIT License
#
#  Copyright (c) 2019 Jason Brackman
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.

from __future__ import annotations

import json
import time
from collections import deque
from heapq import heappop, heappush
from multiprocessing import Pool
from typing import Callable, Dict, Generic, List, Optional, TypeVar

T = TypeVar("T")


def get_lines(path: str) -> List[str]:
    with open(path, "r") as text:
        return [line.strip() for line in text.readlines()]


def load_json(path: str) -> dict:
    with open(path, "r") as o:

        return json.load(o)


def time_it(command):
    t1 = time.perf_counter()
    command()
    print(
        f"[{str(command.__module__)}.{command.__name__}]: Completed in {time.perf_counter() - t1:0.8f} seconds"
    )


def time_it_all(args: List):
    with Pool(4) as p:
        p.map(time_it, args)


class PriorityQueue(Generic[T]):
    def __init__(self) -> None:
        self._container: List[T] = []

    @property
    def empty(self) -> bool:
        return not self._container  # not is true for empty container

    def push(self, item: T) -> None:
        heappush(self._container, item)  # in by priority

    def pop(self) -> T:
        return heappop(self._container)  # out by priority

    def __repr__(self) -> str:
        return repr(self._container)


class Node:
    def __init__(
        self, state, parent, level=1, cost: float = 0.0, heuristic: float = 0.0
    ):
        self.state = state
        self.parent = parent
        self.level = level
        self.cost = cost
        self.heuristic = heuristic

    def __repr__(self):
        return f"Node({self.state!r}, {self.parent!r}, {self.level=}, {self.cost=}, {self.heuristic=})"

    def __lt__(self, other: Node) -> bool:
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)


class Node2(Generic[T]):
    def __init__(
        self,
        state: T,
        parent: Optional[Node2],
        cost: float = 0.0,
        heuristic: float = 0.0,
    ):
        self.state = state
        self.parent = parent
        self.cost = cost
        self.heuristic = heuristic

    def __repr__(self):
        return (
            f"Node2({self.state!r}, {self.parent!r}, {self.cost=}, {self.heuristic=})"
        )

    def __lt__(self, other: Node) -> bool:
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)


def bfs(state, goal, successors, by_level=None, min_path_length=0, debug=False):
    longest_path = 0

    spaces_visited_at_level = []
    frontier = deque([Node(state, None)])
    visited = {hash(state)}

    count = 1
    while frontier:
        count += 1

        current_node = frontier.popleft()
        current_state = current_node.state
        current_level = current_node.level
        if debug and count % 100 == 0:
            print(f"{count:^10}")
            print(current_state)
        if goal(current_state):
            if current_level < min_path_length:
                longest_path = current_level
                continue
            return current_node

        for neighbor in successors(current_state):
            if hash(neighbor) in visited:
                continue
            visited.add(hash(neighbor))
            frontier.append(Node(neighbor, current_node, level=current_level + 1))

        # Not sure how to make this more generic
        if by_level is not None:
            if by_level == current_level:
                spaces_visited_at_level = len(visited)
            if current_level == by_level + 1:
                print(
                    f"At depth of [{by_level}]: Visited {spaces_visited_at_level} unique states."
                )
                by_level = None  # stop this check

    if min_path_length > 0:
        raise AttributeError(
            f"Longest Path greater than [{min_path_length}] is: (1 indexed) {longest_path}"
        )

    return None


def astar(
    initial: T,
    goal_test: Callable[[T], bool],
    successors: Callable[[T], List[T]],
    heuristic: Callable[[T], float],
) -> Optional[Node2[T]]:
    # frontier is where we've yet to go
    frontier: PriorityQueue[Node2[T]] = PriorityQueue()
    frontier.push(
        Node2(initial, None, cost=0.0, heuristic=initial.heuristic())
    )  # explored is where we've been
    explored: Dict[T, float] = {hash(initial): 0.0}
    # keep going while there is more to explore
    while not frontier.empty:
        current_node: Node2[T] = frontier.pop()
        current_state: T = current_node.state  # if we found the goal, we're done

        if goal_test(current_state):
            return current_node
        # check where we can go next and haven't explored
        for child in successors(current_state):
            new_cost: float = current_node.cost + 1  # assumes a grid, need a cost function for more sophisticated apps

            if hash(child) not in explored or explored[hash(child)] > new_cost:
                explored[hash(child)] = new_cost
                frontier.push(Node2(child, current_node, new_cost, child.heuristic()))

    return None  # went through everything and never found goal


def get_node_path_results(result, silent=False):
    flatten_nodes = list()
    if result is not None:
        flatten_nodes.append(result.state)
        while result.parent:
            result = result.parent
            flatten_nodes.append(result.state)
    for n in reversed(flatten_nodes):
        if not silent:
            print(n)

    return len(flatten_nodes)
