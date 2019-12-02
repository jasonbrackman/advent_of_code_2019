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


if __name__ == "__main__":
    elves = [int(line) for line in helpers.get_lines(r"./data/day_01.txt")]
    print(f"Part01: {part_01(elves)}")
    print(f"Part02: {part_02(elves)}")
