from day_09 import IntCodeMachine, parse_instructions


def run_machine(col, row):
    instructions = parse_instructions(r"./data/day_19.txt")
    m = IntCodeMachine(instructions, silent=True).input(col).input(row)
    m.op_codes()
    return m.buffer


def iterate(count, silent=False):
    total = 0
    for row in range(count):
        for col in range(count):
            r = run_machine(row, col)
            total += r
            if not silent:
                icon = "#" if r == 1 else "."
                print(icon, end="")
        if not silent:
            print()

    return total


def iterate2(row_start, row_end, col_start, col_end):
    c = {}

    for x in range(row_start, row_end):
        n = 0
        lo = 0
        for y in range(col_start, col_end):
            r = run_machine(x, y)

            # Get last zero before the ones for the lo
            if n == 0 and r == 1:
                lo = y

            n += r

            # Get last '1' to get the hi number
            if n >= 100 and r == 0:
                hi = lo + n
                c[x] = (lo, hi)

                if x - 99 in c:
                    a, b = c[x - 99]
                    if a <= lo + 1 and (lo + 100) <= b:
                        winner = (x - 99) * 10_000 + lo
                        # print("winner:", x - 99, lo, winner)
                        return winner
                break


def reddit_fast_answer_for_part_2():
    x = y = 0
    while not run_machine(x + 99, y):
        y += 1
        while not run_machine(x, y + 99):
            x += 1
    print(x, y)
    print(x * 10000 + y)


def run():
    # part1
    result = iterate(50, silent=True)
    assert result == 154

    # Part2
    result = iterate2(840, 3000, 1_200, 2_000)
    assert result == 9791328  # 9470649 too low


if __name__ == "__main__":
    run()
