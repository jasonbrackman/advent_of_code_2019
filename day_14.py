from __future__ import annotations
from typing import List, NamedTuple, Optional
import helpers
from dataclasses import dataclass
import re


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

    results = parse_lines(test01.split("\n"))
    r = get_ore_number(results)
    assert r == 31, f"Expected 31, but got {r}"

    results = parse_lines(test02.split("\n"))
    r = get_ore_number(results)
    assert r == 165

    results = parse_lines(test03.split("\n"))
    r = get_ore_number(results)
    assert r == 13312


def get_ore_number(results):
    ores = 0
    extras = {k: 0 for k in results.keys()}
    totals = {k: 0 for k in results.keys()}
    queue = ["FUEL"]
    while queue:
        current = queue.pop()
        for node in results[current].inputs:
            want = node
            item = results[want.name]
            # print(want.name, "comes in lots of", item.amount, "and we want", want.amount)

            total = extras[want.name]
            extras[want.name] = 0
            while total < want.amount:
                totals[item.name] += item.amount
                total += item.amount

                queue.append(item.name)
                # print("\t", item)
            left_over = total - want.amount
            extras[want.name] += left_over
            if node.name == "ORE":
                ores += total - left_over

    return ores


def run():
    # part 01
    lines = helpers.get_lines(r"./data/day_14.txt")
    results = parse_lines(lines)
    r = get_ore_number(results)
    assert r == 378929


if __name__ == "__main__":
    tests()
    run()
