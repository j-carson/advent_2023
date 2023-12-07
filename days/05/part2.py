import sys
from dataclasses import dataclass
from itertools import pairwise
from pathlib import Path

import parse as p
import pytest
from icecream import ic


# --> Puzzle solution
class Interval:
    def __repr__(self):
        if self.offset is not None:
            return f"Interval(start={self.start},stop={self.stop},length={self.length},offset={self.offset})"
        return f"Interval(start={self.start},stop={self.stop},length={self.length})"

    def __init__(
        self,
        start: int,
        stop: int | None,
        length: int | None,
        offset: int | None = None,
    ):
        self.start = start
        self.stop = stop
        self.length = length
        self.offset = offset

        if self.stop is None:
            assert self.length is not None
            self.stop = self.start + self.length - 1
        if self.length is None:
            assert self.stop is not None
            self.length = self.stop - self.start + 1

    def contains(self, val: int):
        return self.start <= val <= self.stop

    def overlap(self, other):
        assert self.contains(other.start)

        if self.contains(other.stop):
            return other, None

        assert other.stop > self.stop

        return (
            Interval(start=other.start, stop=self.stop, length=None),
            Interval(start=self.stop + 1, stop=other.stop, length=None),
        )


@dataclass
class FancyMap:
    source: str
    dest: str
    offsets: dict[tuple[int, int], Interval]

    def get_dest_ranges(self, source_interval):
        # we need to do the tuples in order now

        keys = sorted(self.offsets.keys())
        for key in keys:
            if key[0] <= source_interval.start <= key[1]:
                i = self.offsets[key]
                matched, source_interval = i.overlap(source_interval)

                matched.start += i.offset
                matched.stop += i.offset
                yield matched

                if source_interval is not None:
                    yield from self.get_dest_ranges(source_interval)
                return

        # fell off end is offset 0
        yield source_interval

    @classmethod
    def from_stanza(cls, stanza: str):
        lines = stanza.splitlines()
        source, dest = p.parse("{}-to-{} map:", lines[0])
        offsets = {}
        for line in lines[1:]:
            dest_range_start, source_range_start, range_length = p.parse(
                "{:d} {:d} {:d}", line
            )
            i = Interval(
                source_range_start,
                stop=None,
                length=range_length,
                offset=dest_range_start - source_range_start,
            )
            offsets[(i.start, i.stop)] = i

        keys = sorted(offsets.keys())
        offsets[(-1, keys[0][0] - 1)] = Interval(
            start=-1, stop=keys[0][0] - 1, length=None, offset=0
        )
        for prev_key, next_key in pairwise(keys):
            if prev_key[1] + 1 < next_key[0] - 1:
                offsets[(prev_key[1] + 1, next_key[0] - 1)] = Interval(
                    start=prev_key[1] + 1, stop=next_key[0] - 1, length=None, offset=0
                )

        m = cls(source, dest, offsets)
        ic(m)
        return m


def batch2(s):
    if not s:
        return
    yield s[0], s[1]
    yield from batch2(s[2:])


def solve(input_data):
    stanzas = input_data.split("\n\n")
    seeds = [int(s) for s in stanzas[0].split()[1:]]
    ic(seeds)

    source_intervals = []
    for start, length in batch2(seeds):
        source_intervals.append(Interval(start=start, stop=None, length=length))

    sources = {}
    for stanza in stanzas[1:]:
        m = FancyMap.from_stanza(stanza)
        sources[m.source] = m

    chain = ["seed", "soil", "fertilizer", "water", "light", "temperature", "humidity"]

    for ch in chain:
        dest_intervals: list[Interval] = []
        for source_interval in source_intervals:
            dest_intervals.extend(list(sources[ch].get_dest_ranges(source_interval)))
        source_intervals = dest_intervals

    ic(dest_intervals)
    return min(d.start for d in dest_intervals)


# --> Test driven development helpers


# Test any examples given in the problem

sample = Path("input-sample.txt").read_text().strip()
EXAMPLES = [(sample, 46)]


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
