import sys
from itertools import cycle
from pathlib import Path

import parse as p
import pytest
from icecream import ic

# --> Puzzle solution


def parse(input_data):
    directions, links = input_data.split("\n\n")
    lefts = {}
    rights = {}
    for link in links.splitlines():
        start, left, right = p.parse("{} = ({}, {})", link)
        lefts[start] = left
        rights[start] = right

    return list(directions), lefts, rights


def solve(input_data):
    directions, lefts, rights = parse(input_data)

    my_pos = "AAA"
    steps = 0
    for turn in cycle(directions):
        match turn:
            case "L":
                my_pos = lefts[my_pos]
            case "R":
                my_pos = rights[my_pos]
        steps += 1
        if my_pos == "ZZZ":
            break
    return steps


# --> Test driven development helpers


# Test any examples given in the problem

sample = Path("input-sample.txt").read_text().strip()
EXAMPLES = [
    (sample, 2),
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
