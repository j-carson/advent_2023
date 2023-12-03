import re
import sys
from collections import defaultdict
from dataclasses import dataclass
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
    counted: bool = False

    def id_(self):
        return (self.number, self.row, self.column_start)


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


def parse_symbol_locations(line: str):
    for i, ch in enumerate(line):
        if ch not in ".1234567890":
            yield i


def solve(data):
    rows = data.split("\n")

    parts = defaultdict(list)
    for i, line in enumerate(data.split("\n")):
        parts[i] = parse_part_numbers(line, i)
        ic(rows[i], parts[i])

    triggers = defaultdict(set)
    for row, line in enumerate(data.split("\n")):
        locations = list(parse_symbol_locations(line))
        for location in locations:
            triggers[row].add(location - 1)
            triggers[row].add(location + 1)

            triggers[row - 1].add(location - 1)
            triggers[row - 1].add(location)
            triggers[row - 1].add(location + 1)

            triggers[row + 1].add(location - 1)
            triggers[row + 1].add(location)
            triggers[row + 1].add(location + 1)

    parts_that_count = set()
    for row, locations in triggers.items():
        ic(row, triggers)
        for location in locations:
            for part in parts[row]:
                if part.column_start <= location <= part.column_stop:
                    part.counted = True
                    parts_that_count.add(part.id_())

    score = 0
    for item in parts_that_count:
        score += item[0]

    for row, partlist in parts.items():
        for p in partlist:
            if not p.counted:
                ic(p)

    return score


# --> Test driven development helpers


# Test any examples given in the problem

sample = Path("input-sample.txt").read_text().strip()
EXAMPLES = [
    (sample, 4361),
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
