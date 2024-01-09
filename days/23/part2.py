import itertools
from collections import defaultdict
from pathlib import Path
from typing import NamedTuple

import numpy as np
import pytest
from icecream import ic

# --> Puzzle solution

DIRECTIONS = [
    "north",
    "south",
    "east",
    "west",
]


class Point(NamedTuple):
    row: int
    col: int

    def north(self) -> "Point":
        return Point(self.row - 1, self.col)

    def south(self) -> "Point":
        return Point(self.row + 1, self.col)

    def east(self) -> "Point":
        return Point(self.row, self.col + 1)

    def west(self) -> "Point":
        return Point(self.row, self.col - 1)

    def go(self, direction):
        return getattr(self, direction)()


class HikingTrail:
    def __init__(self, my_input):
        lines = my_input.splitlines()

        self.trails = np.array([[(cell != "#") for cell in list(row)] for row in lines])
        self.n_row, self.n_col = self.trails.shape

        self.start = Point(0, np.where(np.array(list(lines[0])) == ".")[0][0])
        self.finish = Point(
            self.n_row - 1, np.where(np.array(list(lines[-1])) == ".")[0][0]
        )

        nodes = {self.start, self.finish}
        for row, col in itertools.product(range(self.n_row), range(self.n_col)):
            if not self.trails[row, col]:
                continue
            pt = Point(row, col)
            choices = self.get_choices(pt, set())
            if len(choices) > 2:
                nodes.add(pt)

        ic(nodes)

        edges = []
        # start pt, current pt, visit set
        workq = [(n, n, {n}) for n in nodes]
        while len(workq):
            start_pt, current_pt, current_path = workq.pop()
            choices = self.get_choices(current_pt, current_path)
            for choice in choices:
                if choice in nodes:
                    edges.append((start_pt, choice, len(current_path)))
                else:
                    new_path = set(current_path)
                    new_path.add(choice)
                    workq.append((start_pt, choice, new_path))

        self.map = defaultdict(dict)
        for item in edges:
            start, end, cost = item
            self.map[start][end] = cost
            self.map[end][start] = cost
        ic(self.map)

    def get_choices(self, pos, visit_set):
        result = []

        for direction in DIRECTIONS:
            new_pos = pos.go(direction)
            if (
                # Not off the grid
                (0 <= new_pos[0] < self.n_row)
                and (0 <= new_pos[1] < self.n_col)
                # not already visited
                and (new_pos not in visit_set)
                # is an open space
                and (self.trails[new_pos])
            ):
                result.append(new_pos)
        return result

    def take_a_hike(self):
        max_score = 0
        workq = [(self.start, {self.start}, 0)]

        while len(workq):
            cur_pos, visit_set, cost = workq.pop()
            for dest, step_cost in self.map[cur_pos].items():
                if dest in visit_set:
                    continue
                new_cost = cost + step_cost
                if dest == self.finish:
                    if new_cost > max_score:
                        max_score = new_cost
                else:
                    dest_visit_set = set(visit_set)
                    dest_visit_set.add(dest)
                    workq.append((dest, dest_visit_set, new_cost))
        return max_score


def solve(input_data):
    return HikingTrail(input_data).take_a_hike()


# --> Test driven development helpers


# Test any examples given in the problem

sample_input = Path("input-sample.txt").read_text().strip()
EXAMPLES = [
    (sample_input, 154),
]


@pytest.mark.parametrize("sample_data,sample_solution", EXAMPLES, ids=("sample",))
def test_samples(sample_data, sample_solution) -> None:
    assert solve(sample_data) == sample_solution


# --> Setup and run

if __name__ == "__main__":
    #  Run the test examples with icecream debug-trace turned on
    ic.enable()
    ex = pytest.main([__file__, "--pdb", "--capture=tee-sys", "-v"])
    if ex not in {pytest.ExitCode.OK, pytest.ExitCode.NO_TESTS_COLLECTED}:
        print(f"tests FAILED ({ex})")
    else:
        print("tests PASSED")

    #  Actual input data generally has more iterations, turn off log
    ic.disable()
    my_input = Path("input.txt").read_text().strip()
    result = solve(my_input)
    print(result)
