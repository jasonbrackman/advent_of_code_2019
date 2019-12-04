"""
Rules:
It is a six-digit number.
The value is within the range given in your puzzle input.
Two adjacent digits are the same (like 22 in 122345).
Going from left to right, the digits never decrease; they only ever increase or stay the same (like 111123 or 135679).
"""
from collections import Counter

def run():
    # puzzle_input = 172930-683082
    a = 172930
    b = 683082

    counter1 = counter2 = 0

    for n in range(a, b):
        n = str(n)
        if list(n) == sorted(n):
            c = Counter(n).values()

            # Any repeat is good
            if any(x >= 2 for x in c):
                counter1 += 1

            # Must have at least one group of 2
            if 2 in c:
                counter2 += 1

    assert counter1 == 1675
    assert counter2 == 1142


if __name__ == "__main__":
    run()
