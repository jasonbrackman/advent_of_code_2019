"""
PPM
    P3
    # The P3 means colors are in ASCII, then 3 columns and 2 rows,
    # then 255 for max color, then RGB triplets
    3 2
    255
    255   0   0
"""

import random


class Image:

    multiplier = 2

    def __init__(self, rows, cols):
        self.COLOURS = {
            "white": "255 255 255\n",
            "black": "0 0 0\n",
            "random": f"{random.randint(0, 255)} {random.randint(0, 255)} {random.randint(0, 255)}\n",
        }

        self.rows = rows
        self.cols = cols

        # Default background is black
        self.pixels = [["0 0 0\n"] * self.cols for _ in range(self.rows)]

    def pixel(self, row, col, colour):
        if colour not in self.COLOURS:
            raise ValueError(
                f"Expected one of the following colours: {self.COLOURS.keys()}"
            )
        # print(row, col, colour)
        r = row
        c = col
        if r < self.rows and c < self.cols:
            self.pixels[r][c] = self.COLOURS[colour]

    def paint(self, file_path: str):
        ascii_colours = "P3"
        max_colour = 255

        header = f"{ascii_colours} {self.cols} {self.rows} {max_colour} "

        with open(file_path, "wt") as handle:
            handle.write(header)
            for lines in self.pixels:
                # print(lines)
                handle.writelines(lines)


if __name__ == "__main__":
    test_data = [
        "###########",
        "#0.1.....2#",
        "#.#######.#",
        "#4.......3#",
        "###########",
    ]

    rows = len(test_data)
    cols = len(test_data[0])

    for index in range(3):
        canvas = Image(rows, cols)
        for r in range(rows):
            for c in range(cols):
                colour = "black"
                if test_data[r][c] == ".":
                    colour = "white"
                elif test_data[r][c].isdigit():
                    colour = "random"
                canvas.pixel(r, c, colour)
        canvas.paint(f"./data/test_{index:02}.ppm")
