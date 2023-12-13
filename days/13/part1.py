import sys
from pathlib import Path

import pytest
from icecream import ic

# --> Puzzle solution


def get_patterns(input_data):
    for block in input_data.split("\n\n"):
        dataset = []
        for row in block.splitlines():
            dataset.append(row)
        yield dataset


def try_row_reflection(block, split_point):
    upper_blob = block[0:split_point]
    lower_blob = block[split_point:]
    size = min(len(upper_blob), len(lower_blob))

    upper_blob = list(reversed(upper_blob))[:size]
    lower_blob = lower_blob[:size]

    for r1, r2 in zip(upper_blob, lower_blob):
        if r1 != r2:
            return -1

    return split_point


def search_reflection_row(block):
    try:
        for i, row in enumerate(block):
            if block[i + 1] == row:
                if (check := try_row_reflection(block, i + 1)) > 0:
                    return check
    except IndexError:
        return -1


def rotate_block(pat):
    block = []
    for c in range(len(pat[0])):
        block.append("".join(p[c] for p in pat))
    return block


def solve(input_data):
    score = 0
    for pat in get_patterns(input_data):
        v1 = search_reflection_row(pat)
        if v1 > 0:
            score += 100 * v1
            continue
        rot = rotate_block(pat)
        v2 = search_reflection_row(rot)
        assert v2 > 0
        score += v2
    return score


# --> Test driven development helpers


# Test any examples given in the problem

sample = Path("input-sample.txt").read_text().strip()
EXAMPLES = [(sample, 405)]


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
