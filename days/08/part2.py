import sys
from itertools import cycle
from math import gcd
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


def solve_1(start_at, directions, lefts, rights):
    my_pos = start_at
    steps = 0
    for turn in cycle(directions):
        match turn:
            case "L":
                my_pos = lefts[my_pos]
            case "R":
                my_pos = rights[my_pos]
        steps += 1
        if my_pos.endswith("Z"):
            break
    return steps


def solve(input_data):
    directions, lefts, rights = parse(input_data)

    my_pos = [k for k in lefts.keys() if k.endswith("A")]
    cycle_time = [solve_1(k, directions, lefts, rights) for k in my_pos]
    lcm = cycle_time[0]
    for i in cycle_time[1:]:
        lcm = lcm * i // gcd(lcm, i)

    return lcm


# --> Test driven development helpers


# Test any examples given in the problem

sample = Path("input-sample2.txt").read_text().strip()
EXAMPLES = [
    (sample, 6),
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
