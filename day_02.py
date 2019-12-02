import helpers
from typing import List


def parse_instructions(path):
    lines = helpers.get_lines(path)
    return [int(v) for v in lines[0].split(",")]


class IntCodeMachine:
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

    def op_codes(self):
        op = self.memory[self.pointer]

        if op == 99:
            return self.memory[0]

        address1 = self.memory[self.pointer + 1]
        address2 = self.memory[self.pointer + 2]
        address3 = self.memory[self.pointer + 3]

        value_a = self.memory[address1]
        value_b = self.memory[address2]

        if op == 1:
            self.memory[address3] = value_a + value_b

        elif op == 2:
            self.memory[address3] = value_a * value_b

        else:
            raise ValueError(f"Expected, 1, 2, or 99, but got {op}")

        self.pointer += 4

        return None


def perform_hack(instructions, number):
    for noun in range(0, 100):
        for verb in range(0, 100):

            m = IntCodeMachine(instructions, noun, verb)
            p = m.get_result()
            if p == number:
                return 100 * noun + verb


if __name__ == "__main__":
    # m = Machine(None, None, r'./data/day_02_test.txt')

    instructions = parse_instructions(r"./data/day_02.txt")

    part_01 = IntCodeMachine(instructions, noun=12, verb=2).get_result()
    print(f"Part01: {part_01}")

    part_02 = perform_hack(instructions, 19690720)
    print(f"Part02: {part_02}")
