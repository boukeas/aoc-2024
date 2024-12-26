from functools import cache
import sys
from typing import Tuple

"""
# testing
$ python3 solution11.py input11_test1.txt 1
7
$ python3 solution11.py input11_test2.txt 6
22
$ python3 solution11.py input11_test2.txt 25
55312
# part 1
$ python3 solution11.py input11.txt 25
199982
$ python3 solution11.py input11.txt 75
237149922829154
"""

@cache
def blink(stone: int) -> Tuple[int]:
    """
    Return a tuple containing the stones after one blink starting with `stone`
    """
    if stone == 0:
        return (1,)
    else:
        stone_str = str(stone)
        length = len(stone_str)
        if length % 2 == 0:
            return (int(stone_str[:length // 2]), int(stone_str[length // 2:]))
        else:
            return (stone * 2024,)


@cache
def count_stones(stones: Tuple[int], blinks: int):
    """
    Start with a set of `stones` and (recursively) compute the number of stones
    present after a specific number of blinks.
    """
    if blinks == 0:
        return len(stones)
    return sum(count_stones(blink(stone), blinks - 1) for stone in stones)


blinks = int(sys.argv[2])
with open(sys.argv[1]) as file:
    stones = tuple(int(number) for number in file.read().strip().split())

result = count_stones(stones, blinks)
print(result)
