from __future__ import annotations

import math
import re
from collections import defaultdict
from typing import List

import helpers


class Material:
    def __init__(self, name, amount, inputs=None):
        self.name: str = name
        self.amount: int = int(amount)
        self.inputs: List[Material] = [] if inputs is None else inputs

    def __repr__(self):
        return f"Material({self.name=}, {self.amount=}, {self.inputs=}"


def parse_lines(lines):
    pattern = re.compile(r"(\d+) ([A-Z]+)")
    recipes = dict()
    for line in lines:

        reactions = pattern.findall(line)
        *materials, output = reactions

        o = Material(*output[::-1])
        if o not in recipes:
            recipes[o.name] = o

        for material in materials:
            mat = Material(*material[::-1])
            o.inputs.append(mat)
            if mat.name not in recipes:
                recipes[mat.name] = mat
    return recipes


def get_max_fuel_for_ore(results, max_ore=1_000_000_000_000):
    min_ = 1
    max_ = 1_000_000_000

    result = 0
    while True:
        temp = min_ + (max_ - min_) // 2
        result = get_ore_number(results, temp)

        if result < max_ore:
            min_ = temp
        else:
            max_ = temp
        if max_ - min_ == 1:
            return min_


def tests():
    test01 = """10 ORE => 10 A
                1 ORE => 1 B
                7 A, 1 B => 1 C
                7 A, 1 C => 1 D
                7 A, 1 D => 1 E
                7 A, 1 E => 1 FUEL"""

    test02 = """9 ORE => 2 A
                8 ORE => 3 B
                7 ORE => 5 C
                3 A, 4 B => 1 AB
                5 B, 7 C => 1 BC
                4 C, 1 A => 1 CA
                2 AB, 3 BC, 4 CA => 1 FUEL"""

    test03 = """157 ORE => 5 NZVS
                165 ORE => 6 DCFZ
                44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
                12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
                179 ORE => 7 PSHF
                177 ORE => 5 HKGWZ
                7 DCFZ, 7 PSHF => 2 XJWVT
                165 ORE => 2 GPVTF
                3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT"""

    test04 = """2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG
                17 NVRVD, 3 JNWZP => 8 VPVL
                53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL
                22 VJHF, 37 MNCFX => 5 FWMGM
                139 ORE => 4 NVRVD
                144 ORE => 7 JNWZP
                5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC
                5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV
                145 ORE => 6 MNCFX
                1 NVRVD => 8 CXFTF
                1 VJHF, 6 MNCFX => 4 RFSQX
                176 ORE => 6 VJHF"""

    test05 = """171 ORE => 8 CNZTR
                7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
                114 ORE => 4 BHXH
                14 VRPVC => 6 BMBT
                6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
                6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
                15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
                13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
                5 BMBT => 4 WPTQ
                189 ORE => 9 KTJDG
                1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
                12 VRPVC, 27 CNZTR => 2 XDBXC
                15 KTJDG, 12 BHXH => 5 XCVML
                3 BHXH, 2 VRPVC => 7 MZWV
                121 ORE => 7 VRPVC
                7 XCVML => 6 RJRHP
                5 BHXH, 4 VRPVC => 5 LTCX"""

    results = parse_lines(test01.split("\n"))
    r = get_ore_number(results)
    assert r == 31, f"Expected 31, but got {r}"

    results = parse_lines(test02.split("\n"))
    r = get_ore_number(results)
    assert r == 165

    results = parse_lines(test03.split("\n"))
    r = get_ore_number(results)
    assert r == 13312

    # print("Starting part02 Tests:")
    results = parse_lines(test03.split("\n"))
    total = get_max_fuel_for_ore(results)
    assert total == 82892753

    results = parse_lines(test04.split("\n"))
    total = get_max_fuel_for_ore(results)
    assert total == 5586022

    results = parse_lines(test05.split("\n"))
    total = get_max_fuel_for_ore(results)
    assert total == 460664


def get_ore_number(results, starting_fuel=1):
    ores = 0

    extras = {k: 0 for k in results.keys()}

    queue = [("FUEL", starting_fuel)]

    while queue:
        current, multiplier = queue.pop()

        for node in results[current].inputs:
            node_name = node.name
            node_want = node.amount * multiplier
            node_item = results[node_name]

            total = extras[node_name]

            local_multiplier = math.ceil((node_want - total) / node_item.amount)
            total += node_item.amount * local_multiplier
            queue.append((node_item.name, local_multiplier))

            extras[node_name] = left_over = total - node_want
            if node_name == "ORE":
                ores += total - left_over

    return ores


def run():

    lines = helpers.get_lines(r"./data/day_14.txt")
    results = parse_lines(lines)

    part01 = get_ore_number(results)
    assert part01 == 378929

    part02 = get_max_fuel_for_ore(results)
    assert part02 == 3445249


if __name__ == "__main__":
    tests()
    run()
