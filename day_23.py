from collections import deque, defaultdict
from typing import Dict, List, Optional, Tuple

from day_09 import IntCodeMachine, parse_instructions


class Nat:
    def __init__(self) -> None:
        self.idles = 0
        self.part01: Optional[int] = None
        self._signal: Optional[Tuple[int, int]] = None
        self._count = 0

    @property
    def signal(self):
        self._count += 1
        assert self._signal is not None
        return self._signal

    @signal.setter
    def signal(self, value: List[int]) -> None:
        self._count = 0  # reset counter
        if self.part01 is None:
            self.part01 = value[1]
        self._signal = value[0], value[1]

    def is_second_use(self) -> bool:
        return self._count == 2


q: Dict[int, deque[int]] = defaultdict(deque)


class XMasError(BaseException):
    pass


def start_network(machines: List[IntCodeMachine], nat: Nat) -> None:
    keys = set()
    while True:
        # Fill up the machines
        for key in q.keys():

            m = machines[key]
            while q[key]:
                nat.idles = 0  # not idle; accepting input
                keys.add(key)
                m.input(q[key].popleft())

        for key in range(50):
            m = machines[key]
            buffer: List[int] = []
            while True:
                try:
                    m.op_codes()
                    if m.buffer is not None:
                        nat.idles = 0  # reset buffer -- not idle
                        buffer.append(int(m.buffer))
                    if len(buffer) == 3:
                        if buffer[0] == 255:
                            nat.signal = (buffer[1], buffer[2])
                        else:
                            q[buffer[0]].append(buffer[1])
                            q[buffer[0]].append(buffer[2])
                        buffer.clear()

                except (IndexError, RuntimeError) as e:
                    m.input(-1)
                    nat.idles += 1  # likely should only add if q is empty .. but meh.

                    if nat.idles == 100:  # all items are idle
                        a, b = nat.signal
                        machines[0].input(a)
                        machines[0].input(b)
                        if nat.is_second_use():
                            raise XMasError("All criteria met.")
                        nat.idles = 0
                    break
        keys.clear()


def run() -> None:
    nat = Nat()
    instructions = parse_instructions("./data/day_23.txt")

    machines = []
    for x in range(50):
        m = IntCodeMachine(instructions, silent=True)
        m.input(x)  # providing the network address 0-49
        machines.append(m)
    q[0].append(-1)

    try:
        start_network(machines, nat)
    except XMasError as _:
        assert nat.part01 == 17283
        assert nat.signal[1] == 11319


if __name__ == "__main__":
    run()
