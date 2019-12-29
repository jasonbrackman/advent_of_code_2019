from day_09 import IntCodeMachine, parse_instructions


def part01():
    instructions = parse_instructions(r"./data/day_19.txt")
    total = 0
    for x in range(50):
        for y in range(50):
            m = IntCodeMachine(instructions, silent=True)
            m.input(x).input(y)
            r = m.op_codes()
            total += r[1]
            # print('#' if r[1] == 1 else '.', end=' ')
        # print()
    return total


def run():
    result = part01()
    assert result == 154


if __name__ == "__main__":
    run()
