import os
from typing import NamedTuple

from day_09 import IntCodeMachine, parse_instructions

tile_type = {
    0: " ",  # empty
    1: "x",  # wall
    2: "*",  # block -- can be broken
    3: "_",  # horizontal paddle  (indestructible)
    4: "O",  # ball moved diagonally and bounces off objects.
}


class Pos(NamedTuple):
    col: int
    row: int


class Arcade:
    quarters = 2
    row = 26
    col = 42
    read_right_to_left = True

    def __init__(self, instructions):
        self.score = -100
        self.state = [["@"] * self.col for _ in range(self.row)]
        self.joystick_position = 0
        self.m = IntCodeMachine(instructions, quarters=self.quarters, silent=True,)
        # self.m.debug_flag = True
        # self.m.telemetry_flag = True
        self.m.stream_input = self.yield_joystick_position()

    def yield_joystick_position(self):
        while True:
            yield self.joystick_position

    def get_current_screen(self):
        ball_new = Pos(0, 0)
        paddle_pos = Pos(0, 0)

        codes = list()
        counter = 1
        while True:
            # break out if you can
            results = self.m.op_codes()
            if results is None:
                break

            op, code = results
            if op == 4:
                if counter % 3 == 0:
                    if code == 4:  # ball on the move

                        ball_new = Pos(*codes[-2:])
                        self.joystick_position = self.ball_target(ball_new, paddle_pos)
                        # print(f"[{self.joystick_position}] ball_new = {ball_new}, paddle = {paddle_pos}")

                    elif code == 3:  # paddle updated
                        paddle_pos = Pos(*codes[-2:])
                        # print(f"[{self.joystick_position}] ball_new = {ball_new}, paddle = {paddle_pos}")
                    else:
                        pass
                        # print(op, code, results)
            codes.append(code)
            counter += 1

        assert len(codes) % 3 == 0
        return self.m.buffer, codes

    @staticmethod
    def ball_target(ball_new, paddle):
        result = 0
        if paddle.col < ball_new.col:
            result = 1
        if paddle.col > ball_new.col:
            result = -1
        return result

    def automate_gameplay(self):
        result, init_state = self.get_current_screen()
        self.visualize_playback(init_state, step=3)
        return result

    def visualize_playback(self, init_state, step):
        for index in range(0, len(init_state), step):
            a, b, c = init_state[index : index + step]
            if a == -1 and b == 0:
                self.score = c
            else:
                icon = tile_type[c]
                self.state[b][a] = icon

                if icon == tile_type[3] or icon == tile_type[4]:
                    # only display when the board is ready to update
                    # The display appears to clear out the ball and paddle between moves
                    self.display()

    def display(self):
        for r in range(self.row):
            for c in range(self.col):
                print(self.state[r][c], end="")
            print()
        print(f"SCORE: {self.score}")
        os.system("clear")


def run():
    instructions = parse_instructions(r"./data/day_13.txt")
    part_01(instructions)
    part_02(instructions)


def part_01(instructions):
    codes = get_machine_codes(instructions, input=0)
    result = 0
    for index in range(0, len(codes), 3):
        items = codes[index : index + 3]
        result += 1 if items[2] == 2 else 0
    assert result == 380


def part_02(instructions):
    a = Arcade(instructions)
    result, init_state = a.get_current_screen()
    # a.visualize_playback(init_state, step=3)
    assert result == 18647


def get_machine_codes(instructions, input):
    codes = list()
    m = IntCodeMachine(instructions, noun=2, silent=True).input(input)
    while True:
        # break out if you can
        results = m.op_codes()
        if results is None:
            break
        _, code = results
        codes.append(code)
    assert len(codes) % 3 == 0
    return codes


if __name__ == "__main__":
    instructions = parse_instructions(r"./data/day_13.txt")
    a = Arcade(instructions)
    result, init_state = a.get_current_screen()
    a.visualize_playback(init_state, step=3)
    assert result == 18647
