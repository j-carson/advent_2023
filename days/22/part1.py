from itertools import product
from pathlib import Path
from typing import NamedTuple

import matplotlib.pyplot as plt
import numpy as np
import parse as p
from icecream import ic
from tqdm import tqdm


class Occupied(Exception):
    """Used to debug if I put two bricks in the same square"""

    pass


class Unstable(Exception):
    """Used to run the "land bricks" function without changing any bricks"""

    pass


class XYZ(NamedTuple):
    x: int
    y: int
    z: int


class Brick:
    def __init__(self, x0, y0, z0, x1, y1, z1):
        self.end1 = XYZ(x0, y0, z0)
        self.end2 = XYZ(x1, y1, z1)
        self.freeze = False

    @classmethod
    def from_line(cls, line: str):
        args = p.parse("{:d},{:d},{:d}~{:d},{:d},{:d}", line)
        return cls(*args)

    def __repr__(self):
        return f"Brick({self.end1},{self.end2})"

    def range(self, dimension: str):
        ranges = []
        for dim in list(dimension):
            i0 = getattr(self.end1, dim)
            i1 = getattr(self.end2, dim)
            ordered = sorted((i0, i1))
            ranges.append(range(ordered[0], ordered[1] + 1))
        return product(*ranges)

    def min(self, dim: str):
        return min(getattr(self.end1, dim), getattr(self.end2, dim))

    def max(self, dim: str):
        return max(getattr(self.end1, dim), getattr(self.end2, dim))

    def fill_space(self, zlevel: int, space):
        # "self" has no overlap with zlevel, nothing to add to this space
        low = self.min("z")
        high = self.max("z")
        if not (low <= zlevel <= high):
            return

        for xy in self.range("xy"):
            if xy in space:
                raise Occupied(f"Point ({xy}) is already occupied")
            space.add(xy)

    def fall(self, zlevel: int):
        assert zlevel >= 1

        z_min = self.min("z")
        assert z_min >= zlevel, "Trying to fall upwards"

        if z_min == zlevel:
            return
        if self.freeze:
            raise Unstable

        delta_z = z_min - zlevel
        self.end1 = XYZ(self.end1.x, self.end1.y, self.end1.z - delta_z)
        self.end2 = XYZ(self.end2.x, self.end2.y, self.end2.z - delta_z)


def brick_viewer(bricks: list[Brick]):
    fig = plt.figure()
    ax = fig.add_subplot(projection="3d")
    dims = [max(brick.max(dim) for brick in bricks) + 1 for dim in list("xyz")]
    ic(dims)

    voxels = np.zeros(dims, dtype=bool)
    colors = np.empty(dims, dtype="O")
    colors[:, :, :] = ""

    for idx, brick in enumerate(bricks):
        color = f"C{idx}"
        for xyz in brick.range("xyz"):
            voxels[xyz] = True
            colors[xyz] = color

    ax.voxels(filled=voxels, facecolors=colors)
    return fig


def load_bricks(input_data: str) -> list[Brick]:
    return [Brick.from_line(line) for line in input_data.splitlines()]


def land_bricks(bricks: list[Brick]) -> list[Brick]:
    # settle the bricks into a tower
    bricks = sorted(bricks, key=lambda b: b.min("z"))
    landed_bricks = []

    for brick in bricks:
        # if brick is already on the ground, don't try to fall further
        if brick.min("z") == 1:
            landed_bricks.append(brick)
            continue

        # Try levels below current brick in order from highest to lowest
        for level in range(brick.min("z") - 1, 0, -1):
            # figure out what bricks already fill this level
            filled = set()
            for lbrick in landed_bricks:
                lbrick.fill_space(level, filled)

            hit_something = any((xy in filled) for xy in brick.range("xy"))
            if hit_something:
                if (level + 1) != brick.min("z"):
                    brick.fall(level + 1)
                landed_bricks.append(brick)
                break
        else:
            # If we never hit anything, fall all the way down
            brick.fall(1)
            landed_bricks.append(brick)

    assert len(bricks) == len(landed_bricks)
    return landed_bricks


def part_1(bricks: list[Brick]) -> list[Brick]:
    for brick in bricks:
        brick.freeze = True
    # start by assuming all bricks are stable
    score = len(bricks)
    # Remove each brick one at a time and see if anything falls
    for i in tqdm(range(len(bricks))):
        pre = bricks[:i]
        post = bricks[i + 1 :]
        try:
            land_bricks(pre + post)
        except Unstable:
            score -= 1

    return score


if __name__ == "__main__":
    my_input = Path("input.txt").read_text().strip()
    bricks = load_bricks(my_input)
    bricks = land_bricks(bricks)
    score = part_1(bricks)
    print(score)
