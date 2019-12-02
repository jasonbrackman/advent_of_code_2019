import time
from typing import List

import helpers


def parse_instructions(path):
    lines = helpers.get_lines(path)
    return [int(v) for v in lines[0].split(",")]


class IntCodeMachine:
    cmds = {1: lambda a, b: a + b, 2: lambda a, b: a * b}

    def __init__(self, instructions: List[int], noun=None, verb=None):
        self.pointer = 0
        self.memory = list(instructions)

        if noun is not None:
            self.memory[1] = noun
        if verb is not None:
            self.memory[2] = verb

    def get_result(self):
        result = None
        while result is None:
            result = self.op_codes()
        return result

    def op_codes(self, debug=False):

        op, *args = self.memory[self.pointer : self.pointer + 4]
        if op == 99:
            """Halt"""
            return self.memory[0]

        if debug:
            print(f"{op} {args[0]}, {args[1]}, {args[2]}")

        try:
            # dereference the two address values
            value_a = self.memory[args[0]]
            value_b = self.memory[args[1]]

            # apply op code cmd to values and insert into address3
            self.memory[args[2]] = self.cmds[op](value_a, value_b)
        except KeyError as e:
            print(f"Expected, 1, 2, or 99, but received {e.args}")

        # Jump the pointer for next run
        self.pointer += 4


def perform_hack(instructions, number):
    for noun in range(100):
        for verb in range(100):

            m = IntCodeMachine(instructions, noun, verb)
            p = m.get_result()
            if p == number:
                return 100 * noun + verb


def run():
    instructions = parse_instructions(r"./data/day_02.txt")
    part_01 = IntCodeMachine(instructions, noun=12, verb=2).get_result()
    part_02 = perform_hack(instructions, 19690720)

    assert part_01 == 5866663
    assert part_02 == 4259


if __name__ == "__main__":
    # m = Machine(None, None, r'./data/day_02_test.txt')

    instructions = parse_instructions(r"./data/day_02.txt")
    part_01 = IntCodeMachine(instructions, noun=12, verb=2).get_result()
    part_02 = perform_hack(instructions, 19690720)

    print(f"Part01: {part_01}")
    print(f"Part02: {part_02}")

