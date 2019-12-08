#!/usr/bin/env python3
import helpers
import itertools
import pathlib
import sys

sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent / 'lib'))


class IntCode:
    def __init__(self, codes):
        self.code = [x for x in codes]
        self.inputs = []
        self.ptr = 0

    def _value(self, arg, mode):
        return arg if mode else self.code[arg]

    def input(self, input):
        self.inputs.append(input)
        return self

    def run(self):
        while True:
            mode, op = divmod(self.code[self.ptr], 100)
            self.ptr += 1

            modes = [int(x) for x in reversed(str(mode))] + [0, 0, 0]

            # opcode 1: add(arg1, arg2) -> arg3
            if op == 1:
                arg1, arg2, pos = self.code[self.ptr:self.ptr + 3]
                self.code[pos] = self._value(arg1, modes[0]) + self._value(arg2, modes[1])
                self.ptr += 3

            # opcode 2: multiply(arg1, arg2) -> arg2
            elif op == 2:
                arg1, arg2, pos = self.code[self.ptr:self.ptr + 3]
                self.code[pos] = self._value(arg1, modes[0]) * self._value(arg2, modes[1])
                self.ptr += 3

            # opcode 3: read(input) -> arg1
            elif op == 3:
                pos = self.code[self.ptr]
                self.code[pos] = self.inputs.pop(0)
                self.ptr += 1

            # opcode 4: write(arg1) -> output
            elif op == 4:
                pos = self.code[self.ptr]
                self.ptr += 1
                return self._value(pos, modes[0])

            # opcode 5: if(arg1) -> jump(arg2)
            elif op == 5:
                arg1, arg2 = self.code[self.ptr:self.ptr + 2]
                self.ptr += 2

                if self._value(arg1, modes[0]) != 0:
                    self.ptr = self._value(arg2, modes[1])

            # opcode 6: if(!arg1) -> jump(arg2)
            elif op == 6:
                arg1, arg2 = self.code[self.ptr:self.ptr + 2]
                self.ptr += 2

                if self._value(arg1, modes[0]) == 0:
                    self.ptr = self._value(arg2, modes[1])

            # opcode 7: ifless(arg1, arg2) -> arg3
            elif op == 7:
                arg1, arg2, pos = self.code[self.ptr:self.ptr + 3]
                self.code[pos] = 1 if self._value(arg1, modes[0]) < self._value(arg2, modes[1]) else 0
                self.ptr += 3

            # opcode 8: ifequal(arg1, arg2) -> arg3
            elif op == 8:
                arg1, arg2, pos = self.code[self.ptr:self.ptr + 3]
                self.code[pos] = 1 if self._value(arg1, modes[0]) == self._value(arg2, modes[1]) else 0
                self.ptr += 3

            # opcode 99: halt
            elif op == 99:
                return None

            # unknown opcode
            else:
                return None


def amplify(codes):
    max_sequence = None
    max_output = 0

    for sequence in itertools.permutations(list(range(5))):
        signal = 0

        for phase in sequence:
            signal = IntCode(codes) \
                .input(phase) \
                .input(signal) \
                .run()

        if signal > max_output:
            max_output = signal
            max_sequence = sequence

    return max_output, "".join(str(x) for x in max_sequence)


def feedback(codes):
    max_sequence = None
    max_output = 0

    for sequence in itertools.permutations(list(range(5, 10))):
        result = 0

        loop = [IntCode(codes).input(phase) for phase in sequence]

        while result is not None:
            for amplifier in loop:
                signal = result
                result = amplifier.input(signal).run()
                if result is None:
                    break

        if signal > max_output:
            max_output = signal
            max_sequence = sequence

    return max_output, "".join(str(x) for x in max_sequence)


def run():
    input_file = helpers.get_lines(r'./data/day_07.txt')

    codes = [int(x) for x in input_file[0].split(",")]

    output, seq = amplify(codes)
    print(f"Max signal: {output}  Sequence: {seq}")

    output, seq = feedback(codes)
    print(f"Max signal: {output}  Sequence: {seq}")


if __name__ == '__main__':
    run()
    sys.exit(0)