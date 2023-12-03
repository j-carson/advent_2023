import re
import sys
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

    def touches(self, row: int, column: int) -> bool:
        return all(
            (
                self.row - 1 <= row <= self.row + 1,
                self.column_start - 1 <= column <= self.column_stop + 1,
            )
        )


def parse_part_numbers(line: str, row: int):
    for match in re.finditer(r"\d+", line):
        yield PartNumber(
            int(match.group()),
            row,
            match.span()[0],
            match.span()[1] - 1,
        )


def parse_symbol_locations(line: str, row: int):
    for i, ch in enumerate(line):
        if ch == "*":
            yield (row, i)


def solve(data):
    score = 0

    symbols = []
    parts = []

    for row, line in enumerate(data.splitlines()):
        symbols.extend(list(parse_symbol_locations(line, row)))
        parts.extend(list(parse_part_numbers(line, row)))

    for symbol in symbols:
        touch_parts = []
        for part in parts:
            if part.touches(*symbol):
                touch_parts.append(part)
        if len(touch_parts) == 2:
            p1, p2 = touch_parts
            score += p1.number * p2.number
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
