import sys
from dataclasses import dataclass, field
from pathlib import Path

import pytest
from icecream import ic

# --> Puzzle solution


@dataclass
class Card:
    id_: int
    numbers: set[int] = field(default_factory=set)
    winning_numbers: set[int] = field(default_factory=set)
    n_copies = 1

    @classmethod
    def from_line(cls, line: str):
        card_id, cards = line.split(":")

        my_card, winning_card = cards.split("|")
        id_ = int(card_id.split()[1])
        numbers = {int(i) for i in my_card.split()}
        winning_numbers = {int(i) for i in winning_card.split()}
        return cls(id_, numbers, winning_numbers)

    @property
    def n_matches(self):
        return len(self.numbers.intersection(self.winning_numbers))


def solve(input_data):
    cards = [Card.from_line(line) for line in input_data.splitlines()]

    for i, card in enumerate(cards):
        remaining_list = cards[i + 1 :]
        for j in range(cards[i].n_matches):
            remaining_list[j].n_copies += card.n_copies

    for c in cards:
        ic(c.id_, c.n_copies)

    return sum(c.n_copies for c in cards)


# --> Test driven development helpers


# Test any examples given in the problem

sample = Path("input-sample.txt").read_text().strip()
EXAMPLES = [(sample, 30)]


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
