from collections import deque
from itertools import count
from math import lcm
from pathlib import Path
from typing import Any, NamedTuple

from icecream import ic

# --> Puzzle solution


class QItem(NamedTuple):
    high_pulse: bool
    source: Any
    dest: Any


class WorkQ:
    def __init__(self):
        self.q = deque()
        self.high_count = 0
        self.low_count = 0
        self.button_press = 0

    def append(self, item: QItem):
        self.q.append(item)
        if item.source is None:
            self.button_press += 1
        if item.high_pulse:
            self.high_count += 1
        else:
            self.low_count += 1

    def pop(self):
        item = self.q.popleft()
        item.dest.recv_pulse(item.source, item.high_pulse, self)

    def drain(self):
        while len(self.q):
            self.pop()


class Broadcaster:
    def __init__(self):
        self.dests = []
        self.name = "broadcaster"

    def recv_pulse(self, source, high_pulse, q):
        for d in self.dests:
            q.append(QItem(high_pulse, self, d))


class FlipFlop:
    def __init__(self, name):
        self.is_on = False
        self.name = name
        self.dests = []

    def recv_pulse(self, source, high_pulse, q):
        if high_pulse:
            return
        # low pulse
        self.is_on = not self.is_on
        new_pulse = self.is_on
        for d in self.dests:
            q.append(QItem(new_pulse, self, d))


class Conjunction:
    def __init__(self, name):
        self.name = name
        self.dests = []
        self.memory = {}
        self.flip_point = 0

    def set_inputs(self, inputs):
        for i in inputs:
            self.memory[i] = False

    def recv_pulse(self, source, high_pulse, q):
        self.memory[source.name] = high_pulse
        if all(self.memory.values()):
            new_pulse = False
        else:
            new_pulse = True
            if not self.flip_point:
                self.flip_point = q.button_press

        for d in self.dests:
            q.append(QItem(new_pulse, self, d))


class Output:
    def __init__(self, name):
        self.name = name
        self.dests = []

    def recv_pulse(self, source, high_pulse, q):
        pass


def parse(input_data):
    q = WorkQ()
    network = {}
    for line in input_data.splitlines():
        source, _ = line.split("->")
        source = source.strip()
        network["broadcaster"] = Broadcaster()
        network["rx"] = Output("rx")
        if source not in {"output", "broadcaster"}:
            name = source[1:]
            match source[0]:
                case "%":
                    network[name] = FlipFlop(name)
                case "&":
                    network[name] = Conjunction(name)
                case _:
                    raise Exception("whut?")

    for line in input_data.splitlines():
        name, dests = line.split("->")
        name = name.strip()
        if name == "broadcaster":
            source = network[name]
        else:
            source = network[name[1:]]
        source.dests = [network[dname.strip()] for dname in dests.split(",")]

    for name, node in network.items():
        if isinstance(node, Conjunction):
            sources = []
            for name2, node2 in network.items():
                if node in node2.dests:
                    sources.append(name2)
            node.set_inputs(sources)

    return network, q


def solve(input_data):
    network, q = parse(input_data)
    rx_feeders = ["xn", "qn", "xf", "zl"]
    feeders = [network[name] for name in rx_feeders]

    for it in count(1):
        q.append(QItem(False, None, network["broadcaster"]))
        q.drain()
        if all(feeder.flip_point for feeder in feeders):
            break

    cycle_times = [f.flip_point for f in feeders]
    return lcm(*cycle_times)


# --> Setup and run

if __name__ == "__main__":
    #  Run the test examples with icecream debug-trace turned on
    #  Actual input data generally has more iterations, turn off log
    ic.disable()
    my_input = Path("input.txt").read_text().strip()
    result = solve(my_input)
    print(result)
