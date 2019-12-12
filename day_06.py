from collections import deque

import helpers


class SpaceNode:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent

    def depth(self):
        return 0 if not self.parent else self.parent.depth() + 1

    def route(self):
        result = deque([])

        p = self
        while p.parent:
            result.appendleft(p.state)
            p = p.parent
        result.appendleft(p.state)

        return result


def generate_tree2(lines):
    space = dict()

    for line in lines:
        parent, child = line.split(")")
        if parent not in space:
            space[parent] = SpaceNode(parent)
        if child not in space:
            space[child] = SpaceNode(child)
        space[child].parent = space[parent]

    return space


def generate_tree(lines):
    space = dict()
    for line in lines:
        a, b = line.split(")")
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


def find_root_add_remaining_orbits2(space, item_01, item_02):
    v = space[item_01].route()
    y = space[item_02].route()

    index = 0
    for a, b in zip(v, y):
        if a == b:
            index += 1
        else:
            break

    return space[item_01].depth() + space[item_02].depth() - (index * 2)


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

    # Better example
    test = generate_tree2(t1)
    assert test["D"].depth() == 3
    assert test["L"].depth() == 7
    assert sum([test[item].depth() for item in test]) == 42

    test2 = generate_tree2(t2)
    result = find_root_add_remaining_orbits2(test2, "YOU", "SAN")
    assert result == 4
    # ---------------

    x = generate_tree(t1)
    total1, _ = steps_to_root("D", x)
    total2, _ = steps_to_root("L", x)
    assert total1 == 3
    assert total2 == 7
    assert get_total_direct_and_indirect_orbits(x) == 42

    y = generate_tree(t2)
    assert find_root_add_remaining_orbits(y) == 4


def run1():
    # Slightly faster ... more funcs.
    lines_01 = helpers.get_lines(r"./data/day_06.txt")

    x = generate_tree(lines_01)
    part_01 = get_total_direct_and_indirect_orbits(x)
    assert part_01 == 223251

    part_02 = find_root_add_remaining_orbits(x)
    assert part_02 == 430


def run():
    # Slower, but likely easier to read ...
    lines_01 = helpers.get_lines(r"./data/day_06.txt")

    tree = generate_tree2(lines_01)
    part_01 = sum([tree[i].depth() for i in tree])
    assert part_01 == 223251

    part_02 = find_root_add_remaining_orbits2(tree, "YOU", "SAN")
    assert part_02 == 430


if __name__ == "__main__":
    tests()
    run()
    run1()
