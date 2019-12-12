from __future__ import annotations

import re
from collections import deque
import helpers

pattern = re.compile(r"^.*=(-?\d+).*=(-?\d+).*=(-?\d+).*")


class Moon:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

        self.vx = 0
        self.vy = 0
        self.vz = 0

    def __str__(self):
        return f"Moon(x={self.x:>3}, y={self.y:>3}, z={self.z:>3}, vx={self.vx:>3}, vy={self.vy:>3}, vz={self.vz:>3})"

    def __hash__(self):
        return hash((self.x, self.y, self.z, self.vx, self.vy, self.vz))

    def apply_gravity(self, other: Moon):
        if self.x != other.x:
            self.vx += 1 if self.x < other.x else -1
        if self.y != other.y:
            self.vy += 1 if self.y < other.y else -1
        if self.z != other.z:
            self.vz += 1 if self.z < other.z else -1

    def apply_velocity(self):
        self.x += self.vx
        self.y += self.vy
        self.z += self.vz

    def calc_total_energy(self):
        potential_energy = abs(self.x) + abs(self.y) + abs(self.z)
        kinetic_energy = abs(self.vx) + abs(self.vy) + abs(self.vz)
        return potential_energy * kinetic_energy


def get_moons(lines):
    moons = deque([])
    for line in lines:
        x, y, z = re.search(pattern, line).groups()
        moons.append(Moon(int(x), int(y), int(z)))
    return moons


def pprint_moon_info(moons, step=0, silent=False):
    total_energy = sum(moon.calc_total_energy() for moon in moons)

    if not silent:
        print(f"Step [{step + 1}] has a Total Energy of {total_energy}")
        # for moon in moons:
        #     print(f"\t{moon} |==> {moon.calc_total_energy()} = {abs(moon.x) + abs(moon.y) + abs(moon.z)} * {abs(moon.vx) + abs(moon.vy) + abs(moon.vz)}")

    return total_energy


def part_01(lines):

    result = 0
    moons = get_moons(lines)
    for step in range(1000):
        # print(f"Step {step + 1}:")
        for _ in range(len(moons)):
            a, b, c, d = moons
            a.apply_gravity(b)
            a.apply_gravity(c)
            a.apply_gravity(d)
            moons.rotate(1)

        [moon.apply_velocity() for moon in moons]

        result = pprint_moon_info(moons, step, silent=True)

    assert result == 9139

def part_02(lines, silent=False):

    hashes = set()
    moons = get_moons(lines)
    pprint_moon_info(moons)
    for step in range(300_000_000_000):
        for _ in range(len(moons)):
            a, b, c, d = moons
            a.apply_gravity(b)
            a.apply_gravity(c)
            a.apply_gravity(d)
            moons.rotate(1)
        [moon.apply_velocity() for moon in moons]
        if not silent:
            pprint_moon_info(moons, step)
        new_hash = hash((moons[0], moons[1], moons[2], moons[3]))
        if new_hash in hashes:
            pprint_moon_info(moons, step=step-1, silent=False)
            return step
        else:
            hashes.add(new_hash)


if __name__ == "__main__":
    lines = helpers.get_lines(r"./data/day_12.txt")
    test_01 = """<x=-1, y=0, z=2>
                <x=2, y=-10, z=-7>
                <x=4, y=-8, z=8>
                <x=3, y=5, z=-1>""".split(
        "\n"
    )

    part_01(lines)

    part_02_test_01 = part_02(test_01)
    assert part_02_test_01 == 2772, f"Expected 2772, but got {part_02_test_01}"

    # part_02(lines)