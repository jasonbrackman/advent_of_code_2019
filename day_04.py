"""
Rules:
It is a six-digit number.
The value is within the range given in your puzzle input.
Two adjacent digits are the same (like 22 in 122345).
Going from left to right, the digits never decrease; they only ever increase or stay the same (like 111123 or 135679).
"""
from collections import Counter
from typing import Iterator, ValuesView, List


def run() -> None:
    # puzzle_input
    a: int = 172930
    b: int = 683082

    # Can't get around having to convert to a  list of characters for each item -- so doing it
    # all at once up front
    ii: Iterator[List[chr]] = (list(str(n)) for n in range(a, b))

    counter1: int = 0  # Counting any length repeat
    counter2: int = 0  # Must have one group of only 2
    for n in ii:
        if n == sorted(n):
            c: ValuesView = Counter(n).values()
            counter1 += 2 <= max(c)
            counter2 += 2 in c

    assert counter1 == 1675
    assert counter2 == 1142


if __name__ == "__main__":
    run()
