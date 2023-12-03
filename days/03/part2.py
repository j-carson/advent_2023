import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

import pytest
from icecream import ic

# --> Puzzle solution


@dataclass
class PartNumber:
    number: int
    row: int
    column_start: int
    column_stop: int

    def id_(self):
        return (self.number, self.row, self.column_start)


@dataclass
class Symbol:
    row: int
    column: int
    triggers: set = field(default_factory=set)

    def trigger(self, part):
        self.triggers.add(part.id_())


def parse_part_numbers(line: str, row: int):
    parts = []
    for match in re.finditer(r"\d+", line):
        parts.append(
            PartNumber(
                int(match.group()),
                row,
                match.span()[0],
                match.span()[1] - 1,
            )
        )
    return parts


def parse_symbol_locations(line: str, row: int):
    for i, ch in enumerate(line):
        if ch == "*":
            yield Symbol(row, i)


def solve(data):
    score = 0

    parts = defaultdict(list)
    for i, line in enumerate(data.split("\n")):
        parts[i] = parse_part_numbers(line, i)

    for row, line in enumerate(data.split("\n")):
        locations = list(parse_symbol_locations(line, row))
        for location in locations:
            for check_row in range(row - 1, row + 2):
                for check_column in range(location.column - 1, location.column + 2):
                    for part in parts[check_row]:
                        if part.column_start <= check_column <= part.column_stop:
                            location.trigger(part)

            if len(location.triggers) == 2:
                ic(location.row, location.column, location.triggers)
                nums = [t[0] for t in location.triggers]
                score += nums[0] * nums[1]

    return score


# --> Test driven development helpers


# Test any examples given in the problem

sample = Path("input-sample.txt").read_text().strip()
EXAMPLES = [
    (sample, 467835),
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
