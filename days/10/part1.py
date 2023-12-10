import sys
from pathlib import Path
from typing import NamedTuple, Self

import numpy as np
import pytest
from icecream import ic

# --> Puzzle solution


class Point(NamedTuple):
    row: int
    col: int

    def north(self) -> Self:
        return Point(self.row - 1, self.col)

    def south(self) -> Self:
        return Point(self.row + 1, self.col)

    def east(self) -> Self:
        return Point(self.row, self.col + 1)

    def west(self) -> Self:
        return Point(self.row, self.col - 1)

    def adjacent_points(self):
        yield self.north()
        yield self.east()
        yield self.south()
        yield self.west()


def connector(ch: str, ch_loc: Point) -> tuple:  # noqa: PLR0911
    match ch:
        case "|":
            return ch_loc.north(), ch_loc.south()
        case "-":
            return ch_loc.west(), ch_loc.east()
        case "L":
            return ch_loc.north(), ch_loc.east()
        case "J":
            return ch_loc.north(), ch_loc.west()
        case "7":
            return ch_loc.south(), ch_loc.west()
        case "F":
            return ch_loc.south(), ch_loc.east()
        case _:
            return ()


class Map:
    def __init__(self, input_data):
        s_location = None

        lines = input_data.splitlines()
        self.n_rows = len(lines)
        self.n_cols = len(lines[0])
        sketch = np.array([list(line) for line in lines])
        ic(sketch)

        for row, line in enumerate(lines):
            for col, ch in enumerate(line):
                if ch == "S":
                    s_location = Point(row, col)
                    break

        assert s_location is not None
        self.s_location = s_location
        self.sketch = sketch

    def valid(self, point: Point) -> bool:
        return (0 <= point.row < self.n_rows) and (0 <= point.col < self.n_cols)

    def get_starting_move(self, S) -> Point:
        """Used to find the two places that connect to given point"""

        for cand in S.adjacent_points():
            ic(cand)
            if not self.valid(cand):
                ic("not valid")
                continue

            connections = connector(self.sketch[cand.row, cand.col], cand)
            if S in connections:
                return cand
        raise Exception("oops")

    def solve(self):
        pos = self.get_starting_move(self.s_location)
        ic("starting move", pos)

        visited = {self.s_location, pos}

        while True:
            connections = connector(self.sketch[pos.row, pos.col], pos)
            assert connections is not None
            ic(pos, connections)

            if connections[0] in visited and connections[1] in visited:
                break

            if connections[0] in visited:
                pos = connections[1]
            else:
                pos = connections[0]

            ic(pos)
            assert self.valid(pos)
            visited.add(pos)

        return len(visited) // 2


def solve(input_data):
    m = Map(input_data)
    return m.solve()


# --> Test driven development helpers


# Test any examples given in the problem

sample = Path("input-sample.txt").read_text().strip()
sample2 = Path("input-sample-2.txt").read_text().strip()
EXAMPLES = [
    (sample, 4),
    (sample2, 8),
]


@pytest.mark.parametrize(
    "sample_data,sample_solution", EXAMPLES, ids=("sample", "sample2")
)
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
