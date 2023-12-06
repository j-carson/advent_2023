import sys
from pathlib import Path

import pytest
from icecream import ic


# --> Puzzle solution
def solve_one_race(time, distance):
    # split time into hold_time, race_time
    wins = 0
    for i in range(time):
        hold_time = i
        race_time = time - i
        trial = hold_time * race_time
        if trial > distance:
            wins += 1
    return wins


def solve(input_data):
    times, distances = input_data.splitlines()
    times = [int(t) for t in times.split()[1:]]
    distances = [int(t) for t in distances.split()[1:]]

    score = 1
    for time, distance in zip(times, distances):
        score *= solve_one_race(time, distance)

    return score


# --> Test driven development helpers


# Test any examples given in the problem

sample = Path("input-sample.txt").read_text().strip()
EXAMPLES = [
    (sample, 288),
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
