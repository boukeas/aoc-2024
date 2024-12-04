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

# read the input as a dict mapping (row, column) coordinates to their contents
with open(sys.argv[1]) as file:
    data = {
        (row, column): letter
        for row, line in enumerate(file)
        for column, letter in enumerate(line.strip())
    }

# generate the positions where A is located, i.e the centre of the X-MAS cross
x_centres = (position for position in data.keys() if data[position] == 'A')

result = 0
for position in x_centres:
    try:
        # form the three-letter word centered around `position` (a x-centre)
        # in a southwest to northeast direction
        candidate_1 = "".join((data[move(position, Direction.Northeast)], data[position], data[move(position, Direction.Southwest)]))
    except KeyError:
        continue
    try:
        # form the three-letter word centered around `position` (a x-centre)
        # in a southeast to northwest direction
        candidate_2 = "".join((data[move(position, Direction.Northwest)], data[position], data[move(position, Direction.Southeast)]))
    except KeyError:
        continue
    # check if an X-MAS cross is formed
    result += candidate_1 in ("MAS", "SAM") and candidate_2 in ("MAS", "SAM")

print(result)
