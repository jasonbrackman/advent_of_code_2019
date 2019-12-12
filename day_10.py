import math

import helpers


class RegionMap:
    def __init__(self, region_map):
        self.map = region_map
        self.asteroids = self.get_all_asteroids()

    def get_all_asteroids(self):
        collection = []
        for row in range(len(self.map)):
            for col in range(len(self.map[row])):
                if self.map[row][col] == "#":
                    collection.append((col, row))
        return collection

    def count_visible(self, viewer):
        angles = self.get_angles(viewer)
        return viewer, len(angles)

    def get_angle(self, a, b):
        return math.atan2(b[1] - a[1], b[0] - a[0])

    def get_angles(self, b):
        angles = dict()
        for a in self.asteroids:
            if a != b:
                angle = self.get_angle(a, b)
                if angle not in angles:
                    angles[angle] = []
                angles[angle].append(a)
        return angles

    def pprint_map(self):
        for row in self.map:
            print(row)


def part_01(data):
    m = RegionMap(data)
    asteroids = m.get_all_asteroids()
    results = [m.count_visible(a) for a in asteroids]
    return_value = max(results, key=lambda x: x[1])

    return return_value


def part_02(data, asteroid):
    m = RegionMap(data)
    angles = m.get_angles(asteroid)
    index = get_radian_index_pointing_up(angles)

    keys = sorted(angles)

    count = 0
    ordered_asteroids = []
    while len(ordered_asteroids) != len(m.asteroids) - 1:
        key = keys[(count + index) % len(keys)]
        if angles[key]:
            remove = angles[key].pop() if key >= 0 else angles[key].pop(0)
            ordered_asteroids.append(remove)
        count += 1

    return ordered_asteroids


def get_radian_index_pointing_up(angles):
    index = 0
    for i, s in enumerate(sorted(angles)):
        if math.isclose(1.57, s, abs_tol=0.01):
            index = i
            break
    return index


def tests_part01():
    test01 = """
            .#..#
            .....
            #####
            ....#
            ...##
            """.split()

    test02 = """......#.#.
                #..#.#....
                ..#######.
                .#.#.###..
                .#..#.....
                ..#....#.#
                #..#....#.
                .##.#..###
                ##...#..#.
                .#....####""".split()

    test03 = """#.#...#.#.
                .###....#.
                .#....#...
                ##.#.#.#.#
                ....#.#.#.
                .##..###.#
                ..#...##..
                ..##....##
                ......#...
                .####.###.""".split()

    test04 = """.#..#..###
                ####.###.#
                ....###.#.
                ..###.##.#
                ##.##.#.#.
                ....###..#
                ..#.#..#.#
                #..#.#.###
                .##...##.#
                .....#.#..""".split()

    test05 = """.#..##.###...#######
                ##.############..##.
                .#.######.########.#
                .###.#######.####.#.
                #####.##.#.##.###.##
                ..#####..#.#########
                ####################
                #.####....###.#.#.##
                ##.#################
                #####.##.###..####..
                ..######..##.#######
                ####.##.####...##..#
                .#####..#.######.###
                ##...#.##########...
                #.##########.#######
                .####.#.###.###.#.##
                ....##.##.###..#####
                .#.#.###########.###
                #.#.#.#####.####.###
                ###.##.####.##.#..##""".split()
    assert part_01(test01) == ((3, 4), 8)
    assert part_01(test02) == ((5, 8), 33)
    assert part_01(test03) == ((1, 2), 35)
    assert part_01(test04) == ((6, 3), 41)
    assert part_01(test05) == ((11, 13), 210)


def tests_part02():
    test_01 = """.#....#####...#..
                ##...##.#####..##
                ##...#...#.#####.
                ..#.....#...###..
                ..#.#.....#....##""".split()

    test_02 = """.#..##.###...#######
                ##.############..##.
                .#.######.########.#
                .###.#######.####.#.
                #####.##.#.##.###.##
                ..#####..#.#########
                ####################
                #.####....###.#.#.##
                ##.#################
                #####.##.###..####..
                ..######..##.#######
                ####.##.####...##..#
                .#####..#.######.###
                ##...#.##########...
                #.##########.#######
                .####.#.###.###.#.##
                ....##.##.###..#####
                .#.#.###########.###
                #.#.#.#####.####.###
                ###.##.####.##.#..##""".split()

    result = part_01(test_02)
    solution = part_02(test_02, result[0])

    assert solution[1 - 1] == (11, 12)
    assert solution[2 - 1] == (12, 1)
    assert solution[3 - 1] == (12, 2), f"expected (12, 2), but got {solution[3-1]}"

    assert solution[10 - 1] == (12, 8)
    assert solution[20 - 1] == (16, 0)
    assert solution[50 - 1] == (16, 9)

    assert solution[100 - 1] == (
        10,
        16,
    ), f"expected (10, 16), but got {solution[100-1]}"
    assert solution[199 - 1] == (9, 6)
    assert solution[200 - 1] == (8, 2)
    assert solution[201 - 1] == (10, 9), f"expected (10, 9), but got {solution[201-1]}"
    assert solution[299 - 1] == (11, 1), f"expected (11, 1), but got {solution[299-1]}"
    result = solution[200 - 1]
    assert result[0] * 100 + result[1] == 802


def tests():
    tests_part01()
    tests_part02()


def run():
    global part_02
    data = helpers.get_lines(r"./data/day_10.txt")
    results = part_01(data)
    assert results == ((19, 14), 274)
    part_02 = part_02(data, results[0])
    part_02_200th = part_02[200 - 1]
    part_02_result = part_02_200th[0] * 100 + part_02_200th[1]
    assert part_02_result == 305


if __name__ == "__main__":
    tests()
    run()
