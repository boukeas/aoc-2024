from enum import Enum
import sys


class Direction(Enum):
    North = complex(-1, 0)
    East = complex(0, 1)
    South = complex(1, 0)
    West = complex(0, -1)



def get_neighbours(position: complex):
    """
    Generate the neighbouring coordinates of a `position`
    """
    for direction in Direction:
        yield position + direction.value


def flood(position: complex, map: dict[complex, str]) -> tuple[set[complex], int]:
    """
    Starting from a specific `position` in the `map`, flood the area with the
    same content as the `position`. Return the set of all the coordinates this
    area contains, along with the size of its perimeter.
    """
    # the starting symbol
    symbol = map[position]
    # the set of coordinates in the area
    visited = set()
    # the frontier of the flood
    frontier = {position}
    # the size of the perimeter of the flooded area
    perimeter = 4
    while frontier:
        current = frontier.pop()
        visited.add(current)
        # extend the frontier with all the neighbours of the current position
        # with the same content, that have not already been visited
        neighbours = {
            neighbour
            for neighbour in get_neighbours(current)
            if map.get(neighbour) == symbol and neighbour not in frontier
        }
        new_neighbours = neighbours - visited
        frontier.update(new_neighbours)
        # extend the perimeter:
        # - each new neighbour increases the perimeter by 4
        # - each neighbour that has already been visited decreases
        #   the perimeter by 2 (because the common side between the two positions
        #   has already been counted twice)
        perimeter += (
            4 * len(new_neighbours) -
            2 * (len(neighbours) - len(new_neighbours))
        )
    return visited, perimeter


# read the input into a mapping of each coordinate to the symbol it contains
with open(sys.argv[1]) as file:
    map = {}
    for row, line in enumerate(file):
        for column, symbol in enumerate(line.strip()):
            map[complex(row, column)] = symbol

result = 0
# gather all the coordinates found in the map into a set
unprocessed = set(map.keys())
while unprocessed:
    # pick one coordinate
    current = unprocessed.pop()
    # start flooding from the current coordinate and gather
    # the group of coordinates with the same symbol and the
    # number of sides for the group
    group, perimeter = flood(current, map)
    unprocessed.difference_update(group)
    result += len(group) * perimeter
print(result)
