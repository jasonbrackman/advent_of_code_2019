from typing import List, Optional
from dataclasses import dataclass

import helpers


@dataclass
class FFT:
    base_pattern = [0, 1, 0, -1]

    def _repeat_base_pattern(self):
        cycle = 0
        while True:
            for item in self.base_pattern:
                for _ in range(cycle):
                    yield item
            cycle += 1

    @staticmethod
    def get_digit(number, n):
        return abs(number) // 10 ** n % 10

    def repeat_phrase(self, signal):
        pattern_count = len(self.base_pattern)

        gen = self._repeat_base_pattern()

        results: List[Optional[str, int]] = []

        for iteration in range(1, len(signal) + 1):
            repeat_count = pattern_count * iteration
            repeat = [next(gen) for _ in range(repeat_count)]
            total = sum(
                s * repeat[(index + 1) % repeat_count] for index, s in enumerate(signal)
            )
            results.append(self.get_digit(total, 0))

        return results


def tests():
    signal = [int(i) for i in list("12345678")]
    f = FFT()

    # single repeat phrase
    r = f.repeat_phrase(signal)
    assert r == [int(i) for i in list("48226158")], f"Obtained: {r}"

    # repeated four times
    for _ in range(4):
        signal = f.repeat_phrase(signal)
    assert signal == [int(i) for i in list("01029498")]

    # longer signal repeated 100 times
    signal = [int(i) for i in list("80871224585914546619083218645595")]
    for _ in range(100):
        signal = f.repeat_phrase(signal)
    assert signal[0:8] == [2, 4, 1, 7, 6, 1, 7, 6]

    signal = [int(i) for i in list("03036732577212944063491565474664" * 10_000)]
    i = 303673
    for _ in range(100):
        signal = f.repeat_phrase(signal)
        print(signal[i : i + 8])
    #
    # i = 303673
    # print(signal[i:i+8])
    # print(signal)


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

    # part 02
    # for _ in range(100):
    #     signal = f.repeat_phrase(signal, override=9_999)
    # part02 = int("".join((str(c) for c in signal[0:8])))
    # print(part02)
    # result = signal[part02: part02 + 8]
    # print("PART02:", result)


if __name__ == "__main__":
    tests()
    import cProfile

    cProfile.run("run()")
    # run()
