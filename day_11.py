from day_09 import IntCodeMachine, parse_instructions

DIRS = {
    "N": (-1, 0),
    "E": (0, 1),
    "S": (1, 0),
    "W": (0, -1),
}


def add_positions(pos1, go):
    r2, c2 = DIRS[go]
    row = pos1[0] + r2
    col = pos1[1] + c2

    return row, col


def part_01():
    panels = do_work(0)
    return len(panels)


def draw_panels():
    panels = do_work(1)

    row_collection = [x[0] for x in panels.keys()]
    col_collection = [x[1] for x in panels.keys()]

    row_min = min(row_collection)
    row_max = max(row_collection)

    col_min = min(col_collection)
    col_max = max(col_collection)

    for r in range(row_min, row_max + 1):
        for c in range(col_min, col_max + 1):
            col = "#" if panels.get((r, c), "0") == 1 else " "
            print(col, end="")
        print()


# JKZLZJBH
colours = {
    "black": 0,
    "white": 1,
}


def do_work(input_colour):
    instructions = parse_instructions(r"./data/day_11.txt")

    dirs = ["N", "E", "S", "W"]

    current_dir = 0
    current_loc = 0, 0

    panels = dict()
    panels[(0, 0)] = input_colour

    m = IntCodeMachine(instructions, silent=True).input(input_colour)
    while True:
        # break out if you can
        col = m.op_codes()
        if col is None:
            break

        # get current colour to paint before moving
        # 0 black
        # 1 white
        panels[current_loc] = colours["black"] if col[1] == 0 else colours["white"]

        # Get direction and update location: 0 is left 1 is right
        current_dir += -1 if m.op_codes()[1] == 0 else 1
        current_loc = add_positions(current_loc, dirs[current_dir % 4])

        # Add new input based on the next colour
        new_input = panels.get(current_loc, 0)
        m.input(new_input)

    return panels


def run():
    part01 = part_01()
    assert part01 == 1894

    draw_panels()  # JKZLZJBH


if __name__ == "__main__":
    run()
