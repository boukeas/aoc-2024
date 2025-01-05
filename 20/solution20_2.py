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


def peek(position: complex, scores: set[complex], distance: int):
    """
    Peek at the scores of all positions that are within (at most) a certain
    Manhattan `distance` from `position`. Generate distance,score pairs.
    """
    yielded = set()
    for direction in Direction:
        for parallel_distance in range(2, distance + 1):
            for perpendicular_distance in range(distance + 1 - parallel_distance):
                # rotate 90 and -90 degrees from the peeking direction
                for rotation in (complex(0, 1), complex(0, -1)):
                    # move parallel_distance steps in `direction`, then rotate
                    # and move another perpendicular_distance steps
                    # (parallel_distance + perpendicular distance <= distance)
                    distant_neighbour = position + (
                        parallel_distance * direction.value +
                        perpendicular_distance * direction.value * rotation
                    )
                    if distant_neighbour not in yielded:
                        yielded.add(distant_neighbour)
                        try:
                            yield (
                                (parallel_distance + perpendicular_distance),
                                scores[distant_neighbour]
                            )
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
    for distance, cheat_score in peek(position, scores, distance=20):
        improvement = current_score - (cheat_score + distance)
        # exclusively for testing
        if improvement >= 50:
            cheats.update({improvement: 1})
        # count the result
        if improvement >= 100:
            nb_cheats += 1

# reproduce the testing output
for key, value in sorted(cheats.items()):
    print(f"There are {value} cheats that save {key} picoseconds")

print(nb_cheats)