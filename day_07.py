"""Opcode 3 takes a single integer as input and saves it to the address given by its only parameter.
For example, the instruction 3,50 would take an input value and store it at address 50.
Opcode 4 outputs the value of its only parameter.
For example, the instruction 4,50 would output the value at address 50.
Programs that use these instructions will come with document"""

from typing import List
from itertools import permutations, cycle
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

    # def get_result(self):
    #     while True:
    #         result = self.op_codes()
    #         if result:
    #             return result

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

            if len(str(op)) > 2:
                # ABCDE
                items = list(str(op))
                while len(items) < 5:
                    items.insert(0, 0)

                op = int("".join(items[-2:]))
                position_modes = [int(i) for i in reversed(items[0:-2])]

            if op == 1:  # add
                args = self.memory[self.pointer : self.pointer + 3]

                value_a = self.memory[args[0]] if position_modes[0] == 0 else args[0]
                value_b = self.memory[args[1]] if position_modes[1] == 0 else args[1]
                self.memory[args[2]] = value_a + value_b

                self.pointer += 3

            elif op == 2:  # mult
                args = self.memory[self.pointer : self.pointer + 3]
                value_a = self.memory[args[0]] if position_modes[0] == 0 else args[0]
                value_b = self.memory[args[1]] if position_modes[1] == 0 else args[1]
                self.memory[args[2]] = value_a * value_b
                self.pointer += 3

            elif op == 3:  # input to param
                args = self.memory[self.pointer]

                # Hack to allow testing and not have to manually enter in a starting number
                if len(self.hack_input) == 0:
                    print(
                        "Something went awry -- expect input from previous amp step..."
                    )
                    return None

                result = self.hack_input.pop(0)
                if self.hack_input is None:
                    result = input("INPUT:")

                self.memory[args] = int(result)
                self.pointer += 1

            elif op == 4:  # output
                args = self.memory[self.pointer]
                self.buffer = self.memory[args] if position_modes[0] == 0 else args
                if not self.silent:
                    print(self.buffer)
                self.pointer += 1

                return op, self.buffer

            elif op == 5:
                """
                If not zero, sets the instruction pointer to the value from the second parameter. 
                Otherwise, it does nothing.
                """
                args = self.memory[self.pointer : self.pointer + 2]

                value_a = self.memory[args[0]] if position_modes[0] == 0 else args[0]
                value_b = self.memory[args[1]] if position_modes[1] == 0 else args[1]
                if value_a != 0:
                    self.pointer = value_b
                else:
                    self.pointer += 2

            elif op == 6:
                """jump-if-false: if the first parameter is zero, it sets the instruction pointer to the value
                from the second parameter. Otherwise, it does nothing."""
                args = self.memory[self.pointer : self.pointer + 2]
                value_a = self.memory[args[0]] if position_modes[0] == 0 else args[0]
                value_b = self.memory[args[1]] if position_modes[1] == 0 else args[1]
                if value_a == 0:
                    self.pointer = value_b
                else:
                    self.pointer += 2

            elif op == 7:
                """jump-if-false: if the first parameter is zero, it sets the instruction pointer to the value
                 from the second parameter. Otherwise, it does nothing."""
                args = self.memory[self.pointer : self.pointer + 3]

                value_a = self.memory[args[0]] if position_modes[0] == 0 else args[0]
                value_b = self.memory[args[1]] if position_modes[1] == 0 else args[1]

                self.memory[args[2]] = 1 if value_a < value_b else 0

                self.pointer += 3

            elif op == 8:
                """jump-if-false: if the first parameter is zero, it sets the instruction pointer to the value
                from the second parameter. Otherwise, it does nothing."""
                args = self.memory[self.pointer : self.pointer + 3]

                value_a = self.memory[args[0]] if position_modes[0] == 0 else args[0]
                value_b = self.memory[args[1]] if position_modes[1] == 0 else args[1]
                self.memory[args[2]] = 1 if value_a == value_b else 0

                self.pointer += 3

            elif op == 99:
                """Halt: Exit Now..."""
                if not self.silent:
                    print("Halting!")
                return None

            else:
                raise RuntimeError(f"Expected, 1-9 or 99, but received {op}")

            if self.debug_flag:
                self.pprint_debug(pointer, op, args, position_modes)

    def pprint_debug(self, pointer, op, args, position_modes):
        print(f"{pointer:04}: {self.symb[op]:>13} [{op}] {args} | {position_modes}")


def parse_instructions(path):
    lines = helpers.get_lines(path)
    return [int(v) for v in lines[0].split(",")]


def run():
    instructions = parse_instructions(r"./data/day_05.txt")

    # Part01: Use 1
    m = IntCodeMachine(instructions, silent=True).input(1)
    results = m.get_result()
    assert results[1] == 13978427

    # Part02: Use 5
    m = IntCodeMachine(instructions, silent=True).input(5)
    m.telemetry_flag = False
    results = m.get_result()
    assert results[1] == 11189491

    if m.telemetry_flag is True:
        for k, v in m.telemetry.items():
            print(f"{k:03}: {v}")


def get_result(instructions, phase_settings, result):

    for i in phase_settings:
        m = IntCodeMachine(instructions, silent=True).input(i).input(result)
        m.op_codes()
        result = m.buffer

    return result


def get_result2(amps):
    result = 0
    while result is not None:

        for index, amp in enumerate(amps):
            results = amp.op_codes()

            # exit out if None returned
            if results is None:
                return result

            # else lets do some more work!
            _, result = results
            if result is not None:
                signal = result
                amps[(index + 1) % 5].input(signal)

    return result


def generate_amps(instructions, phase_settings):
    phases = []
    for index, i in enumerate(phase_settings):
        m = IntCodeMachine(instructions, silent=True).input(i)
        if index == 0:
            m.input(index)
        phases.append(m)
    return phases


def part_01():
    instructions = parse_instructions(r"./data/day_07.txt")
    # instructions = [int(i) for i in "3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0".split(',')]
    highest = 0
    all = permutations([0, 1, 2, 3, 4], 5)
    for nIndex in all:
        result = get_result(instructions, nIndex, result=0)
        if result > highest:
            highest = result

    assert highest == 24625


def part_02():
    instructions = parse_instructions(r"./data/day_07.txt")
    part02 = get_part_02_response(instructions)
    assert part02 == 36497698


def run():
    part_01()
    part_02()


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

    test1 = get_part_02_response(test1)
    assert test1 == 139629729
    print("Test01 Passed ... ")
    test2 = get_part_02_response(test2)
    assert test2 == 18216
    print("Test02 Passed ...")


def get_part_02_response(instructions):
    highest = 0
    for permutation in permutations([5, 6, 7, 8, 9], 5):
        # print(permutation)
        amps = generate_amps(instructions, permutation)
        result = get_result2(amps)
        if result > highest:
            highest = result

    return highest


if __name__ == "__main__":
    tests()
    run()
