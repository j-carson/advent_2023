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
    history = []
    visited = set()

    TOTAL_CYCLES = 1000000000
    for cycle_count in range(TOTAL_CYCLES):
        key = get_flat(raw_data)
        history.append(key)
        if key in visited:
            break
        visited.add(key)
        raw_data = cycle(raw_data)

    # Process cycle here
    first = history.index(key)
    cycle_length = len(history) - first - 1
    remaining_cycles = TOTAL_CYCLES - cycle_count
    batches = remaining_cycles // cycle_length

    for cycle_count in range(first + cycle_length * batches, TOTAL_CYCLES):
        raw_data = cycle(raw_data)

    return score(raw_data)


def get_flat(data):
    return "".join(data.flatten())


def cycle(raw_data):
    # North
    ohx, ohy = np.where(raw_data == "O")
    for row, col in zip(ohx, ohy):
        new_row = old_row = row
        for r in range(row - 1, -1, -1):
            if raw_data[r, col] == ".":
                new_row = r
            else:
                break
        if old_row != new_row:
            raw_data[old_row, col] = "."
            raw_data[new_row, col] = "O"
    ic(raw_data, "north")

    # West
    ohx, ohy = np.where(raw_data == "O")
    for row, col in zip(ohx, ohy):
        new_col = old_col = col
        for c in range(col - 1, -1, -1):
            if raw_data[row, c] == ".":
                new_col = c
            else:
                break
        if old_col != new_col:
            raw_data[row, old_col] = "."
            raw_data[row, new_col] = "O"
    ic(raw_data, "west")

    # South
    n_row, n_col = raw_data.shape
    ohx, ohy = np.where(raw_data == "O")
    for row, col in zip(reversed(ohx), reversed(ohy)):
        new_row = old_row = row
        for r in range(row + 1, n_row):
            if raw_data[r, col] == ".":
                new_row = r
            else:
                break
        if old_row != new_row:
            raw_data[old_row, col] = "."
            raw_data[new_row, col] = "O"
    ic(raw_data, "south")

    # East
    ohx, ohy = np.where(raw_data == "O")
    for row, col in zip(reversed(ohx), reversed(ohy)):
        new_col = old_col = col
        for c in range(col + 1, n_col):
            if raw_data[row, c] == ".":
                new_col = c
            else:
                break
        if old_col != new_col:
            raw_data[row, old_col] = "."
            raw_data[row, new_col] = "O"
    ic(raw_data, "east")

    return raw_data


# --> Test driven development helpers


# Test any examples given in the problem

cycle_examples = Path("sample-cycles.txt").read_text().strip().split("\n\n")
CYCLE_TESTS = [
    (1, cycle_examples[0]),
    (2, cycle_examples[1]),
    (3, cycle_examples[2]),
]

sample = Path("input-sample.txt").read_text().strip()
EXAMPLES = [
    (sample, 64),
]


@pytest.mark.parametrize("n_cycles,result", CYCLE_TESTS, ids=(1, 2, 3))
@pytest.mark.parametrize("sample", [sample], ids=("sample",))
def test_cycle(sample, n_cycles, result):
    raw_data = parse(sample)
    expected_result = parse(result)
    for _ in range(n_cycles):
        raw_data = cycle(raw_data)
    assert np.all(raw_data == expected_result)


@pytest.mark.parametrize("sample_data,sample_solution", EXAMPLES, ids=("sample",))
def test_samples(sample_data, sample_solution) -> None:
    assert solve(sample_data) == sample_solution


# --> Setup and run

if __name__ == "__main__":
    #  Run the test examples with icecream debug-trace turned on
    ic.disable()
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
