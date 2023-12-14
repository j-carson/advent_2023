import sys
from itertools import combinations
from pathlib import Path

import numpy as np
import pytest
from icecream import ic


# --> Puzzle solution
def is_solution(puzzle_chars, guess, lengths):
    copy = list(puzzle_chars)
    for g in guess:
        copy[g] = "#"
    for i in range(len(puzzle_chars)):
        if copy[i] == "?":
            copy[i] = "."
    as_string = "".join(copy)
    splits = [chunk for chunk in as_string.split(".") if len(chunk)]
    split_sizes = [len(s) for s in splits]
    if len(splits) == len(lengths) and all(
        l1 == l2 for l1, l2 in zip(split_sizes, lengths)
    ):
        return 1
    return 0


def count_char(s, ch):
    return sum((c == ch) for c in list(s))


def score(line):
    status, counts = line.split()

    lengths = [int(i) for i in counts.split(",")]
    total_hash = sum(lengths)
    status_chars = np.array(list(status), dtype=str)

    n_hash = count_char(status, "#")
    ques_locs = np.where(status_chars == "?")[0]

    n_missing_hash = total_hash - n_hash
    if n_missing_hash:
        total = 0
        for guess in combinations(ques_locs, n_missing_hash):
            total += is_solution(status_chars, guess, lengths)
        return total
    return 1


def solve(input_data):
    result = 0
    for line in input_data.splitlines():
        result += score(line)
    return result


# --> Test driven development helpers


# Test any examples given in the problem

sample = Path("input-sample.txt").read_text().strip()
EXAMPLES = [
    (sample, 21),
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
