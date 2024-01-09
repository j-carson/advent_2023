import sys
from pathlib import Path
from typing import NamedTuple

import parse as p
import pytest
import sympy
from icecream import ic

# --> Puzzle solution


class Hailstone(NamedTuple):
    x: int
    y: int
    z: int
    vx: int
    vy: int
    vz: int

    @classmethod
    def from_line(cls, line):
        args = p.parse("{:d}, {:d}, {:d} @ {:d}, {:d}, {:d}", line)
        return cls(*args)


def intersect(h1: Hailstone, h2: Hailstone, xmin: int, xmax: int, ymin: int, ymax: int):
    xi, yi, t1, t2 = sympy.symbols("xi yi t1 t2")
    result = sympy.solve(
        [
            sympy.Eq(xi, h1.x + t1 * h1.vx),
            sympy.Eq(xi, h2.x + t2 * h2.vx),
            sympy.Eq(yi, h1.y + t1 * h1.vy),
            sympy.Eq(yi, h2.y + t2 * h2.vy),
        ]
    )

    if not len(result):
        return False

    return all(
        (
            result[t1] >= 0,
            result[t2] >= 0,
            xmin <= result[xi] <= xmax,
            ymin <= result[yi] <= ymax,
        )
    )


def solve(input_data, xmin, xmax, ymin, ymax):
    stones = [Hailstone.from_line(line) for line in input_data.splitlines()]
    n_stones = len(stones)

    score = 0
    for i in range(n_stones):
        for j in range(i + 1, n_stones):
            score += intersect(
                stones[i],
                stones[j],
                xmin,
                xmax,
                ymin,
                ymax,
            )
    return score


# --> Test driven development helpers


# Test any examples given in the problem

sample_input = Path("input-sample.txt").read_text().strip()
EXAMPLES = [
    (sample_input, 2),
]


@pytest.mark.parametrize("sample_data,sample_solution", EXAMPLES, ids=("sample",))
def test_samples(sample_data, sample_solution) -> None:
    assert solve(sample_data, 7, 27, 7, 27) == sample_solution


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
    result = solve(
        my_input,
        200000000000000,
        400000000000000,
        200000000000000,
        400000000000000,
    )
    print(result)
