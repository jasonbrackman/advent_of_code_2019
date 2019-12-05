"""Opcode 3 takes a single integer as input and saves it to the address given by its only parameter.
For example, the instruction 3,50 would take an input value and store it at address 50.
Opcode 4 outputs the value of its only parameter.
For example, the instruction 4,50 would output the value at address 50.
Programs that use these instructions will come with document"""

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

    def __init__(
        self,
        instructions: List[int],
        noun=None,
        verb=None,
        hack_input=None,
        silent=False,
    ):

        self.pointer = 0
        self.memory = list(instructions)

        # for day_02
        self.memory[1] = self.memory[1] if noun is None else noun
        self.memory[2] = self.memory[2] if verb is None else verb

        # for day_05
        self.hack_input = hack_input
        self.buffer = ""

        # silent is used to remove the print (annoying when running all AOC problems).
        self.silent = silent

    def get_result(self):
        for _ in range(0, len(self.memory)):
            result = self.op_codes()
            if result:
                return result

    def op_codes(self, debug=False):
        # for debug purposes freeze the starting pointer
        pointer = int(self.pointer)

        # set default flags for position_modes
        position_modes = [0, 0, 0]

        op = self.memory[self.pointer]
        self.pointer += 1

        if len(str(op)) > 2:
            # ABCDE
            items = list(str(op))
            while len(items) < 5:
                items.insert(0, 0)

            op = int("".join(items[-2:]))
            position_modes = [int(i) for i in reversed(items[0:-2])]

        if op == 99:
            """Halt: Exit Now..."""
            if not self.silent:
                print("Halting!")
            return self.memory[0], self.buffer

        else:
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
                result = self.hack_input
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

            else:
                raise RuntimeError(f"Expected, 1, 2, 3, 4, or 99, but received {op}")

        if debug:
            self.pprint_debug(pointer, op, args, position_modes)

    def pprint_debug(self, pointer, op, args, position_modes):
        print(f"{pointer:04}: {self.symb[op]:>13} [{op}] {args} | {position_modes}")


def parse_instructions(path):
    lines = helpers.get_lines(path)
    return [int(v) for v in lines[0].split(",")]


def run():
    instructions = parse_instructions(r"./data/day_05.txt")

    # Part01: Use 1
    m = IntCodeMachine(instructions, hack_input=1, silent=True)
    results = m.get_result()
    assert results[1] == 13978427

    # Part02: Use 5
    m = IntCodeMachine(instructions, hack_input=5, silent=True)
    results = m.get_result()
    assert results[1] == 11189491


if __name__ == "__main__":
    run()
