import json
import os
import random
import display
from day_09 import IntCodeMachine, parse_instructions
import helpers
from typing import List, Tuple
from ast import literal_eval
from copy import deepcopy


class Maze:
    moves = {
        1: (-1, 0),
        2: (1, 0),
        3: (0, -1),
        4: (0, 1),
    }

    status = {
        0: "#",  # wall
        1: " ",  # hallway
        2: "0",  # Oxygen
    }

    def __init__(self):

        self.current_pos = 0, 0
        self.goal_pos = None, None
        self.map = {self.current_pos: "S"}

        json_path = r"./data/day_15.json"
        if os.path.isfile(json_path):
            with open(json_path) as file:
                json_data = json.load(file)
                self.map = {literal_eval(k): v for k, v in json_data.items()}
                for k, v in self.map.items():
                    if v == "0":
                        self.goal_pos = k

        instructions = parse_instructions(r"./data/day_15.txt")
        self.m = IntCodeMachine(instructions, silent=True)

    def successors(self, state: Tuple[int, int]) -> List[Tuple[int, int]]:
        succs = []
        for k, v in Maze.moves.items():
            new_position = Maze.add_position(state, v)
            response = self.map.get(new_position, "#")
            if response != "#":
                succs.append(new_position)

        return succs

    def goal(self, state):
        return self.map[state] == "0"

    @staticmethod
    def add_position(pos1, pos2):
        return pos1[0] + pos2[0], pos1[1] + pos2[1]

    def explore(self):
        status = 0
        while status != 2:
            choice = random.choice(list(self.moves.keys()))

            self.m.input(choice)
            op, status = self.m.op_codes()

            current_pos = self.add_position(self.current_pos, self.moves[choice])
            if status != 0:
                self.current_pos = current_pos
            if status == 2:
                self.goal_pos = current_pos

            self.map[current_pos] = self.status[status]

        self.map[(0, 0)] = "S"

        # print("Found Oxygen")

    def save_map(self):
        def remap_keys(mapping):
            return {str(k): v for k, v in mapping.items()}

        with open(r"./data/day_15.json", "w") as file:
            json.dump(remap_keys(self.map), file)

    def display(self):
        rows = [k[0] for k, v in self.map.items()]
        cols = [k[1] for k, v in self.map.items()]
        rows_min, rows_max = min(rows), max(rows)
        cols_min, cols_max = min(cols), max(cols)
        row_offset, col_offset = abs(rows_min), abs(cols_min)

        image = display.Image(abs(rows_min) + rows_max, abs(cols_min) + cols_max)
        for r in range(rows_max + row_offset + 1):
            for c in range(cols_max + col_offset + 1):
                icon = self.map.get((r - row_offset, c - col_offset), "m")
                if icon == "m":
                    image.pixel(r, c, "blue")
                elif icon == " ":
                    image.pixel(r, c, "white")
                elif icon == "#":
                    image.pixel(r, c, "black")
                elif icon == "0":
                    image.pixel(r, c, "green")
                elif icon == "S":
                    image.pixel(r, c, "purple")

        image.paint(r"./display/day_15.ppm")


def shortest_path_to_oxygen(m):
    r = helpers.bfs((0, 0), m.goal, m.successors, debug=False)
    return (
        helpers.get_node_path_results(r, silent=True) - 1
    )  # don't count starting position -- only moves


def steps_to_oxygen_filled_maze(m):
    pass


def run():
    m = Maze()
    if len(m.map) == 1:
        m.explore()
        m.save_map()
    old_map_size = len(m.map)
    m.explore()
    if len(m.map) > old_map_size:
        print("found more info...")
        m.save_map()
        m.display()

    part01 = shortest_path_to_oxygen(m)
    assert part01 == 212

    steps_to_oxygen_filled_maze(m)


if __name__ == "__main__":
    run()
