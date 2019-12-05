from __future__ import annotations

import math
from heapq import heappop, heappush
from typing import Callable, Dict, Generic, List, Optional, TypeVar

T = TypeVar("T")


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


class Node(Generic[T]):
    def __init__(
        self,
        state: T,
        parent: Optional[Node],
        cost: float = 0.0,
        heuristic: float = 0.0,
    ):
        self.state = state
        self.parent = parent
        self.cost = cost
        self.heuristic = heuristic

    def __repr__(self):
        return f"Node({self.state!r}, {self.parent!r}, {self.cost=}, {self.heuristic=})"

    def __lt__(self, other: Node) -> bool:
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)


def euclidean_distance(goal: T) -> Callable[[T], float]:
    def distance(ml: T) -> float:
        xdist: int = ml.column - goal.column
        ydist: int = ml.row - goal.row
        return math.sqrt((xdist * xdist) + (ydist * ydist))

    return distance


def manhattan_distance(goal: T) -> Callable[[T], float]:
    def distance(ml: T) -> float:
        xdist: int = abs(ml.column - goal.column)
        ydist: int = abs(ml.row - goal.row)
        return xdist + ydist

    return distance


def astar(
    initial: T,
    goal_test: Callable[[T], bool],
    successors: Callable[[T], List[T]],
    heuristic: Callable[[T], float],
) -> Optional[Node[T]]:
    # frontier is where we've yet to go
    frontier: PriorityQueue[Node[T]] = PriorityQueue()
    frontier.push(Node(initial, None, cost=0.0, heuristic=heuristic(initial)))

    # explored is where we've been
    explored: Dict[T, float] = {hash(initial): 0.0}

    # keep going while there is more to explore
    while not frontier.empty:
        current_node: Node[T] = frontier.pop()
        current_state: T = current_node.state  # if we found the goal, we're done

        if goal_test(current_state):
            return current_node

        for child in successors(current_state):
            new_cost: float = current_node.cost + 1  # assumes a grid, need a cost function for more sophisticated apps

            if hash(child) not in explored or explored[hash(child)] > new_cost:
                explored[hash(child)] = new_cost
                frontier.push(Node(child, current_node, new_cost, heuristic(child)))

    return None  # went through everything and never found goal
