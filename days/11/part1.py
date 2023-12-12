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


def expand_rows(galaxy):
    final_rows = []
    for row in galaxy:
        if np.sum(row) == 0:
            final_rows.append(np.array(row, copy=True, dtype=np.int8))
        final_rows.append(row)
    return np.array(final_rows, copy=True, dtype=np.int8)


def expand_galaxy(galaxy):
    galaxy = expand_rows(galaxy)
    galaxy = expand_rows(galaxy.T)
    result = galaxy.T
    ic(result)
    return result


def compress_galaxy(galaxy):
    xs, ys = np.where(galaxy == 1)
    return list(zip(xs, ys))


def distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def solve(input_data):
    galaxy = read_galaxy(input_data)
    galaxy = expand_galaxy(galaxy)
    important_points = compress_galaxy(galaxy)
    ic(important_points)

    ans = 0
    for p1, p2 in combinations(important_points, 2):
        ans += distance(p1, p2)
    return ans


# --> Test driven development helpers


# Test any examples given in the problem

sample = Path("input-sample.txt").read_text().strip()
EXAMPLES = [
    (sample, 374),
]


@pytest.mark.parametrize("sample_data,sample_solution", EXAMPLES, ids=("sample",))
def test_samples(sample_data, sample_solution) -> None:
    assert solve(sample_data) == sample_solution


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
    result = solve(my_input)
    print(result)
