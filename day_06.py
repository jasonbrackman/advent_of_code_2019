import helpers


def generate_tree(lines):
    space = dict()
    for line in lines:
        a, b = line.split(")")
        # print(f"{b} orbits {a}")
        space[b] = a
    return space


def steps_to_root(key, tree):
    count = 0
    route = [key]
    while key is not None:
        key = tree.get(key, None)
        route.append(key)
        count += 1
    # print(list(reversed(route)))
    return count - 1, list(reversed(route))  # don't count the COM


def get_total_direct_and_indirect_orbits(space):
    total = 0
    for k in space.keys():
        t, route = steps_to_root(k, space)
        total += t
    return total


def find_root_add_remaining_orbits(space):
    t1, you = steps_to_root("YOU", space)
    t2, san = steps_to_root("SAN", space)
    counter = -1  # remove the None
    for (a, b) in zip(you, san):
        if a == b:
            counter += 1
        else:
            break
    return t1 - counter + t2 - counter


def tests():
    t1 = """COM)B
    B)C
    C)D
    D)E
    E)F
    B)G
    G)H
    D)I
    E)J
    J)K
    K)L""".split()

    t2 = """COM)B
    B)C
    C)D
    D)E
    E)F
    B)G
    G)H
    D)I
    E)J
    J)K
    K)L
    K)YOU
    I)SAN""".split()

    x = generate_tree(t1)
    total1, _ = steps_to_root("D", x)
    total2, _ = steps_to_root("L", x)
    assert total1 == 3
    assert total2 == 7
    assert get_total_direct_and_indirect_orbits(x) == 42

    y = generate_tree(t2)
    assert find_root_add_remaining_orbits(y) == 4


def run():
    lines_01 = helpers.get_lines(r"./data/day_06.txt")
    x = generate_tree(lines_01)
    part_01 = get_total_direct_and_indirect_orbits(x)
    assert part_01 == 223251
    part_02 = find_root_add_remaining_orbits(x)
    assert part_02 == 430


if __name__ == "__main__":
    tests()
    run()
