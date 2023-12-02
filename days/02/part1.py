import sys
from collections import defaultdict
from pathlib import Path

import parse as p
import pytest
from icecream import ic

# --> Puzzle solution


class Game:
    def __init__(self, line):
        self.game_id, rest_of_line = p.parse("Game {:d}: {}", line)

        self.trials = []
        for trial in rest_of_line.split(";"):
            cubes = trial.split(",")
            cube_counts = defaultdict(int)
            for cube in cubes:
                count, color = p.parse("{:d} {}", cube)
                cube_counts[color] = count
            self.trials.append(cube_counts)

    def possible(self, cube_counts):
        for color, count in cube_counts.items():
            for game in self.trials:
                if game[color] > count:
                    ic("impossible", cube_counts, game)
                    return False

        ic("possible", cube_counts, self.trials)
        return True


def solve(input_data, check_vs):
    score = 0
    for line in input_data.split("\n"):
        if line:
            game = Game(line)
            if game.possible(check_vs):
                score += game.game_id

    return score


# --> Test driven development helpers


# Test any examples given in the problem

test_data = Path("input-sample.txt").read_text().strip()
cubeset = {"red": 12, "green": 13, "blue": 14}

EXAMPLES = [
    (test_data, cubeset, 8),
]


@pytest.mark.parametrize("sample_data, cubeset, sample_solution", EXAMPLES)
def test_samples(sample_data, cubeset, sample_solution) -> None:
    assert solve(sample_data, cubeset) == sample_solution


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
    result = solve(my_input, cubeset)
    print(result)
