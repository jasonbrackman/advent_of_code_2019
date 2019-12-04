import time
import display
import helpers


def parse_input():
    results = helpers.get_lines(r"./data/day_03.txt")
    wire01 = results[0].split(",")
    wire02 = results[1].split(",")
    return [wire01, wire02]


def add_positions(pos1, pos2):
    row = pos1[0] + pos2[0]
    col = pos1[1] + pos2[1]
    return row, col


def create_path(wire):
    dirs = {"R": (0, 1), "L": (0, -1), "U": (-1, 0), "D": (1, 0)}

    current = (0, 0)

    visited = [current]

    for cmd in wire:
        d, n = cmd[0], int(cmd[1:])
        for _ in range(0, n):
            current = add_positions(current, dirs[d])
            visited.append(current)
    return visited


def manhattan_distance(pos2):
    return abs(pos2[0]) + abs(pos2[1])


def get_shortest_distances(wires):
    paths = [create_path(wire) for wire in wires]
    cross = set(paths[0]).intersection(set(paths[1]))

    footsteps = [paths[0].index(c) + paths[1].index(c) for c in cross]
    manhattan = [manhattan_distance(c) for c in cross]

    return sorted(manhattan)[1], sorted(footsteps)[1]


def tests():
    test01 = "R8,U5,L5,D3".split(",")
    test02 = "U7,R6,D4,L4".split(",")
    wires = [test01, test02]
    t1, t2 = get_shortest_distances(wires)
    assert t1 == 6
    assert t2 == 30

    test01 = "R75,D30,R83,U83,L12,D49,R71,U7,L72".split(",")
    test02 = "U62,R66,U55,R34,D71,R55,D58,R83".split(",")
    wires = [test01, test02]
    t1, t2 = get_shortest_distances(wires)
    assert t1 == 159
    assert t2 == 610

    test01 = "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51".split(",")
    test02 = "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7".split(",")
    wires = [test01, test02]
    t1, t2 = get_shortest_distances(wires)
    assert t1 == 135
    assert t2 == 410


def run():
    wires = parse_input()
    part01, part02 = get_shortest_distances(wires)
    assert part01 == 316
    assert part02 == 16368


def draw_crossed_wires():
    wires = parse_input()
    paths = [create_path(wire) for wire in wires]
    xs = []
    ys = []
    for path in paths:
        for i in path:
            xs.append(i[0])
            ys.append(i[1])
    min_x = abs(min(xs))
    min_y = abs(min(ys))

    image = display.Image(max(xs)+min_x, max(ys)+min_y)

    green = paths[0]
    blue = paths[1]
    purple = set(paths[0]).intersection(set(paths[1]))

    for g in green:
        image.pixel(g[0]+min_x, g[1]+min_y, 'green')
    for b in blue:
        image.pixel(b[0]+min_x, b[1]+min_y, 'blue')
    for p in purple:
        for incx in range(-5, 6):
            for incy in range(-5, 6):
                image.pixel(p[0]+min_x+incx, p[1]+min_y+incy, 'white')

    image.paint(r'./display/day_03.ppm')

if __name__ == "__main__":
    t1 = time.perf_counter()

    draw_crossed_wires()
    tests()
    run()

    print(f"[Completed in {time.perf_counter() - t1:0.8f} seconds")
