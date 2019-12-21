from day_09 import IntCodeMachine, parse_instructions


class Ascii:
    def __init__(self):
        self.grid = self.extract_grid()

    @staticmethod
    def extract_grid():
        instructions = parse_instructions(r"./data/day_17.txt")
        m = IntCodeMachine(instructions, silent=True)

        lines = []
        line = ""

        while True:
            results = m.op_codes()
            if results is None:
                break
            op, code = results
            code = int(code)
            if code == 10:
                if len(line) > 1:
                    lines.append(list(line))
                line = ""
            else:
                line += chr(code)

        return lines

    def identify_crossovers(self):
        total = 0
        for r in range(len(self.grid)):
            for c in range(len(self.grid[0])):
                if 0 <= r < len(self.grid) - 1 and 0 <= c < len(self.grid[0]) - 1:
                    if (
                        self.grid[r][c]
                        == self.grid[r - 1][c]
                        == self.grid[r + 1][c]
                        == self.grid[r][c - 1]
                        == self.grid[r][c + 1]
                        == "#"
                    ):
                        total += r * c

        return total


def run():
    ascii = Ascii()
    part01 = ascii.identify_crossovers()
    assert part01 == 4408


if __name__ == "__main__":
    run()
