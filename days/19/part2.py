import sys
from collections import defaultdict
from functools import partial
from pathlib import Path

import pytest
from icecream import ic

# --> Puzzle solution


class WildCardPart:
    def __str__(self):
        return f"{self.x=},{self.m=},{self.a=},{self.s=}"

    def __repr__(self):
        return f"WildCardPart {self.x=},{self.m=},{self.a=},{self.s=}"

    def __init__(self, clone=None):
        if clone is not None:
            self.x = clone.x
            self.m = clone.m
            self.a = clone.a
            self.s = clone.s
        else:
            self.x = (1, 4000)
            self.m = (1, 4000)
            self.a = (1, 4000)
            self.s = (1, 4000)

    def debug(self):
        for attr in list("xmas"):
            low, high = getattr(self, attr)
            assert low < high
            assert 1 <= low <= 4000
            assert 1 <= high <= 4000

    def constrain(self, key, rule, val):
        pass_part = WildCardPart(clone=self)
        fail_part = WildCardPart(clone=self)

        key_range = getattr(self, key)

        match rule:
            case "always":
                pass_part = self
                fail_part = None
            case "gt":
                if key_range[0] <= val + 1 <= key_range[1]:
                    pass_range = val + 1, key_range[1]
                    setattr(pass_part, key, pass_range)
                    fail_range = key_range[0], val
                    setattr(fail_part, key, fail_range)
                elif key_range[1] < val:
                    pass_part = None
                    fail_part = self
                elif key_range[0] > val:
                    pass_part = self
                    fail_part = None
                else:
                    raise Exception("oops gt")
            case "lt":
                if key_range[0] <= val - 1 <= key_range[1]:
                    pass_range = key_range[0], val - 1
                    setattr(pass_part, key, pass_range)
                    fail_range = val, key_range[1]
                    setattr(fail_part, key, fail_range)
                elif key_range[1] < val:
                    pass_part = None
                    fail_part = self
                elif key_range[0] > val:
                    pass_part = self
                    fail_part = None
                else:
                    raise Exception("oops lt")

        if fail_part is not None:
            fail_part.debug()
        if pass_part is not None:
            pass_part.debug()
        return pass_part, fail_part

    def combinations(self):
        result = 1
        for attr in list("xmas"):
            low, high = getattr(self, attr)
            result *= high - low + 1
        return result


class Rule:
    def __init__(self, text):
        if ":" in text:
            rule, dest = text.split(":")
            key = rule[0]
            compare = rule[1]
            val = int(rule[2:])

            match compare:
                case "<":
                    self._apply = partial(self.less, key=key, val=val, dest=dest)
                case ">":
                    self._apply = partial(self.more, key=key, val=val, dest=dest)
        else:
            self._apply = partial(self.always, dest=text)

    def more(self, part, key, val, dest):
        return *part.constrain(key, "gt", val), dest

    def less(self, part, key, val, dest):
        return *part.constrain(key, "lt", val), dest

    def always(self, part, dest):
        return part, None, dest

    def apply(self, part):
        return self._apply(part)


class WorkFlow:
    def __init__(self, name, rules):
        self.name = name
        self.rules = rules

    def get_paths(self, part):
        result = defaultdict(list)
        for rule in self.rules:
            pass_part, fail_part, dest = rule.apply(part)
            if (pass_part is not None) and (dest != "R"):
                result[dest].append(pass_part)
            if fail_part is not None:
                part = fail_part
            else:
                break
        assert fail_part is None
        return result


def parse_workflows(data):
    workflows = {}
    for line in data.splitlines():
        name, specs = line.split("{")
        rules = specs[:-1].split(",")
        wf = WorkFlow(name, [Rule(r) for r in rules])
        workflows[name] = wf
    return workflows


def solve(input_data):
    workflows, _ = input_data.split("\n\n")
    flows = parse_workflows(workflows)
    part = WildCardPart()

    accepted = []
    workq = []
    workq.append(("in", part))

    while len(workq):
        current_flow, part = workq.pop()
        flow = flows[current_flow]
        paths = flow.get_paths(part)
        if "A" in paths:
            accepted.extend(paths["A"])
            paths.pop("A")
        for key, val in paths.items():
            for item in val:
                workq.append((key, item))

    return sum(a.combinations() for a in accepted)


# --> Test driven development helpers


# Test any examples given in the problem

sample_input = Path("input-sample.txt").read_text().strip()
EXAMPLES = [
    (sample_input, 167409079868000),
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
