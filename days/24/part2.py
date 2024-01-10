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


def line_up(
    h1: Hailstone,
    h2: Hailstone,
    h3: Hailstone,
):
    t1, t2, t3 = sympy.symbols("t1 t2 t3", negative=False)
    x, y, z, vx, vy, vz = sympy.symbols("x y z vx vy vz")

    soln = sympy.solve(
        [
            sympy.Eq(x + t1 * vx, h1.x + t1 * h1.vx),
            sympy.Eq(y + t1 * vy, h1.y + t1 * h1.vy),
            sympy.Eq(z + t1 * vz, h1.z + t1 * h1.vz),
            sympy.Eq(x + t2 * vx, h2.x + t2 * h2.vx),
            sympy.Eq(y + t2 * vy, h2.y + t2 * h2.vy),
            sympy.Eq(z + t2 * vz, h2.z + t2 * h2.vz),
            sympy.Eq(x + t3 * vx, h3.x + t3 * h3.vx),
            sympy.Eq(y + t3 * vy, h3.y + t3 * h3.vy),
            sympy.Eq(z + t3 * vz, h3.z + t3 * h3.vz),
        ]
    )

    return soln[0][x] + soln[0][y] + soln[0][z]


def solve(input_data):
    stones = [Hailstone.from_line(line) for line in input_data.splitlines()]
    return line_up(*stones[:3])


# --> Test driven development helpers


# Test any examples given in the problem

sample_input = Path("input-sample.txt").read_text().strip()
EXAMPLES = [
    (sample_input, 47),
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
