from collections import defaultdict
from enum import Enum
import sys
from typing import Tuple


class Direction(Enum):
    North = (-1, 0)
    Northeast = (-1, 1)
    East = (0, 1)
    Southeast = (1, 1)
    South = (1, 0)
    Southwest = (1, -1)
    West = (0, -1)
    Northwest = (-1, -1)


Position = Tuple[int, int]


def move(position: Position, direction: Direction) -> Position:
    """
    Return the position you find yourself if you move from `position`
    towards `direction`
    """
    row, column = position
    row_offset, column_offset = direction.value
    return (row + row_offset, column + column_offset)


def generate_directions_for_position(data, position, next_letter, directions, next_directions):
    """
    Given that `directions` is a mapping of positions where
    the current letter was found to the directions where the `next_letter`
    might be found, perform the actual check and update `next_directions`
    (for the next letter) accordingly, i.e. allow moving in the same direction
    """
    for direction in directions[position]:
        next_position = move(position, direction)
        if next_position not in data:
            continue
        if data[next_position] == next_letter:
            next_directions[next_position].add(direction)


def generate_directions(data, next_letter, directions):
    """
    Call `generate_directions_for_position` for all the positions
    remaining in `directions`
    """
    next_directions = defaultdict(set)
    for position in directions.keys():
        generate_directions_for_position(data, position, next_letter, directions, next_directions)
    return next_directions


# read the input as a dict mapping (row, column) coordinates to their contents
with open(sys.argv[1]) as file:
    data = {
        (row, column): letter
        for row, line in enumerate(file)
        for column, letter in enumerate(line.strip())
    }

word = "XMAS"

# `directions` is mapping of (row, column) coordinates to
# a set of directions where the next letter of the word _might_ lie
directions = defaultdict(set)

# initialise `directions`: map every position where the first letter
# of the word is found to the complete set of directions
for position in data.keys():
    if data[position] == word[0]:
        directions[position] = set(direction for direction in Direction)

# iteratively call `generate_directions` for the remaining letters in the word
for next_letter in word[1:]:
    directions = generate_directions(data, next_letter, directions)

# the total number of remaining feasible directions is the total number
# of times that the `word` was found in the data, in any direction
result = sum(len(candidates) for candidates in directions.values())
print(result)
