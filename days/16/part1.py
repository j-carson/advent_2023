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


class MirrorPuzzle:
    def __init__(self, mirrors):
        self.mirrors = mirrors
        self.energized = np.zeros_like(mirrors, dtype=bool)
        self.visited = set()
        self.workq = []

    def check_in_bounds(self, row, col):
        n_row, n_col = self.mirrors.shape
        return (0 <= row < n_row) and (0 <= col < n_col)

    def solve(self):
        self.workq.append((Point(0, -1), "east"))

        while len(self.workq):
            self.take_step(*self.workq.pop())

        return np.sum(self.energized)

    def take_step(self, pos, direction_of_travel):
        get_step = getattr(pos, direction_of_travel)
        new_pos = get_step()
        if not self.check_in_bounds(*new_pos):
            return

        if (new_pos, direction_of_travel) in self.visited:
            return

        self.energized[*new_pos] = True
        self.visited.add((new_pos, direction_of_travel))

        match (direction_of_travel, self.mirrors[new_pos]):
            case "north", "\\":
                self.workq.append((new_pos, "west"))

            case "south", "\\":
                self.workq.append((new_pos, "east"))

            case "east", "\\":
                self.workq.append((new_pos, "south"))

            case "west", "\\":
                self.workq.append((new_pos, "north"))

            case "north", "/":
                self.workq.append((new_pos, "east"))

            case "south", "/":
                self.workq.append((new_pos, "west"))

            case "east", "/":
                self.workq.append((new_pos, "north"))

            case "west", "/":
                self.workq.append((new_pos, "south"))

            case ("north", "|") | ("south", "|"):
                self.workq.append((new_pos, direction_of_travel))

            case ("east", "|") | ("west", "|"):
                self.workq.append((new_pos, "north"))
                self.workq.append((new_pos, "south"))

            case ("north", "-") | ("south", "-"):
                self.workq.append((new_pos, "east"))
                self.workq.append((new_pos, "west"))

            case ("east", "-") | ("west", "-"):
                self.workq.append((new_pos, direction_of_travel))

            case _, ".":
                self.workq.append((new_pos, direction_of_travel))

            case _:
                raise Exception("oops!")


def solve(my_input):
    mirrors = np.array([list(row) for row in my_input.splitlines()])
    return MirrorPuzzle(mirrors).solve()


# --> Test driven development helpers


# Test any examples given in the problem

sample = Path("input-sample.txt").read_text().strip()
EXAMPLES = [(sample, 46)]


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
