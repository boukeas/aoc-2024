from collections import Counter
from enum import Enum
import sys


class Direction(Enum):
    North = complex(-1, 0)
    East = complex(0, 1)
    South = complex(1, 0)
    West = complex(0, -1)


def get_neighbours(position: complex, map: set[complex]):
    """
    Generate the coordinates of valid positions around `position`

    A position is valid if it is in the `map`, which holds for positions
    that are not out of bounds and are in the track (not walls)
    """
    for direction in Direction:
        neighbour = position + direction.value
        if neighbour in map:
            yield neighbour


def peek(position: complex, scores: set[complex]):
    """
    Generate the scores of all positions that are at two positions away from
    `position`.
    """
    for direction in Direction:
        neighbour = position + direction.value
        if neighbour not in scores:
            neighbour += direction.value
        try:
            yield scores[neighbour]
        except KeyError:
            pass


def follow(start: complex, end: complex, map: set[complex]):
    """
    Generate all the positions on the track from `start` to `end`.
    """
    previous = None
    current = start
    while current != end:
        yield current
        new_current = (set(get_neighbours(current, map)) - {previous}).pop()
        previous = current
        current = new_current
    yield end


# read the input as a dict mapping (row, column) coordinates to their contents
with open(sys.argv[1]) as file:
    map = set()
    for row, line in enumerate(file):
        for column, content in enumerate(line.strip()):
            if content == ".":
                map.add(complex(row, column))
            elif content == "S":
                start = complex(row, column)
                map.add(complex(row, column))
            elif content == "E":
                end = complex(row, column)
                map.add(complex(row, column))

# follow the track from start to end and record the list of positions visited
track = list(follow(start, end, map))
# score each track position with its distance to the end
scores = {position: steps for steps, position in enumerate(reversed(track))}

# count the number of cheats
cheats = Counter()
nb_cheats = 0
for position in track:
    current_score = scores[position]
    # peek at the score of every position that is reachable by cheating
    for cheat_score in peek(position, scores):
        improvement = current_score - (cheat_score + 2)
        # exclusively for testing
        if improvement > 0:
            cheats.update({improvement: 1})
        # count the result
        if improvement >= 100:
            nb_cheats += 1

# reproduce the testing output
for key, value in sorted(cheats.items()):
    print(f"There are {value} cheats that save {key} picoseconds")

print(nb_cheats)
