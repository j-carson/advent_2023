import sys
from itertools import pairwise
from pathlib import Path
from typing import Self

import pytest
from icecream import ic

# --> Puzzle solution


class Sequence:
    def __init__(self, items: list[int]):
        self.sequence = []
        self.sequence.append(items)
        self.iterate()
        ic(self.sequence)

    @property
    def latest(self) -> list[int]:
        return self.sequence[-1]

    def iterate(self):
        while not all(i == 0 for i in self.latest):
            next_seq = [j - i for i, j in pairwise(self.latest)]
            self.sequence.append(next_seq)

    def solve(self):
        solution = 0
        upwards = list(reversed(self.sequence))
        for s in upwards[1:]:
            solution = s[-1] + solution
        return solution

    def solve_p2(self):
        solution = 0
        upwards = list(reversed(self.sequence))
        for s in upwards[1:]:
            solution = s[0] - solution
        return solution

    @classmethod
    def from_line(cls, line: str) -> Self:
        return cls([int(i) for i in line.split()])


def solve(input_data):
    sequences = [Sequence.from_line(line) for line in input_data.splitlines()]
    return sum(s.solve_p2() for s in sequences)


# --> Test driven development helpers


# Test any examples given in the problem

sample = Path("input-sample.txt").read_text().strip()
EXAMPLES = [(sample, 2)]


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
