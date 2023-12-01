import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from icecream import ic

# --> Puzzle solution


def solve(input_data):
    return 0


# --> Test driven development helpers


# Test any examples given in the problem


@pytest.mark.parametrize("sample_data,sample_solution", [("first_example", 0)])
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