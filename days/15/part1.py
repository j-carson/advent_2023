import sys
from pathlib import Path

import pytest
from icecream import ic

# --> Puzzle solution


def HASH(chain):
    current_value = 0
    for ch in chain:
        current_value += ord(ch)
        current_value *= 17
        current_value = current_value % 256
    return current_value


def solve(input_data):
    result = 0
    for item in input_data.split(","):
        result += HASH(item)
    return result


# --> Test driven development helpers


# Test any examples given in the problem


EXAMPLES = [("HASH", 52)]


@pytest.mark.parametrize("chain,result", EXAMPLES)
def test_HASH(chain, result):
    assert HASH(chain) == result


my_input = Path("input-sample.txt").read_text().strip()


@pytest.mark.parametrize(
    "sample_data,sample_solution", [(my_input, 1320)], ids=("sample",)
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
