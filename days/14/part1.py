import sys
from pathlib import Path

import numpy as np
import pytest
from icecream import ic

# --> Puzzle solution


def parse(input_data):
    return np.array([list(row) for row in input_data.splitlines()], dtype=str)


def score(tilted):
    ic(tilted)
    flip = np.flipud(tilted)
    ohx, ohy = np.where(flip == "O")
    return sum(x + 1 for x in ohx)


def solve(input_data):
    raw_data = parse(input_data)
    ic(raw_data)
    ohx, ohy = np.where(raw_data == "O")
    ic(ohx, ohy)
    for row, col in zip(ohx, ohy):
        new_row = old_row = row
        for r in range(row - 1, -1, -1):
            ic(r)
            if raw_data[r, col] == ".":
                new_row = r
            else:
                break
        if old_row != new_row:
            raw_data[old_row, col] = "."
            raw_data[new_row, col] = "O"

    return score(raw_data)


# --> Test driven development helpers


# Test any examples given in the problem


sample = Path("input-sample.txt").read_text().strip()
EXAMPLES = [
    (sample, 136),
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
