from pathlib import Path

# --> Puzzle solution


class StateMachine:
    def __init__(self):
        self.cache = {}

    @classmethod
    def from_line(cls, line):
        status, counts = line.split()
        goal = tuple(int(c) for c in counts.split(","))

        status = "?".join([status for _ in range(5)])
        goal = goal * 5

        instance = cls()
        return instance.solve(status, 0, goal)

    def solve(self, remaining_chain, current_group, remaining_groups):
        if (remaining_chain, current_group, remaining_groups) in self.cache:
            return self.cache[remaining_chain, current_group, remaining_groups]

        self.cache[
            remaining_chain, current_group, remaining_groups
        ] = self.count_solutions(remaining_chain, current_group, remaining_groups)
        return self.cache[remaining_chain, current_group, remaining_groups]

    def count_solutions(
        self,
        remaining_chain,
        current_group,
        remaining_groups,
    ):
        ch = remaining_chain[0]
        remaining = remaining_chain[1:]

        match ch:
            case "#":
                # must add to current group
                current_group += 1
                if len(remaining_groups):
                    if current_group > remaining_groups[0]:
                        # Ooops! bucket overflow!
                        return 0
                else:
                    # Ooops! no more buckets!
                    return 0

            case ".":
                # must start a new group, unless we're already at zero
                # then we haven't really started a new group yet
                if current_group != 0:
                    if current_group != remaining_groups[0]:
                        # Oops wrong size!  Just stop!
                        return 0
                    # reset the group size counter for the new group
                    current_group = 0
                    remaining_groups = remaining_groups[1:]
                    if len(remaining_groups) == 0:
                        # if we ran out of buckets and have hashtags left, we are done
                        if "#" in remaining:
                            return 0

            case "?":
                if current_group > 0:
                    if current_group < remaining_groups[0]:
                        # must not start a new group, current bucket is not full
                        # treat as '#'
                        return self.solve(
                            "#" + remaining, current_group, remaining_groups
                        )

                    if current_group == remaining_groups[0]:
                        # must end current group, current bucket is full
                        # treat as '.'
                        return self.solve(
                            "." + remaining, current_group, remaining_groups
                        )
                    else:
                        raise Exception("ooops! Illegal state!")

                # no clever tricks here... just need to try both paths
                return self.solve(
                    "#" + remaining, current_group, remaining_groups
                ) + self.solve("." + remaining, current_group, remaining_groups)

        if len(remaining):
            # enqueue the next character...
            return self.solve(remaining, current_group, remaining_groups)

        # we ran out of string!
        # better have finished all groups
        if len(remaining_groups) == 1:
            if current_group == remaining_groups[0]:
                return 1
        elif len(remaining_groups) == 0:
            if current_group == 0:
                return 1

        return 0


def solve(input_data):
    solution = 0

    for line in input_data.splitlines():
        solution += StateMachine.from_line(line)

    return solution


if __name__ == "__main__":
    my_input = Path("input.txt").read_text().strip()
    result = solve(my_input)
    print(result)
