import helpers


def calculate_fuel_mass(value):
    result = 0
    while True:
        value = (value // 3) - 2
        if value <= 0:
            break
        result += value
    return result


def part_01(elves):
    return sum([(int(mass) // 3) - 2 for mass in elves])


def part_02(elves):
    return sum([calculate_fuel_mass(mass) for mass in elves])


def tests():
    assert part_01([12]) == 2
    assert part_01([14]) == 2
    assert part_01([1969]) == 654
    assert part_01([100756]) == 33583

    assert part_02([14]) == 2
    assert part_02([1969]) == 966
    assert part_02([100756]) == 50346


def run():
    elves = [int(line) for line in helpers.get_lines(r"./data/day_01.txt")]
    assert part_01(elves) == 3366415
    assert part_02(elves) == 5046772


if __name__ == "__main__":
    tests()
    run()
