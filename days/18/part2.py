from pathlib import Path

import numpy as np
import parse as p
from icecream import ic


def shoelace(coords):
    xs = np.array([c[0] for c in coords])
    ys = np.array([c[1] for c in coords])
    return np.abs(np.dot(xs, np.roll(ys, 1)) - np.dot(np.roll(xs, 1), ys)) / 2


def picks(area, perimeter):
    return area + 1 + perimeter / 2


def get_area(perimeter_coords, perimeter_length):
    ic(perimeter_coords)
    ic(perimeter_length)

    area = shoelace(perimeter_coords)
    ic(area)
    return picks(area, perimeter_length)


def solve(input_data: str):
    dig_coords: list[tuple[int, int]] = []
    cur_row = 0
    cur_col = 0
    perimeter = 0

    data_rows = input_data.splitlines()

    for data in data_rows:
        _, _, code = p.parse("{} {} (#{})", data)
        amt = int(code[:5], 16)
        perimeter += amt

        direction = {
            "0": "R",
            "1": "D",
            "2": "L",
            "3": "U",
        }[code[-1]]

        match direction:
            case "R":
                dig_coords.append((cur_row, cur_col + amt))
            case "L":
                dig_coords.append((cur_row, cur_col - amt))
            case "D":
                dig_coords.append((cur_row + amt, cur_col))
            case "U":
                dig_coords.append((cur_row - amt, cur_col))

        cur_row, cur_col = dig_coords[-1]

    return get_area(dig_coords, perimeter)


if __name__ == "__main__":
    #  Run the test examples with icecream debug-trace turned on
    ic.disable()
    my_input = Path("input.txt").read_text().strip()
    result = solve(my_input)
    print(result)
