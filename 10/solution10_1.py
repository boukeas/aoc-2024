from collections import defaultdict
from enum import Enum
import sys


class Direction(Enum):
    North = complex(-1, 0)
    East = complex(0, 1)
    South = complex(1, 0)
    West = complex(0, -1)


def neighbours(position: complex, slope: int):
    """
    Generate the neighbours of a `position` that have a height difference
    of `slope`.
    """
    height = map[position]
    for direction in Direction:
        neighbour = position + direction.value
        try:
            neighbouring_height = map[neighbour]
        except KeyError:
            continue
        if neighbouring_height - height == slope:
            yield neighbour

# read the input as a mapping from positions to heights
# and also record the set of peak positions (i.e. height is 9)
with open(sys.argv[1]) as file:
    peaks = set()
    map = {}
    for row, line in enumerate(file):
        for column, height in enumerate(line.strip()):
            position = complex(row, column)
            # allow for dots in the input, to be able to read test cases
            if height == '.':
                height = -2
            else:
                height = int(height)
            if height == 9:
                peaks.add(position)
            map[position] = height

# `contours` is a dict that maps each position (of a certain height)
# to the set of peaks that are reachable from that position -- start
# from height 9, i.e. the peaks themselves
height = 9
contours = {peak: {peak} for peak in peaks}
# compute the contours for decreasing heights by computing the union
# of reachable peaks from all neighbours
while height > 0:
    next_contours = defaultdict(set)
    for position, reachable_peaks in contours.items():
        for neighbour in neighbours(position, slope=-1):
            next_contours[neighbour] = next_contours[neighbour].union(reachable_peaks)
    contours = next_contours
    height -= 1

result = sum(len(reachable_peaks) for reachable_peaks in contours.values())
print(result)
