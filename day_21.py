from day_09 import IntCodeMachine, parse_instructions


class SpringScript:

    t = ord("T")  # temp value (writeable)
    j = ord("J")  # jump value (writeable)

    a = ord("A")  # one tile away
    b = ord("B")  # two tiles away
    c = ord("C")  # three tiles away
    d = ord("D")  # four tiles away

    def __init__(self, instructions):
        self.m = IntCodeMachine(instructions, silent=True)

    def bump_it(self):
        o1 = ['AND', 'OR', 'NOT']
        o2 = ['A', 'B', 'C', 'D']
        o3 = ['T', 'J']

    def input_instruction(self, cmd):
        for c in list(cmd):
            self.m.input(ord(c))
        self.m.input(10)

    def run(self):
        self.m.input(ord("W")).input(ord("A")).input(ord("L")).input(ord("K")).input(10)
        while True:
            results = self.m.op_codes()
            if results:
                print(chr(results[1]), end="")
            else:
                break


if __name__ == "__main__":
    instructions = parse_instructions(r"./data/day_21.txt")

    sc = SpringScript(instructions)
    # sc.input_instruction("NOT A J")
    sc.run()
