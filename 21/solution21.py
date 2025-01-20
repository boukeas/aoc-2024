"""
# part I
$ python3 solution21.py input.txt 2

# part II
$ python3 solution21.py input.txt 25
"""

from functools import cache
from itertools import pairwise
from string import digits
import sys


def numeric(code: str) -> str:
    """
    Return the numeric part of the `code`
    """
    return int(
        "".join(
            character
            for character in code if character in digits
        )
    )


class Playout:

    """
    +---+---+---+
    | 7 | 8 | 9 |
    +---+---+---+
    | 4 | 5 | 6 |
    +---+---+---+
    | 1 | 2 | 3 |
    +---+---+---+
      x | 0 | A |
        +---+---+
    """

    numerical_coordinates = {
        "0": complex(3, 1),
        "1": complex(2, 0),
        "2": complex(2, 1),
        "3": complex(2, 2),
        "4": complex(1, 0),
        "5": complex(1, 1),
        "6": complex(1, 2),
        "7": complex(0, 0),
        "8": complex(0, 1),
        "9": complex(0, 2),
        "A": complex(3, 2),
        "x": complex(3, 0)
    }

    """
        +---+---+
      x | ^ | A |
    +---+---+---+
    | < | v | > |
    +---+---+---+
    """

    directional_coordinates = {
        "^": complex(0, 1),
        "<": complex(1, 0),
        "v": complex(1, 1),
        ">": complex(1, 2),
        "A": complex(0, 2),
        "x": complex(0, 0)
    }

    @classmethod
    @cache
    def coordinates(cls, char_1: str, char_2: str) -> bool:
        if len(set(cls.numerical_coordinates) & {char_1, char_2}) == 2:
            return cls.numerical_coordinates
        else:
            return cls.directional_coordinates

    @classmethod
    @cache
    def distance(cls, start: str, end: str) -> tuple[int, int]:
        """
        Return the vertical and horizontal distance between the `start`
        and `end` positions.
        """
        coordinates = cls.coordinates(start, end)
        difference = coordinates[end] - coordinates[start]
        return int(difference.real), int(difference.imag)

    @classmethod
    @cache
    def translate(cls, start: str, end: str):
        """
        Return the sequence of directional instructions that would result in
        a move from the `start` symbol to the `end` symbol.
        """
        vertical_distance, horizontal_distance = cls.distance(start, end)
        if vertical_distance > 0:
            vertical_instructions = "v" * vertical_distance
        elif vertical_distance < 0:
            vertical_instructions = "^" * -vertical_distance
        else:
            vertical_instructions = ""
        if horizontal_distance > 0:
            horizontal_instructions = ">" * horizontal_distance
        elif horizontal_distance < 0:
            horizontal_instructions = "<" * -horizontal_distance
        else:
            horizontal_instructions = ""
        if horizontal_instructions and vertical_instructions:
            result = []
            coordinates = cls.coordinates(start, end)
            # make sure the instructions don't take us over an "x"
            if (
                coordinates[start].real != coordinates['x'].real or
                coordinates[start].imag + horizontal_distance != coordinates['x'].imag
            ):
                result.append(
                    horizontal_instructions + vertical_instructions + "A"
                )
            if (
                coordinates[start].imag != coordinates['x'].imag or
                coordinates[start].real + vertical_distance != coordinates['x'].real
            ):
                result.append(
                    vertical_instructions + horizontal_instructions + "A"
                )
            return tuple(result)
        else:
            return (horizontal_instructions + vertical_instructions + "A",)

    @classmethod
    @cache
    def length(self, sequence: str, depth: int):
        """
        Return the length of the instruction sequence that a robot which is
        `depth` levels down would need to type in order for the robot at
        the current level to type `sequence`.
        """
        if depth == 0:
            return len(sequence)
        result = 0
        for start, end in pairwise("A" + sequence):
            # get the candidate translation instructions for the robot at
            # the current depth
            instructions = self.translate(start, end)
            if len(instructions) == 1:
                # there is only one candidate sequence of instructions
                result += self.length(instructions[0], depth - 1)
            else:
                # there are two candidate sequences of instructions:
                # choose the one with the minimum length
                result += min(
                    self.length(instructions[0], depth - 1),
                    self.length(instructions[1], depth - 1)
                )
        return result


with open(sys.argv[1]) as file:
    codes = [line.strip() for line in file]

# get the "depth" (i.e. the number of directional keyboard robots) from the
# command line and add 1 for the robot on the numerical keyboard
depth = int(sys.argv[2]) + 1
result = sum(
    numeric(code) * (Playout.length("A" + code, depth) - 1)
    for code in codes
)
print(result)
