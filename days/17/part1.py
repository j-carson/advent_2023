import heapq
import sys
from pathlib import Path
from typing import NamedTuple, Self

import numpy as np
import pytest
from icecream import ic

# --> Puzzle solution

DIRECTIONS = ["south", "east", "north", "west"]
REVERSE_DIRECTIONS = {
    "south": "north",
    "north": "south",
    "east": "west",
    "west": "east",
}


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

    def go(self, direction) -> Self:
        take_step = getattr(self, direction)
        return take_step()


class RecentPath:
    def __init__(self, *args):
        if len(args):
            arg = args[0]
            assert isinstance(arg, RecentPath)
            self.direction = arg.direction
            self.count = arg.count
        else:
            self.direction = None
            self.count = 0

    def update(self, direction):
        if self.direction == direction:
            self.count += 1
        else:
            self.direction = direction
            self.count = 1

    def must_turn(self):
        assert 1 <= self.count <= 3
        return self.count == 3


class Map:
    def __init__(self, data):
        ic(data)
        self.data = data
        # assume worst case scenario is visiting every square
        self.score_to_beat = np.sum(data)
        self.n_row, self.n_col = data.shape
        self.goal = Point(self.n_row - 1, self.n_col - 1)
        self.visisted = set()

    def __getitem__(self, pos: Point):
        return self.data[pos]

    def in_bounds(self, point: Point):
        return (0 <= point.row < self.n_row) and (0 <= point.col < self.n_col)

    def move_options(self, path: "WorkPath"):
        """Return all possible legal moves for given path"""

        pos = path.current_pos
        history = path.recent_path

        for direction in DIRECTIONS:
            # check for reverse direction
            if direction == REVERSE_DIRECTIONS[history.direction]:
                continue

            # check for can't go the same way 4 times
            if (direction == history.direction) and history.must_turn():
                continue

            # check for going off the edge
            proposed = pos.go(direction)
            if not self.in_bounds(proposed):
                continue

            yield direction

    def visitable(self, pos: Point, direction: str, count: int) -> bool:
        cache_key = (*pos, direction, count)
        if cache_key in self.visisted:
            return False
        self.visisted.add(cache_key)
        return True


class WorkPath:
    def __init__(self, *args):
        """Need to specify either a Map for new path to follow,
        or an existing WorkPath to clone"""

        if len(args) != 1:
            raise ValueError(str(args))
        arg = args[0]

        if isinstance(arg, Map):
            self.map = arg
            self.recent_path = RecentPath()
            self.current_pos = Point(0, 0)
            self.score = 0
            self.abort = False
        elif isinstance(arg, WorkPath):
            self.map = arg.map
            self.recent_path = RecentPath(arg.recent_path)
            self.current_pos = arg.current_pos
            self.score = arg.score
            self.abort = False
        else:
            raise ValueError(f"{type(arg)}")

    @property
    def sortable(self):
        return (self.score, sum(self.current_pos))

    def __lt__(self, other):
        return self.sortable < other.sortable

    def find_steps(self):
        yield from self.map.move_options(self)

    def take_step(self, direction):
        self.current_pos = self.current_pos.go(direction)
        self.score += self.map[self.current_pos]
        self.recent_path.update(direction)
        self.abort = not self.map.visitable(
            self.current_pos, direction, self.recent_path.count
        )

    @property
    def done(self):
        return self.current_pos == self.map.goal


class ScoreKeeper:
    def __init__(self, map):
        self.map = map
        self.workq = []

        # Create first two jobs by hand to fill in their "history" field
        first_job = WorkPath(map)
        first_job.take_step("east")
        second_job = WorkPath(map)
        second_job.take_step("south")

        heapq.heappush(self.workq, (first_job.sortable, first_job))
        heapq.heappush(self.workq, (second_job.sortable, second_job))

    def solve(self):
        while len(self.workq):
            _, item = heapq.heappop(self.workq)
            for direction in item.find_steps():
                clone = WorkPath(item)
                clone.take_step(direction)
                if clone.done:
                    return clone.score
                if not clone.abort:
                    heapq.heappush(self.workq, (clone.sortable, clone))
        raise Exception("oops!")


def parse(input_data):
    return np.array([[int(r) for r in list(row)] for row in input_data.splitlines()])


def solve(input_data):
    map = Map(parse(input_data))
    keeper = ScoreKeeper(map)
    return keeper.solve()


# --> Test driven development helpers


# Test any examples given in the problem

sample_input = Path("input-sample.txt").read_text().strip()
EXAMPLES = [
    (sample_input, 102),
]


@pytest.mark.parametrize("sample_data,sample_solution", EXAMPLES, ids=("sample",))
def test_samples(sample_data, sample_solution) -> None:
    assert solve(sample_data) == sample_solution


# --> Setup and run

if __name__ == "__main__":
    #  Run the test examples with icecream debug-trace turned on
    ic.enable()
    ex = pytest.main(
        [
            __file__,
            "--capture=tee-sys",
            "-v",
        ]
    )
    if ex not in {pytest.ExitCode.OK, pytest.ExitCode.NO_TESTS_COLLECTED}:
        print(f"tests FAILED ({ex})")
        sys.exit(1)
    else:
        print("tests PASSED")

    #  Actual input data generally has more iterations, turn off log
    my_input = Path("input.txt").read_text().strip()
    result = solve(my_input)
    print(result)
