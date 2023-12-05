import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

import parse as p
import pytest
from icecream import ic

# --> Puzzle solution


@dataclass
class Map:
    source: str
    dest: str
    dest_range_start: int
    source_range_start: int
    range_length: int

    def get_dest(self, source):
        if source < self.source_range_start:
            return None
        if source >= self.source_range_start + self.range_length:
            return None
        return self.dest_range_start + (source - self.source_range_start)

    @classmethod
    def from_map(cls, stanza: str):
        lines = stanza.splitlines()
        source, dest = p.parse("{}-to-{} map:", lines[0])
        for line in lines[1:]:
            dest_range_start, source_range_start, range_length = p.parse(
                "{:d} {:d} {:d}", line
            )
            m = cls(source, dest, dest_range_start, source_range_start, range_length)
            yield m


def calc_dest(source, maps):
    for m in maps:
        d = m.get_dest(source)
        if d is not None:
            return d
    return source


def solve(input_data):
    stanzas = input_data.split("\n\n")
    seeds = [int(s) for s in stanzas[0].split()[1:]]
    ic(seeds)

    sources = defaultdict(list)
    for stanza in stanzas[1:]:
        for m in Map.from_map(stanza):
            sources[m.source].append(m)

    acc = {}
    chain = [
        "seed",
        "soil",
        "fertilizer",
        "water",
        "light",
        "temperature",
        "humidity",
        "location",
    ]
    for seed in seeds:
        next_source = seed
        debug = {}
        for ch in chain:
            debug[ch] = next_source
            next_source = calc_dest(next_source, sources[ch])
        ic(debug)
        acc[seed] = next_source

    return min(acc.values())


# --> Test driven development helpers


# Test any examples given in the problem

sample = Path("input-sample.txt").read_text().strip()
EXAMPLES = [(sample, 35)]


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
