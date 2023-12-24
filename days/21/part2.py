import sys
from functools import cache
from pathlib import Path

import numpy as np
import pytest
from icecream import ic

# --> Puzzle solution


class Puzzle:
    def __init__(self, garden_map):
        data = []
        for row_num, map_data in enumerate(garden_map.splitlines()):
            row_data = []
            for col_num, cell in enumerate(list(map_data)):
                if cell == "#":
                    row_data.append(0)
                else:
                    row_data.append(1)
                if cell == "S":
                    self.starting_point = (row_num, col_num)
            data.append(row_data)

        self.garden_map = np.array(data, dtype=bool)
        self.n_row, self.n_col = self.garden_map.shape

    def open_square(self, point):
        row, col = point
        row = row % self.n_row
        col = col % self.n_col
        return self.garden_map[row, col]

    @cache
    def solve1(self, row, col):
        return {
            p
            for p in ((row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1))
            if self.open_square(p)
        }

    def solve(self, nsteps):
        acc = set()
        acc.add(self.starting_point)

        for _ in range(nsteps):
            newpoints = set()
            for p in acc:
                newpoints |= self.solve1(*p)
            acc = newpoints
        return len(acc)


def solve(input_data, n_steps):
    puzzle = Puzzle(input_data)
    return puzzle.solve(n_steps)


# --> Test driven development helpers


# Test any examples given in the problem

sample_input = Path("input-sample.txt").read_text().strip()
EXAMPLES = [
    (sample_input, 6, 16),
    (sample_input, 10, 50),
    (sample_input, 50, 1594),
    (sample_input, 100, 6536),
    (sample_input, 500, 167004),
]


@pytest.mark.parametrize("sample_data,n_steps,sample_solution", EXAMPLES)
def test_samples(sample_data, n_steps, sample_solution) -> None:
    assert solve(sample_data, n_steps) == sample_solution


# --> Setup and run

if __name__ == "__main__":
    #  Run the test examples with icecream debug-trace turned on
    ic.enable()
    ex = pytest.main([__file__, "--capture=tee-sys", "-v"])
    if ex not in {pytest.ExitCode.OK, pytest.ExitCode.NO_TESTS_COLLECTED}:
        print(f"tests FAILED ({ex})")
        sys.exit(1)
    else:
        print("tests PASSED")

    ic(solve(sample_input, 1))
    ic(solve(sample_input, 2))
    ic(solve(sample_input, 3))
    ic(solve(sample_input, 4))
    ic(solve(sample_input, 5))
    ic(solve(sample_input, 10))

    my_input = Path("input.txt").read_text().strip()

    ic(solve(my_input, 1))
    ic(solve(my_input, 2))
    ic(solve(my_input, 3))
    ic(solve(my_input, 4))
    ic(solve(my_input, 5))
    ic(solve(my_input, 10))

    # I didn't see the pattern by eye, had to look up how they did it on reddit
    # formula: https://math.stackexchange.com/questions/680646/get-polynomial-function-from-3-points/680695#680695
    x1, x2, x3 = 65, 65 + 131, 65 + 2 * 131
    y1 = solve(my_input, x1)
    y2 = solve(my_input, x2)
    y3 = solve(my_input, x3)

    a = (x1 * (y3 - y2) + x2 * (y1 - y3) + x3 * (y2 - y1)) / (
        (x1 - x2) * (x1 - x3) * (x2 - x3)
    )
    b = (y2 - y1) / (x2 - x1) - a * (x1 + x2)
    c = y1 - a * x1**2 - b * x1

    n_steps = 26501365

    print(a * n_steps**2 + b * n_steps + c)
