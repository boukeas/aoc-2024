"""
$ python3 solution18_1.py input18_test.txt 6 12
22

$ python3 solution18_1.py input18.txt 70 1024
372
"""

from enum import Enum
from math import inf
import sys


class Direction(Enum):
    North = complex(-1, 0)
    East = complex(0, 1)
    South = complex(1, 0)
    West = complex(0, -1)


def neighbours(position: complex, map: set[complex]):
    """
    Generate the coordinates of valid positions around `position`

    A position is valid if it is in the `map`, which holds for positions
    that are not out of bounds and are not corrupted.
    """
    for direction in Direction:
        new_position = position + direction.value
        if new_position in map:
            yield new_position


def read_input(lines: int | None = None):
    """
    Generate the coordinates of the positions contained in the input file

    If `lines` is not None then only read the first `lines` of input.
    """
    count = 0
    with open(sys.argv[1]) as file:
        for line in file:
            x, y = (int(coordinate) for coordinate in line.strip().split(","))
            yield complex(y, x)
            count += 1
            if lines and count == lines:
                break


def search(map: set[complex], source: complex, target: complex) -> dict[complex, int]:
    """
    Return a "scores" mapping that associates each position in the `map` with
    the number of steps required to reach the `target` from that position.

    For the small example provided, this is what the scores look like:

    22 21 22  # 14 13 12
    21 20  # 16 15  # 11
    20 19 18 17  #  9 10
    21 20 19  #  7  8  #
    22 21  #  5  6  #  2
     .  #  5  4  #  2  1
     #  .  #  3  2  1  0

    The bottom right position (with the 0) is the `target` and the top left is
    the `source`. The iterative process of computing the scores stops either
    when there are no more scores to compute or when the `source` has a score
    (hence the positions without a score).

    If the returned scores contain a score for the `source` then the target is
    reachable from the source and the score is the minimum number of steps
    required to reach it.
    """
    # initially all scores are infinite, except the target which is 0
    scores = {
        position: inf
        for position in map
    }
    scores[target] = 0
    # the frontier is the set of positions that need to be examined and
    # it is expanded outwards from the target
    frontier = {target}
    visited = set()
    while frontier and not scores[source] < inf:
        new_frontier = set(
            neighbour
            for position in frontier
            for neighbour in neighbours(position, map)
            if neighbour not in visited
        )
        visited.update(frontier)
        # the score of each node in the new frontier is the best of its
        # neighbour's scores plus one (the cost of moving to a neighbour)
        scores.update({
            position: 1 + min(
                scores[neighbour] for neighbour in neighbours(position, map)
            )
            for position in new_frontier
        })
        frontier = new_frontier
    return scores


def print_map():
    for row in range(size + 1):
        for column in range(size + 1):
            position = complex(row, column)
            if position in map:
                score = scores[position]
                if score < inf:
                    print(f"{score:>3}", end="")
                else:
                    print(f"{'.':>3}", end="")
            else:
                print(f"{'#':>3}", end="")
        print()
    print()


# the size of the grid and the number of corrupted blocks to read from the
# input file are specified as command-line arguments
size = int(sys.argv[2])
nb_corrupted = int(sys.argv[3])

source = complex(0, 0)
target = complex(size, size)

# create an "empty" map, i.e. a set that contains all positions
map = {
    complex(row, column)
    for row in range(size + 1)
    for column in range(size + 1)
}
# read the corrupted blocks from the input file
corrupted = read_input(lines=nb_corrupted)
# remove the corrupted blocks from the map
map.difference_update(corrupted)

scores = search(map, source, target)
# print_map()
print(scores[source])
