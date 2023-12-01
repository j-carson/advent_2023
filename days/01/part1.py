import sys
from pathlib import Path

import pytest
from icecream import ic

# --> Puzzle solution


def solve(input_data):
    ans = 0
    for line in input_data.split("\n"):
        if not line:
            continue
        digs = [ch for ch in line if ch.isdigit()]
        score = int("".join([digs[0], digs[-1]]))
        ic(line, score)
        ans += score
    return ans


# --> Test driven development helpers


# Test any examples given in the problem

EXAMPLES = [
    (
        """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet""",
        142,
    ),
]


@pytest.mark.parametrize("sample_data,sample_solution", EXAMPLES)
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
    my_input = Path("input.txt").read_text()
    result = solve(my_input)
    print(result)
