import sys
from collections import Counter, defaultdict
from pathlib import Path

import pytest
from icecream import ic

# --> Puzzle solution

CARD_VALUES = {c: i for i, c in enumerate(list(reversed("AKQT98765432J")))}
HAND_RANKS = {
    c: i for i, c in enumerate(list(reversed(["5", "4", "H", "3", "22", "2", "1"])))
}


class Card:
    def __init__(self, ch):
        self.ch = ch

    def __lt__(self, other):
        return CARD_VALUES[self.ch] < CARD_VALUES[other.ch]

    def __gt__(self, other):
        return CARD_VALUES[self.ch] > CARD_VALUES[other.ch]

    def __eq__(self, other):
        return CARD_VALUES[self.ch] == CARD_VALUES[other.ch]


class Hand:
    def __init__(self, input_text):
        hand, value = input_text.split()

        self.cards = list(hand)
        self.card_to_count = Counter(self.cards)
        self.bid = int(value)

        self.count_to_cards = defaultdict(list)
        for key, value in self.card_to_count.items():
            self.count_to_cards[value].append(key)

        if 5 in self.count_to_cards:
            self.hand = "5"
            self.hand_rank = HAND_RANKS["5"]
        elif 4 in self.count_to_cards:
            self.hand = "4"
            self.hand_rank = HAND_RANKS["4"]
        elif 3 in self.count_to_cards and 2 in self.count_to_cards:
            self.hand = "H"
            self.hand_rank = HAND_RANKS["H"]
        elif 3 in self.count_to_cards:
            self.hand = "3"
            self.hand_rank = HAND_RANKS["3"]
        elif 2 in self.count_to_cards and len(self.count_to_cards[2]) == 2:
            self.hand = "22"
            self.hand_rank = HAND_RANKS["22"]
        elif 2 in self.count_to_cards:
            self.hand = "2"
            self.hand_rank = HAND_RANKS["2"]
        else:
            self.hand = "1"
            self.hand_rank = HAND_RANKS["1"]

        ic(hand, self.hand, self.hand_rank)

        if "J" in self.cards:
            self.joker()

        ic(hand, self.hand_rank, HAND_RANKS[self.hand])

    def joker(self):
        # all jokers, nothing can be substituted to get more cards
        if all(ch == "J" for ch in self.cards):
            return

        non_joker_cards = [ch for ch in self.cards if ch != "J"]
        non_joker_card_to_count = Counter(non_joker_cards)
        non_joker_count_to_card = defaultdict(list)
        for key, value in non_joker_card_to_count.items():
            non_joker_count_to_card[value].append(key)

        max_count = max(non_joker_count_to_card.keys())
        card_objs = [Card(ch) for ch in non_joker_count_to_card[max_count]]
        highest_card = max(card_objs)
        real_hand = "".join(self.cards)
        fake_hand = real_hand.replace("J", highest_card.ch)
        fake_card = Hand(f"{fake_hand} 0")
        self.hand_rank = fake_card.hand_rank
        ic(real_hand, fake_hand)

    def __lt__(self, other):
        if self.hand_rank < other.hand_rank:
            result = True
        elif self.hand_rank > other.hand_rank:
            result = False
        elif self.hand_rank == other.hand_rank:
            for c1, c2 in zip(self.cards, other.cards):
                if CARD_VALUES[c1] < CARD_VALUES[c2]:
                    result = True
                    break
                if CARD_VALUES[c1] > CARD_VALUES[c2]:
                    result = False
                    break
        if result:
            s = "lt"
        else:
            s = "gt"
        ic(self.cards, s, other.cards)
        return result

    def __gt__(self, other):
        return other.__lt__(self)


def solve(input_data):
    hands = sorted([Hand(row) for row in input_data.splitlines()])
    score = 0
    for rank, hand in enumerate(hands, start=1):
        ic(rank, hand.cards)
        score += hand.bid * rank
    return score


# --> Test driven development helpers


# Test any examples given in the problem

sample = Path("input-sample.txt").read_text().strip()
EXAMPLES = [
    (sample, 5905),
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
