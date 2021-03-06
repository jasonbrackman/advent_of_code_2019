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
from multiprocessing import Pool
from typing import List, TypeVar
from functools import wraps

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
        f"[{str(command.__module__)}.{command.__name__}]: Completed in {(time.perf_counter() - t1)*1_000:0.1f} ms"
    )


def time_it_all(args: List):
    with Pool(4) as p:
        p.map(time_it, args)


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


def bfs(state, goal, successors, by_level=None, min_path_length=0, debug=False):
    longest_path = 0

    spaces_visited_at_level = []
    frontier = deque([Node(state, None)])
    visited = {state}

    count = 1
    while frontier:
        count += 1

        current_node = frontier.popleft()
        current_state = current_node.state
        current_level = current_node.level
        if debug:
            print(f"{count:^10}: {current_state}")

        if goal(current_state):
            if current_level < min_path_length:
                longest_path = current_level
                continue

            return current_node

        for neighbor in successors(current_state):
            if neighbor in visited:
                continue
            visited.add(neighbor)
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


def timeit_wrapper(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()  # Alternatively, you can use time.process_time()
        func_return_val = func(*args, **kwargs)
        end = time.perf_counter()
        print(
            "{0:<10}.{1:<8} : {2:<8}".format(
                func.__module__, func.__name__, end - start
            )
        )
        return func_return_val

    return wrapper
