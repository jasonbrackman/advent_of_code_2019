from typing import List

import helpers


class IntCodeMachine:
    symb = {1: "add", 2: "mul", 99: "hlt"}

    def __init__(self, instructions: List[int], noun=None, verb=None):
        self.pointer = 0
        self.memory = list(instructions)

        self.memory[1] = self.memory[1] if noun is None else noun
        self.memory[2] = self.memory[2] if verb is None else verb

    def get_result(self, step=4):
        for _ in range(0, len(self.memory), step):
            result = self.op_codes(step)
            if result:
                return result
            self.pointer += step

    def op_codes(self, step, debug=False):

        op, *args = self.memory[self.pointer : self.pointer + step]
        if op == 99:
            """Halt: Exit Now..."""
            return self.memory[0]

        else:
            # dereference the two address values
            value_a = self.memory[args[0]]
            value_b = self.memory[args[1]]

            if op == 1:  # add
                self.memory[args[2]] = value_a + value_b

            elif op == 2:  # mult
                self.memory[args[2]] = value_a * value_b

            else:
                raise RuntimeError(f"Expected, 1, 2, or 99, but received {op}")

        if debug:
            self.pprint_debug(args, op, value_a, value_b)

    def pprint_debug(self, args, op, value_a, value_b):
        print(
            f"{op:03}, {args[0]:03}, {args[1]:03}, {args[2]:03} | "
            f"{args[2]:>3} => {self.symb[op]:>4}({value_a}, {value_b}) = {self.memory[args[2]]}"
        )


def parse_instructions(path):
    lines = helpers.get_lines(path)
    return [int(v) for v in lines[0].split(",")]


def brute_force_haystack(instructions, needle):
    for noun in range(100):
        for verb in range(100):

            m = IntCodeMachine(instructions, noun, verb)
            p = m.get_result()
            if p == needle:
                return 100 * noun + verb


def run():
    instructions = parse_instructions(r"./data/day_02.txt")
    part_01 = IntCodeMachine(instructions, noun=12, verb=2).get_result()
    part_02 = brute_force_haystack(instructions, 19690720)

    assert part_01 == 5866663
    assert part_02 == 4259


if __name__ == "__main__":
    # m = Machine(None, None, r'./data/day_02_test.txt')

    instructions = parse_instructions(r"./data/day_02.txt")
    part_01 = IntCodeMachine(instructions, noun=12, verb=2).get_result()
    part_02 = brute_force_haystack(instructions, 19690720)

    print(f"Part01: {part_01}")
    print(f"Part02: {part_02}")
