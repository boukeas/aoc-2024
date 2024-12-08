from collections import defaultdict
import sys
from itertools import combinations


Position = complex


def out_of_bounds(position: Position) -> bool:
    return (
        position.real < 0 or position.imag < 0 or
        position.real >= nb_rows or position.imag >= nb_columns
    )


def get_directed_antinodes(antenna1: Position, antenna2: Position):
    """
    Generate all harmonic antinodes created from `antenna1` towards
    the direction of `antenna2`, until the bounds of the grid are reached
    """
    harmonic = 0
    distance = antenna1 - antenna2
    while True:
        antinode = antenna1 + harmonic * distance
        if out_of_bounds(antinode):
            break
        yield antinode
        harmonic += 1


def get_antinodes(antenna1: Position, antenna2: Position):
    """
    Generate the antinodes created from a pair of antennas --
    calls `get_directed_antinodes` in both directions
    """
    yield from get_directed_antinodes(antenna1, antenna2)
    yield from get_directed_antinodes(antenna2, antenna1)


# read the input as a dict mapping (row, column) coordinates to their contents
with open(sys.argv[1]) as file:
    antennas = defaultdict(set)
    start_position = None
    for row, line in enumerate(file):
        for column, symbol in enumerate(line.strip()):
            if symbol != ".":
                antennas[symbol].add(complex(row, column))

# read the input as a map from antenna families to the coordinates of each
# family's individual antennas
with open(sys.argv[1]) as file:
    antennas = defaultdict(set)
    start_position = None
    for row, line in enumerate(file):
        for column, symbol in enumerate(line.strip()):
            if symbol != ".":
                # store the coordinates as a complex number to allow for
                # vector operations
                antennas[symbol].add(complex(row, column))

# global variables for the size of the grid
nb_rows, nb_columns = row + 1, column + 1

# generate antinodes for each pair of antennas in the same family
antinodes = {
    antinode
    for family in antennas.values()
    for antenna1, antenna2 in combinations(family, r=2)
    for antinode in get_antinodes(antenna1, antenna2)
}

result = len(antinodes)
print(result)
