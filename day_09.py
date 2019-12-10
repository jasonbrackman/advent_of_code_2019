from itertools import permutations
from typing import List

import helpers


class IntCodeMachine:
    symb = {
        1: "add",
        2: "mul",
        3: "input",
        4: "output",
        5: "jump_if_!zero",
        6: "jump_if_zero",
        7: "if_less_than",
        8: "if_equal",
        9: "set_relative",
        99: "halt",
    }
    test_mode = False
    telemetry_flag = False
    telemetry = dict()

    debug_flag = False

    def __init__(
        self, instructions: List[int], noun=None, verb=None, silent=False,
    ):

        self.pointer = 0
        self.relative_base = 0
        self.memory = list(instructions)

        # for day_02
        self.memory[1] = self.memory[1] if noun is None else noun
        self.memory[2] = self.memory[2] if verb is None else verb

        # for day_05
        self.hack_input: List[int] = []
        self.buffer = None
        self.debug_buffer = []

        # silent is used to remove the print (annoying when running all AOC problems).
        self.silent = silent

        # Telemetry to help optimization
        self.telemetry = {i: 0 for i, _ in enumerate(self.memory)}

    def memory_write(self, position, val):
        while len(self.memory) < position + 1:
            self.memory.append(0)

        self.memory[position] = val

    def memory_read(self, position):
        if position < 0:
            raise RuntimeError(
                f"Expected the position to be zero or greater, but got {position}!"
            )
        while len(self.memory) < position + 1:
            self.memory.append(0)
        return self.memory[position]

    def input(self, input: int):
        self.hack_input.append(input)
        return self

    def op_codes(self):
        while True:
            # for debug purposes freeze the starting pointer
            pointer = self.pointer

            # set default flags for position_modes
            position_modes = [0, 0, 0]

            op = self.memory_read(self.pointer)

            self.pointer += 1

            if self.telemetry_flag:
                self.telemetry[self.pointer] += 1

            # setup the modes
            if len(str(op)) > 2:
                items = list(str(op))
                while len(items) < 5:
                    items.insert(0, 0)

                op = int("".join(items[-2:]))
                position_modes = [int(i) for i in reversed(items[0:-2])]

            if op == 1:  # add
                value_a = self.get_value(position_modes[0])
                value_b = self.get_value(position_modes[1])
                value_c = self.set_value(position_modes[2])
                self.memory_write(value_c, value_a + value_b)

                debug_args = [value_a, value_b, value_c]

            elif op == 2:  # multiplication
                value_a = self.get_value(position_modes[0])
                value_b = self.get_value(position_modes[1])
                value_c = self.set_value(position_modes[2])
                self.memory_write(value_c, value_a * value_b)

                debug_args = [value_a, value_b, value_c]

            elif op == 3:  # input to param

                # Hack to allow testing and not have to manually enter in a starting number
                if len(self.hack_input) == 0:
                    raise RuntimeError("Expected input from previous amp step...")

                result = self.hack_input.pop(0)

                if self.hack_input is None:
                    result = input("INPUT:")

                value_c = self.set_value(position_modes[0])
                self.memory_write(value_c, int(result))

                self.debug_buffer.insert(0, f"\tINPUT VALUE: {result}")
                debug_args = [value_c]

            elif op == 4:  # output
                value_a = self.get_value(position_modes[0])
                self.buffer = value_a

                if not self.silent:
                    print(">>", self.buffer)

                if self.test_mode is False:
                    if self.debug_flag:
                        self.pprint_debug(pointer, op, [value_a], position_modes)
                    return op, self.buffer

                debug_args = [value_a]

            elif op == 5:
                """
                If not zero, sets the instruction pointer to the value from the second parameter. 
                Otherwise, it does nothing.
                """
                value_a = self.get_value(position_modes[0])
                value_b = self.get_value(position_modes[1])
                self.pointer = value_b if value_a != 0 else self.pointer

                debug_args = [value_a, value_b]

            elif op == 6:
                """jump-if-zero: if the first parameter is zero, it sets the instruction pointer to the value
                from the second parameter. Otherwise, it does nothing."""
                value_a = self.get_value(position_modes[0])
                value_b = self.get_value(position_modes[1])
                self.pointer = value_b if value_a == 0 else self.pointer

                debug_args = [value_a, value_b]

            elif op == 7:
                """if less than: set next arg to 1 else 0"""
                value_a = self.get_value(position_modes[0])
                value_b = self.get_value(position_modes[1])
                value_c = self.set_value(position_modes[2])
                self.memory_write(value_c, 1 if value_a < value_b else 0)

                debug_args = [value_a, value_b, value_c]

            elif op == 8:
                """if equal: set next arg to 1 else 0"""
                value_a = self.get_value(position_modes[0])
                value_b = self.get_value(position_modes[1])
                value_c = self.set_value(position_modes[2])

                val = 1 if value_a == value_b else 0

                self.memory_write(value_c, val)
                debug_args = [value_a, value_b, value_c]

            elif op == 9:
                """adjusts the relative base by the value of its only parameter."""

                value_a = self.get_value(position_modes[0])

                self.relative_base += value_a

                debug_args = [value_a]

            elif op == 99:
                """Halt: Exit Now..."""

                self.pprint_debug(pointer, op, [], position_modes)
                if self.debug_flag:
                    while self.debug_buffer:
                        print(self.debug_buffer.pop())

                if not self.silent:
                    print("Halting!")

                if self.test_mode is True:
                    return op, self.buffer

                return None

            else:
                raise RuntimeError(
                    f"Expected, 1-9 or 99, but received {op}\n"
                    f" - current buffer: {self.buffer}\n"
                    f" - current pointer: {self.pointer}\n"
                    f" - memory dump: \n{self.memory}"
                )

            if self.debug_flag:
                self.pprint_debug(pointer, op, debug_args, position_modes)
                while self.debug_buffer:
                    print(self.debug_buffer.pop())

    def set_value(self, position_mode):
        raw_value = self.memory_read(self.pointer)
        self.pointer += 1
        if position_mode == 0:
            return raw_value
        elif position_mode == 2:
            x = raw_value + self.relative_base

            return x

    def get_value(self, position_mode):
        """
        - Mode 0: reads memory at pointer value
        - Mode 1: returns the pointer value
        - Mode 2: reads memory at pointer value + relative_base
        """
        self.debug_buffer.insert(0, f"\tCurrent Pointer: {self.pointer}")
        self.debug_buffer.insert(0, f"\tCurrent Relative Pointer: {self.relative_base}")
        self.debug_buffer.insert(0, f"\tCurrent Memory: {self.memory}")

        raw_value = self.memory_read(self.pointer)

        if position_mode == 0:
            # default mode
            self.debug_buffer.insert(
                0,
                f"\t[Mode {position_mode}] MemoryReadAtMemoryPointerValue({raw_value}) = {self.memory_read(raw_value)}",
            )
            return_value = self.memory_read(raw_value)

        elif position_mode == 1:
            self.debug_buffer.insert(
                0, f"\t[Mode {position_mode}] MemoryRead({self.pointer}) = {raw_value}"
            )
            return_value = raw_value

        elif position_mode == 2:
            self.debug_buffer.insert(
                0,
                f"\t[Mode {position_mode}] MemoryRead({raw_value} + {self.relative_base}) = {self.memory_read(raw_value + self.relative_base)}",
            )

            return_value = self.memory_read(raw_value + self.relative_base)

        self.pointer += 1

        return return_value

    def pprint_debug(self, pointer, op, args, position_modes):
        self.debug_buffer.insert(
            0,
            f"{pointer:04}: [{op:02}]: {self.symb[op]:>13} {tuple(args)} | Modes: {position_modes} | {self.relative_base}",
        )


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


def day_07_tests():
    t1 = [
        int(i)
        for i in "3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5".split(
            ","
        )
    ]
    t2 = [
        int(i)
        for i in "3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10".split(
            ","
        )
    ]

    test1 = part_02(t1)
    assert test1 == 139629729

    test2 = part_02(t2)
    assert test2 == 18216


def test_mode(instructions, input_=1, debug_flag=False, rb_start=0, test_mode=False):
    collection = []
    m = IntCodeMachine(instructions).input(input_)
    m.test_mode = test_mode
    m.relative_base = rb_start
    m.debug_flag = debug_flag
    m.silent = True

    _, result = m.op_codes()

    while result is not None:
        collection.append(result)
        m.input(result)
        results = m.op_codes()

        if results is None:
            break

        _, result = results

    return collection


def day_05_tests():
    instructions = parse_instructions(r"./data/day_05.txt")

    # Part01: Use 1
    m = IntCodeMachine(instructions).input(1)
    m.test_mode = True
    m.debug_flag = False
    results = m.op_codes()
    assert results[1] == 13978427

    # Part02: Use 5
    m = IntCodeMachine(instructions).input(5)
    results = m.op_codes()
    assert results[1] == 11189491


def day_09_tests():
    test1 = [
        int(x)
        for x in "109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99".split(",")
    ]
    test2 = [int(x) for x in "1102,34915192,34915192,7,4,7,99,0".split(",")]
    test3 = [int(x) for x in "104,1125899906842624,99".split(",")]

    t1 = test_mode(test1)
    assert t1 == test1
    t2 = test_mode(test2)
    assert t2 == [1219070632396864]
    t3 = test_mode(test3)
    assert t3[0] == test3[1]

    test4 = [int(x) for x in "1, 5, 0, 1985, 109, 19, 204, -34, 99".split(",")]
    t4 = test_mode(test4, debug_flag=False, rb_start=2000)
    assert t4 == [20]

    test5 = [int(x) for x in "109,1,203,11,209,8,204,1,99,10,0,42,0".split(",")]
    t5 = test_mode(test5, input_=1, debug_flag=False)
    print(t5)

    test6 = [
        int(x)
        for x in "3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99".split(
            ","
        )
    ]
    t6 = test_mode(test6, input_=9)
    print(t6)

    t6 = [int(x) for x in "109, -1, 4, 1, 99".split(",")]  # -1
    t7 = [int(x) for x in "109, -1, 104, 1, 99".split(",")]  # 1
    t8 = [int(x) for x in "109, -1, 204, 1, 99".split(",")]  # 109
    t9 = [int(x) for x in "109, 1, 9, 2, 204, -6, 99".split(",")]  # 204
    s1 = [int(x) for x in "109, 1, 109, 9, 204, -6, 99".split(",")]  # 204
    s2 = [int(x) for x in "109, 1, 209, -1, 204, -106, 99".split(",")]  # 204
    s3 = [int(x) for x in "109, 1, 3, 3, 204, 2, 99".split(",")]  # output output
    s4 = [int(x) for x in "109, 1, 203, 2, 204, 2, 99".split(",")]  # output input
    items = [
        (t6, [-1]),
        (t7, [1]),
        (t8, [109]),
        (t9, [204]),
        (s1, [204]),
        (s2, [204]),
        (s3, [1]),
        (s4, [1]),
    ]
    for item in items:
        all = test_mode(item[0], debug_flag=False, test_mode=False)
        assert all == item[1]


def run_all_tests():
    day_05_tests()
    print("Day05 Tests Pass...")
    day_07_tests()
    print("Day07 Tests Pass...")
    day_09_tests()
    print("Day09 Tests Pass...")


if __name__ == "__main__":
    run_all_tests()

    i = parse_instructions(r"./data/day_09.txt")
    part01 = test_mode(i, debug_flag=False, test_mode=False)
    assert part01 == [2932210790]
