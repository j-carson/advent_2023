import sys
from itertools import combinations
from pathlib import Path

import numpy as np
import pytest
from icecream import ic

# --> Puzzle solution


def read_galaxy(input_data):
    galaxy = np.array(
        [[0 if ch == "." else 1 for ch in line] for line in input_data.splitlines()]
    )
    ic(galaxy)
    return galaxy


def expand_galaxy(galaxy, expansion_factor):
    x_expansion_points = np.where([np.sum(row) == 0 for row in galaxy])[0]
    y_expansion_points = np.where([np.sum(col) == 0 for col in galaxy.T])[0]

    xs, ys = np.where(galaxy == 1)
    ic(xs, ys)
    new_xs = []
    new_ys = []
    for x, y in zip(xs, ys):
        x_expansion_count = np.sum(x_expansion_points < x)
        new_xs.append(x + (expansion_factor - 1) * x_expansion_count)
        y_expansion_count = np.sum(y_expansion_points < y)
        new_ys.append(y + (expansion_factor - 1) * y_expansion_count)

    return list(zip(new_xs, new_ys))


def distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def solve(input_data, expansion_factor):
    galaxy = read_galaxy(input_data)
    important_points = expand_galaxy(galaxy, expansion_factor)
    ic(important_points)

    ans = 0
    for (
        p1,
        p2,
    ) in combinations(important_points, 2):
        ic(p1, p2)
        ans += distance(p1, p2)
    return ans


# --> Test driven development helpers


# Test any examples given in the problem

sample = Path("input-sample.txt").read_text().strip()
EXAMPLES = [
    (sample, 2, 374),
    (sample, 10, 1030),
    (sample, 100, 8410),
]
IDS = [
    "sample2",
    "sample10",
    "sample100",
]


@pytest.mark.parametrize(
    "sample_data,expansion_factor,sample_solution", EXAMPLES, ids=IDS
)
def test_samples(sample_data, expansion_factor, sample_solution) -> None:
    assert solve(sample_data, expansion_factor) == sample_solution


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

    #  Actual input data generally has more iterations, turn off log
    ic.disable()
    my_input = Path("input.txt").read_text().strip()
    result = solve(my_input, 1000000)
    print(result)
