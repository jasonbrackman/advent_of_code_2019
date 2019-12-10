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

    telemetry_flag = False
    telemetry = dict()

    debug_flag = False

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
        self.hack_input: List[int] = []
        self.buffer = ""

        # silent is used to remove the print (annoying when running all AOC problems).
        self.silent = silent

        # Telemetry to help optimization
        self.telemetry = {i: 0 for i, _ in enumerate(self.memory)}

    def op_codes(self, debug=False):
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
                value_a = self.get_value(position_modes[0])
                value_b = self.get_value(position_modes[1])
                value_c = self.get_value(2 if position_modes[2] == 2 else 1)
                self.memory_write(value_c, value_a + value_b)

                # debug_args = [value_a, value_b, value_c]

            elif op == 2:  # mult
                value_a = self.get_value(position_modes[0])
                value_b = self.get_value(position_modes[1])
                value_c = self.get_value(2 if position_modes[2] == 2 else 1)
                self.memory_write(value_c, value_a * value_b)

                # debug_args = [value_a, value_b, value_c]

            elif op == 3:  # input to param
                # Hack to allow testing and not have to manually enter in a starting number
                if len(self.hack_input) == 0:
                    raise RuntimeError("Expected input from previous amp step...")

                result = self.hack_input.pop(0)
                if self.hack_input is None:
                    result = input("INPUT:")

                value_c = self.get_value(2 if position_modes[2] == 2 else 1)
                self.memory_write(value_c, int(result))

                # self.debug_buffer.insert(0, f"\tINPUT VALUE: {result}")
                # debug_args = [value_c]

            elif op == 4:  # output
                value_a = self.get_value(position_modes[0])

                self.buffer = value_a
                if not self.silent:
                    print(">>", self.buffer)

                # return op, self.buffer

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
                value_c = self.get_value(2 if position_modes[2] == 2 else 1)
                self.memory_write(value_c, 1 if value_a < value_b else 0)

            elif op == 8:
                """jump-if-false: if the first parameter is zero, it sets the instruction pointer to the value
                from the second parameter. Otherwise, it does nothing."""
                value_a = self.get_value(position_modes[0])
                value_b = self.get_value(position_modes[1])
                value_c = self.get_value(2 if position_modes[2] == 2 else 1)

                val = 1 if value_a == value_b else 0

                self.memory_write(value_c, val)

            elif op == 99:
                """Halt: Exit Now..."""
                if not self.silent:
                    print("Halting!")
                return self.memory[0], self.buffer

            else:
                raise RuntimeError(f"Expected, 1, 2, 3, 4, or 99, but received {op}")

            if debug:
                self.pprint_debug(pointer, op, [], position_modes)

    def pprint_debug(self, pointer, op, args, position_modes):
        print(f"{pointer:04}: {self.symb[op]:>13} [{op}] {args} | {position_modes}")

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

    def input(self, input: int):
        self.hack_input.append(input)
        return self


def parse_instructions(path):
    lines = helpers.get_lines(path)
    return [int(v) for v in lines[0].split(",")]


def run():
    instructions = parse_instructions(r"./data/day_05.txt")

    # Part01: Use 1
    m = IntCodeMachine(instructions, silent=True).input(1)
    results = m.op_codes()
    assert results[1] == 13978427

    # Part02: Use 5
    m = IntCodeMachine(instructions, silent=True).input(5)
    m.telemetry_flag = False
    results = m.op_codes()
    assert results[1] == 11189491

    if m.telemetry_flag is True:
        for k, v in m.telemetry.items():
            print(f"{k:03}: {v}")


if __name__ == "__main__":
    run()
