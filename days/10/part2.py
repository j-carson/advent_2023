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

    def get_starting_move(self, S):
        """Used to find the two places that connect to given point"""

        ok = []
        for cand in S.adjacent_points():
            if not self.valid(cand):
                continue

            connections = connector(self.sketch[cand.row, cand.col], cand)
            if S in connections:
                ok.append(cand)

        assert len(ok) == 2
        return ok[0]

    def solve_1(self):
        pos = self.get_starting_move(self.s_location)
        self.visited = [self.s_location, pos]

        while True:
            connections = connector(self.sketch[pos.row, pos.col], pos)
            assert connections is not None

            if connections[0] in self.visited and connections[1] in self.visited:
                break

            if connections[0] in self.visited:
                pos = connections[1]
            else:
                pos = connections[0]

            assert self.valid(pos)
            self.visited.append(pos)
        return len(self.visited) // 2

    def solve_2(self):
        self.solve_1()

        # Shoelace formula to give area enclosed
        # https://en.wikipedia.org/wiki/Shoelace_formula

        xs = [p.row for p in self.visited]
        ys = [p.col for p in self.visited]
        x_shift = xs[1:] + [xs[0]]
        y_shift = ys[1:] + [ys[0]]

        adds = sum(x * y for (x, y) in zip(xs, y_shift))
        subtracts = sum(x * y for (x, y) in zip(x_shift, ys))
        area = abs(adds - subtracts) / 2

        # Pick's theorm
        # https://en.wikipedia.org/wiki/Pick%27s_theorem
        # > area = interior + (borders/2) - 1
        # > interior = area - (borders/2) + 1

        borders = len(self.visited)
        return area - borders / 2 + 1


def solve(input_data):
    m = Map(input_data)
    return m.solve_2()


# --> Test driven development helpers


# Test any examples given in the problem

sample3 = Path("input-sample-3.txt").read_text().strip()
sample4 = Path("input-sample-4.txt").read_text().strip()
EXAMPLES = [
    (sample4, 8),
    (sample3, 10),
]


@pytest.mark.parametrize(
    "sample_data,sample_solution", EXAMPLES, ids=("first", "second")
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
