"""Images are sent as a series of digits that each represent the color of a single pixel.
The digits fill each row of the image left-to-right,
then move downward to the next row,
filling rows top-to-bottom until every pixel of the image is filled."""

import helpers
from collections import Counter


def parse_data():
    lines = helpers.get_lines(r"./data/day_08.txt")
    return lines[0]


def get_layer_containing_fewest_zeroes(layers):
    lowest = 1_000_000
    lowest_layer = None
    for index, layer in enumerate(layers):
        result = sum([Counter(sheet).get("0", 0) for sheet in layer])
        if result < lowest:
            lowest, lowest_layer = result, layer

    return lowest, lowest_layer


def display_layers(layers, wide, tall):
    """
    0 is black,
    1 is white, and
    2 is transparent."""

    colours = {
        "0": "   ",
        "1": " # ",
    }

    for row in range(tall):
        for col in range(wide):
            pixels = [layer[row][col] for layer in layers]
            line = next(colours[p] for p in pixels if p in colours)
            print(line, end="")
        print()


def run():
    """
    - find the layer that contains the fewest 0 digits
    - what is the number of 1 digits multiplied by the number of 2 digits?
    """

    data = parse_data()

    wide = 25
    tall = 6

    layers = []
    for index in range(0, len(data), wide * tall):
        item = data[index : index + wide * tall]
        item = [item[x : x + wide] for x in range(0, wide * tall, wide)]
        layers.append(item)

    lowest, layer = get_layer_containing_fewest_zeroes(layers)

    ones = sum([Counter(l).get("1", 0) for l in layer])
    twos = sum([Counter(l).get("2", 0) for l in layer])
    assert (ones * twos) == 1820

    display_layers(layers, wide, tall)  # ckuj


if __name__ == "__main__":
    run()
