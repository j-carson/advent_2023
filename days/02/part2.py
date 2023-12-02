import sys
from collections import defaultdict
from pathlib import Path

import pytest
from icecream import ic

# --> Puzzle solution


class Game:
    def __init__(self, line):
        game, games = line.split(":")

        self.game_id = int(game.split()[-1])
        self.games = []
        for game in games.split(";"):
            cubes = game.split(",")
            game_numbers = {}
            for cube in cubes:
                count, color = cube.split()
                game_numbers[color] = int(count)
            self.games.append(game_numbers)

    def score(self):
        acc = defaultdict(int)
        for game in self.games:
            for color, value in game.items():
                acc[color] = max(value, acc[color])
        pscore = 1
        for value in acc.values():
            pscore *= value
        return pscore


def solve(input_data):
    score = 0
    for line in input_data.split("\n"):
        if line:
            score += Game(line).score()

    return score


# --> Test driven development helpers


# Test any examples given in the problem

test_data = Path("input-sample.txt").read_text().strip()

EXAMPLES = [
    (test_data, 2286),
]


@pytest.mark.parametrize("sample_data, sample_solution", EXAMPLES)
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
