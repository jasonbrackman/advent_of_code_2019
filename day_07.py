"""Opcode 3 takes a single integer as input and saves it to the address given by its only parameter.
For example, the instruction 3,50 would take an input value and store it at address 50.
Opcode 4 outputs the value of its only parameter.
For example, the instruction 4,50 would output the value at address 50.
Programs that use these instructions will come with document"""

from itertools import permutations
from typing import List

import helpers


class IntCodeMachine:
    symb = {
        1: "add",
        2: "mul",
        3: "input",
        4: "output",
        5: "jump_if_true",
        6: "jump_if_false",
        7: "less_than",
        8: "equals",
        99: "hlt",
    }

    telemetry_flag = False
    telemetry = dict()

    debug_flag = False

    def __init__(
        self, instructions: List[int], noun=None, verb=None, silent=False,
    ):

        self.pointer = 0
        self.memory = list(instructions)

        # for day_02
        self.memory[1] = self.memory[1] if noun is None else noun
        self.memory[2] = self.memory[2] if verb is None else verb

        # for day_05
        self.hack_input: List[int] = []
        self.buffer = None

        # silent is used to remove the print (annoying when running all AOC problems).
        self.silent = silent

        # Telemetry to help optimization
        self.telemetry = {i: 0 for i, _ in enumerate(self.memory)}

    def input(self, input: int):
        self.hack_input.append(input)
        return self

    def op_codes(self):
        while True:
            # for debug purposes freeze the starting pointer
            pointer = int(self.pointer)

            # set default flags for position_modes
            position_modes = [0, 0, 0]

            op = self.memory[self.pointer]

            self.pointer += 1

            if self.telemetry_flag:
                self.telemetry[self.pointer] += 1

            # setup the modes
            if len(str(op)) > 2:
                # ABCDE
                items = list(str(op))
                while len(items) < 5:
                    items.insert(0, 0)

                op = int("".join(items[-2:]))
                position_modes = [int(i) for i in reversed(items[0:-2])]

            if op == 1:  # add
                value_a = self.get_value(position_modes[0])
                value_b = self.get_value(position_modes[1])
                value_c = self.get_value(1)
                self.memory_write(value_c, value_a + value_b)

            elif op == 2:  # multiplication
                value_a = self.get_value(position_modes[0])
                value_b = self.get_value(position_modes[1])
                value_c = self.get_value(1)
                self.memory_write(value_c, value_a * value_b)

            elif op == 3:  # input to param
                # Hack to allow testing and not have to manually enter in a starting number
                if len(self.hack_input) == 0:
                    raise RuntimeError(f"Expected input from previous amp step.")

                result = self.hack_input.pop(0)
                if self.hack_input is None:
                    result = input("INPUT:")

                value_c = self.get_value(1)
                self.memory_write(value_c, int(result))

            elif op == 4:  # output
                value_a = self.get_value(position_modes[0])
                self.buffer = value_a
                if not self.silent:
                    print(self.buffer)

                return op, self.buffer

            elif op == 5:
                """
                If not zero, sets the instruction pointer to the value from the second parameter. 
                Otherwise, it does nothing.
                """
                value_a = self.get_value(position_modes[0])
                value_b = self.get_value(position_modes[1])
                self.pointer = value_b if value_a != 0 else self.pointer

            elif op == 6:
                """jump-if-false: if the first parameter is zero, it sets the instruction pointer to the value
                from the second parameter. Otherwise, it does nothing."""
                value_a = self.get_value(position_modes[0])
                value_b = self.get_value(position_modes[1])
                self.pointer = value_b if value_a == 0 else self.pointer

            elif op == 7:
                """jump-if-false: if the first parameter is zero, it sets the instruction pointer to the value
                 from the second parameter. Otherwise, it does nothing."""
                value_a = self.get_value(position_modes[0])
                value_b = self.get_value(position_modes[1])
                value_c = self.get_value(1)
                self.memory_write(value_c, 1 if value_a < value_b else 0)

            elif op == 8:
                """jump-if-false: if the first parameter is zero, it sets the instruction pointer to the value
                from the second parameter. Otherwise, it does nothing."""
                value_a = self.get_value(position_modes[0])
                value_b = self.get_value(position_modes[1])
                value_c = self.get_value(1)
                self.memory_write(value_c, 1 if value_a == value_b else 0)

            elif op == 99:
                """Halt: Exit Now..."""
                if not self.silent:
                    print("Halting!")
                return None

            else:
                raise RuntimeError(f"Expected, 1-9 or 99, but received {op}")

            if self.debug_flag:
                self.pprint_debug(pointer, op, [], position_modes)

    def memory_write(self, position, val):
        while len(self.memory) < position + 1:
            self.memory.append(0)

        self.memory[position] = val

    def memory_read(self, position):
        while len(self.memory) < position + 1:
            self.memory.append(0)
        return self.memory[position]

    def get_value(self, position_mode):
        arg = self.memory_read(self.pointer)
        self.pointer += 1

        if position_mode == 0:
            return_value = self.memory_read(arg)
        elif position_mode == 1:
            return_value = arg
        elif position_mode == 2:
            raise NotImplemented

        return return_value

    def pprint_debug(self, pointer, op, args, position_modes):
        print(f"{pointer:04}: {self.symb[op]:>13} [{op}] {args} | {position_modes}")


def parse_instructions(path):
    lines = helpers.get_lines(path)
    return [int(v) for v in lines[0].split(",")]


def get_result(amps):
    result = 0

    while True:
        for index, amp in enumerate(amps):
            results = amp.op_codes()
            if results is None:
                return result

            # else lets feed the result to the next amp
            _, result = results
            amps[(index + 1) % 5].input(result)


def generate_amps(instructions, phase_settings):
    phases = []
    for index, i in enumerate(phase_settings):
        m = IntCodeMachine(instructions, silent=True).input(i)
        if index == 0:
            m.input(index)
        phases.append(m)
    return phases


def part_01(instructions):
    highest = 0
    for phase_settings in permutations([0, 1, 2, 3, 4], 5):
        result = 0

        for i in phase_settings:
            m = IntCodeMachine(instructions, silent=True).input(i).input(result)
            m.op_codes()
            result = m.buffer

        if result > highest:
            highest = result

    return highest


def part_02(instructions):
    highest = 0
    for permutation in permutations([5, 6, 7, 8, 9], 5):
        amps = generate_amps(instructions, permutation)
        result = get_result(amps)
        if result > highest:
            highest = result
    return highest


def run():
    instructions = parse_instructions(r"./data/day_07.txt")
    part01 = part_01(instructions)
    assert part01 == 24625

    part02 = part_02(instructions)
    assert part02 == 36497698


def tests():
    test1 = [
        int(i)
        for i in "3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5".split(
            ","
        )
    ]
    test2 = [
        int(i)
        for i in "3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10".split(
            ","
        )
    ]

    test1 = part_02(test1)
    assert test1 == 139629729
    print("Test01 Passed ... ")

    test2 = part_02(test2)
    assert test2 == 18216
    print("Test02 Passed ...")


if __name__ == "__main__":
    tests()
    run()
