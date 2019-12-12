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


def pprint_moon_info():
    hashes = set()
    # total_energy = 0
    for moon in moons:
        moon.apply_velocity()
        hashes.add(hash(moon))
    return hashes
    # total_energy += moon.calc_total_energy()
    # print(moon)
    # print(f"Total Energy of System: {total_energy}")


if __name__ == "__main__":

    lines = helpers.get_lines(r"./data/day_12.txt")
    test_01 = """<x=-1, y=0, z=2>
                <x=2, y=-10, z=-7>
                <x=4, y=-8, z=8>
                <x=3, y=5, z=-1>
    """.split(
        "\n"
    )
    moons = get_moons(lines)
    hashes = pprint_moon_info()

    for step in range(1_000_000_000):
        if step % 500_000 == 0:
            print(f"Step {step+1}:")
        for _ in range(len(moons)):
            a, b, c, d = moons
            a.apply_gravity(b)
            a.apply_gravity(c)
            a.apply_gravity(d)
            moons.rotate(1)

        new_hashes = pprint_moon_info()
        if all(hash in hashes for hash in new_hashes):
            print(f"Winner: {step+1}")
        else:
            hashes.union(new_hashes)
