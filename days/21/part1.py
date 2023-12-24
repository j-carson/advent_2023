import sys
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

    def inbounds(self, row, col):
        return (0 <= row < self.n_row) and (0 <= col < self.n_col)

    def neighbors(self, row, col):
        for point in ((row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1)):
            if self.inbounds(*point) and self.garden_map[point]:
                yield point

    def solve(self, nsteps):
        resultset = set()
        visitcache = set()

        workq = []
        workq.append((self.starting_point, 0))
        visitcache.add((self.starting_point, 0))

        while len(workq):
            point, distance = workq.pop()
            if distance == nsteps:
                resultset.add(point)
                continue

            assert distance < nsteps

            for neighbor in self.neighbors(*point):
                job = (neighbor, distance + 1)
                if job not in visitcache:
                    visitcache.add(job)
                    workq.append(job)

        return len(resultset)


def solve(input_data, n_steps):
    puzzle = Puzzle(input_data)
    return puzzle.solve(n_steps)


# --> Test driven development helpers


# Test any examples given in the problem

sample_input = Path("input-sample.txt").read_text().strip()
EXAMPLES = [
    (sample_input, 6, 16),
]


@pytest.mark.parametrize(
    "sample_data,n_steps,sample_solution", EXAMPLES, ids=("sample",)
)
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

    #  Actual input data generally has more iterations, turn off log
    ic.disable()
    my_input = Path("input.txt").read_text().strip()
    result = solve(my_input, 64)
    print(result)
