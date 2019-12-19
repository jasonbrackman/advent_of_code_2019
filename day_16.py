from typing import List
from collections import deque
from dataclasses import dataclass

import helpers


@dataclass
class FFT:
    base_pattern = deque([0, 1, 0, -1])

    def repeat_base_pattern(self):
        cycle = 0
        while True:
            for index in range(len(self.base_pattern)):
                for x in range(cycle):
                    yield self.base_pattern[index]
            cycle += 1

    def repeat_phrase(self, signal):
        iterations = len(signal)
        pattern_count = len(self.base_pattern)
        gen = self.repeat_base_pattern()
        position = 1
        results: List[int] = []
        for iteration in range(1, iterations + 1):
            repeat = [next(gen) for _ in range(pattern_count * iteration)]

            total = 0
            for index, s in enumerate(signal, 0):
                total += s * repeat[(index + 1) % (pattern_count * iteration)]
                position += 1
            results.append(int(str(total)[-1]))

        return results


def tests():
    signal = [int(i) for i in list("12345678")]
    f = FFT()

    # single repeat phrase
    r = f.repeat_phrase(signal)
    assert r == [int(i) for i in list("48226158")]

    # repeated four times
    for _ in range(4):
        signal = f.repeat_phrase(signal)
    assert signal == [int(i) for i in list("01029498")]

    # longer signal repeated 100 times
    signal = [int(i) for i in list("80871224585914546619083218645595")]
    for _ in range(100):
        signal = f.repeat_phrase(signal)
    assert signal[0:8] == [2, 4, 1, 7, 6, 1, 7, 6]


def run():
    # prep data
    lines = helpers.get_lines(r"./data/day_16.txt")
    signal = [int(i) for i in lines[0]]

    # instantiate an FFT object
    f = FFT()

    # part 01
    for _ in range(100):
        signal = f.repeat_phrase(signal)
    assert "".join((str(c) for c in signal[0:8])) == "67481260"


if __name__ == "__main__":
    tests()

    run()
