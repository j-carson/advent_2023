import sys
from functools import partial
from pathlib import Path

import parse as p
import pytest
from icecream import ic

# --> Puzzle solution


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
        if part[key] > val:
            return dest
        return None

    def less(self, part, key, val, dest):
        if part[key] < val:
            return dest
        return None

    def always(self, _, dest):
        return dest

    def apply(self, part):
        return self._apply(part)


class WorkFlow:
    def __init__(self, name, rules):
        self.name = name
        self.rules = rules

    def check(self, part):
        for rule in self.rules:
            dest = rule.apply(part)
            if dest is not None:
                return dest
        raise Exception("oops")


def parse_workflows(data):
    workflows = {}
    for line in data.splitlines():
        name, specs = line.split("{")
        rules = specs[:-1].split(",")
        wf = WorkFlow(name, [Rule(r) for r in rules])
        workflows[name] = wf
    return workflows


def parse_parts(parts):
    result = []
    for line in parts.splitlines():
        part = {}
        items = line[1:-1].split(",")
        for item in items:
            let, val = p.parse("{}={:d}", item)
            part[let] = val
        ic(part)
        result.append(part)
    return result


def solve(input_data):
    workflows, items = input_data.split("\n\n")
    flows = parse_workflows(workflows)
    parts = parse_parts(items)
    score = 0

    for part in parts:
        flow = flows["in"]
        while True:
            dest = flow.check(part)
            match dest:
                case "R":
                    break
                case "A":
                    score += sum(part.values())
                    break
                case somewhere:
                    flow = flows[somewhere]
    return score


# --> Test driven development helpers


# Test any examples given in the problem

sample_input = Path("input-sample.txt").read_text().strip()
EXAMPLES = [
    (sample_input, 19114),
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
