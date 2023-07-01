import itertools
import os
import re
from random import choices
from typing import List, Dict

from day_09 import IntCodeMachine, parse_instructions

ShipData = Dict[str, List[str]]


def _add_input(m: IntCodeMachine, message: str) -> None:
    for i in message:
        m.input(ord(i))
    m.input(10)


def load_spin() -> None:
    bogus_startup_codes = [109, 4789, 21101]
    m = IntCodeMachine(
        bogus_startup_codes,
        silent=True,
    )
    _items = [
        "jam",
        "loom",
        "mug",
        "spool of cat6",
        "prime number",
        "food ration",
        "fuel cell",
        "manifold",
    ]

    for i in range(1, len(_items) + 1):
        y = itertools.combinations(_items, i)

        buffer = ""
        for _things in y:
            if os.path.isfile("day_25.save"):
                m.load("day_25.save")

            for thing in _things:
                _add_input(m, "drop " + thing)
            _add_input(m, "inv")
            _add_input(m, "north")

            try:

                for x in range(101500):
                    m.op_codes()
                    if isinstance(m.buffer, int):
                        buffer += chr(m.buffer)

                    if "Command?" in buffer:
                        buffer = ""
            except RuntimeError as _:
                # Will get hit if we run out of inputs which is expected for this loop to keep trying
                # all combinations.
                pass

            except KeyError as _:
                # Natural end to the program...
                pattern = re.compile(r"\d+")
                results = re.findall(pattern, buffer)
                assert results[0] == "537002052"
                return

    return


def spin(m: IntCodeMachine) -> bool:
    all_items = False
    items = ""
    try:
        rooms: ShipData = {}
        visited: ShipData = {}
        descriptions: ShipData = {}

        while True:
            m.op_codes()
            if isinstance(m.buffer, int):
                items += chr(m.buffer)

            if "Command?\n" in items:
                # print(items)
                title = [i for i in items.split("\n") if i.startswith("==")]

                if title and title[0] not in rooms:
                    if title[0] == "== Pressure-Sensitive Floor ==":
                        choices_ = ["south"]
                    else:
                        choices_ = [
                            i[2:] for i in items.split("\n") if i.startswith("-")
                        ]
                    rooms[title[0]] = choices_
                    visited[title[0]] = []
                    descriptions[title[0]] = [items]

                if not title:
                    if "Items in your inventory" in items:
                        choices_ = [
                            i[2:] for i in items.split("\n") if i.startswith("-")
                        ]
                        if len(choices_) == 8:
                            all_items = True

                    items = ""
                    continue

                if all_items and title[0] == "== Security Checkpoint ==":
                    m.save()
                    return True

                for choice in rooms[title[0]]:
                    if (
                        choice
                        not in [
                            "north",
                            "south",
                            "east",
                            "west",
                            "photons",  # breaks
                            "infinite loop",  # locks up
                            "molten lava",  # just breaks
                            "escape pod",  # just breaks
                            "giant electromagnet",  # makes you stuck
                        ]
                        and choice not in visited[title[0]]
                    ):
                        _add_input(m, "take " + choice)
                        _add_input(m, "inv")
                        visited[title[0]].append(choice)

                # then attempt a move
                made_move = False
                for option in rooms[title[0]]:
                    if (
                        option in ["north", "south", "east", "west"]
                        and option not in visited[title[0]]
                    ):
                        # print(f">> {option} for {title[0]}")
                        _add_input(m, option)
                        visited[title[0]].append(option)
                        made_move = True
                        break

                if not made_move:
                    # Visited all possible rooms - let's randomly explore.
                    option = choices(
                        [
                            n
                            for n in ["north", "south", "west", "east"]
                            if n in rooms[title[0]]
                        ]
                    )[0]
                    # print(f">> {option}")
                    _add_input(m, option)
                    visited[title[0]].append(option)

                items = ""
        print("Ran out of loops.. sorry.")

    except RuntimeError as _:
        # Will get hit if we run out of inputs which is expected for this loop to keep trying
        # all combinations.
        pass

    # _pprint_debug_exploration_info(descriptions, rooms, visited)
    return False


def _pprint_debug_exploration_info(
    descriptions: ShipData, rooms: ShipData, visited: ShipData
) -> None:
    inventory = []
    for k, v in rooms.items():
        print(k, v)
    print()
    for k, v in visited.items():
        print(k, v)
        for item in set(v):
            if item not in ["north", "south", "east", "west"]:
                inventory.append(item)
        for item in rooms[k]:
            if item not in v:
                print("\tNever visited or taken:", item)
    print()
    for k, v in descriptions.items():
        print(k, v)
    print(inventory)


def run() -> None:
    instructions = parse_instructions("./data/day_25.txt")
    m = IntCodeMachine(instructions, silent=True)
    spin(m)
    load_spin()


if __name__ == "__main__":
    run()
