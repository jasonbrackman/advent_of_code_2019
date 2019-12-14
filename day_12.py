from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from typing import Optional

import helpers

pattern = re.compile(r"^.*=(-?\d+).*=(-?\d+).*=(-?\d+).*")


@dataclass
class Vec:
    x: int
    y: int
    z: int


class Moon:
    def __init__(self, position: Vec, axis: Optional[chr]):
        self.pos = position
        self.axis = axis

        self.vel: Vec = Vec(0, 0, 0)

    def __repr__(self):
        return f"Moon(pos={self.pos}, vel={self.vel})"

    def __hash__(self):
        if self.axis is None:
            return hash(
                (
                    self.pos.x,
                    self.pos.y,
                    self.pos.z,
                    self.vel.x,
                    self.vel.y,
                    self.vel.z,
                )
            )
        elif self.axis == "x":
            return self.hash_x()
        elif self.axis == "y":
            return self.hash_y()
        elif self.axis == "z":
            return self.hash_z()

    def hash_x(self):
        return hash((self.pos.x, self.vel.x))

    def hash_y(self):
        return hash((self.pos.y, self.vel.y))

    def hash_z(self):
        return hash((self.pos.z, self.vel.z))

    def apply_gravity(self, other: Moon):
        x = 1 if (x := self.pos.x - other.pos.x) < 0 else (0 if x == 0 else -1)
        y = 1 if (y := self.pos.y - other.pos.y) < 0 else (0 if y == 0 else -1)
        z = 1 if (z := self.pos.z - other.pos.z) < 0 else (0 if z == 0 else -1)

        self.vel.x += x
        self.vel.y += y
        self.vel.z += z

        other.vel.x -= x
        other.vel.y -= y
        other.vel.z -= z

    def apply_velocity(self):
        self.pos.x += self.vel.x
        self.pos.y += self.vel.y
        self.pos.z += self.vel.z

    def calc_total_energy(self):
        potential_energy = abs(self.pos.x) + abs(self.pos.y) + abs(self.pos.z)
        kinetic_energy = abs(self.vel.x) + abs(self.vel.y) + abs(self.vel.z)
        return potential_energy * kinetic_energy


def get_moons(lines, axis=None):
    moons = []
    for line in lines:
        x, y, z = re.search(pattern, line).groups()
        moons.append(Moon(Vec(int(x), int(y), int(z)), axis=axis))
    return moons


def pprint_moon_info(moons, step=0, silent=False):
    total_energy = sum(moon.calc_total_energy() for moon in moons)

    if not silent:
        print(f"Step [{step + 1}] has a Total Energy of {total_energy}")
        for moon in moons:
            print(
                f"\t{moon} |==> {moon.calc_total_energy()} = {abs(moon.pos.x) + abs(moon.pos.y) + abs(moon.pos.z)} * {abs(moon.vel.x) + abs(moon.vel.y) + abs(moon.vel.z)}"
            )

    return total_energy


def part_01(lines):

    result = 0
    moons = get_moons(lines)
    for step in range(1000):  # get 1000th step Total Energy
        a, b, c, d = moons
        a.apply_gravity(b)
        a.apply_gravity(c)
        a.apply_gravity(d)
        b.apply_gravity(c)
        b.apply_gravity(d)
        c.apply_gravity(d)

        [moon.apply_velocity() for moon in moons]

        result = pprint_moon_info(moons, step, silent=True)

    return result


def get_number_divisible_by_all(x, y):
    m = min(x, y)
    for i in range(1, sys.maxsize):
        r = m * i
        if (r % x) == (r % y) == 0:
            return r


def get_first_hash_hit(lines, axis=None, silent=False):
    hashes = set()
    moons = get_moons(lines, axis=axis)
    for step in range(sys.maxsize):
        a, b, c, d = moons
        a.apply_gravity(b)
        a.apply_gravity(c)
        a.apply_gravity(d)
        b.apply_gravity(c)
        b.apply_gravity(d)
        c.apply_gravity(d)

        a.apply_velocity()
        b.apply_velocity()
        c.apply_velocity()
        d.apply_velocity()

        new_hash = hash((moons[0], moons[1], moons[2], moons[3]))
        if new_hash in hashes:
            pprint_moon_info(moons, step=step - 1, silent=silent)
            return step
        else:
            hashes.add(new_hash)


def part_02(lines, silent=True):
    # this part could be optimized to look for all three in one pass...
    x = get_first_hash_hit(lines, axis="x", silent=silent)
    y = get_first_hash_hit(lines, axis="y", silent=silent)
    z = get_first_hash_hit(lines, axis="z", silent=silent)

    a = get_number_divisible_by_all(x, y)
    b = get_number_divisible_by_all(x, z)
    c = get_number_divisible_by_all(a, b)

    return c


def run():
    lines = helpers.get_lines(r"./data/day_12.txt")
    assert part_01(lines) == 9139
    assert part_02(lines) == 420788524631496


def tests():
    test_01 = "<x=-1, y=0, z=2>\n<x=2, y=-10, z=-7>\n<x=4, y=-8, z=8>\n<x=3, y=5, z=-1>".split(
        "\n"
    )

    part_02_test_01 = part_02(test_01, silent=True)
    assert part_02_test_01 == 2772, f"Expected 2772, but got {part_02_test_01}"


if __name__ == "__main__":
    tests()
    print("Passed tests...")
    run()
