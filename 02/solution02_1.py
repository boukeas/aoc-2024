from itertools import pairwise
import sys


def is_safe_pair_ascending(previous, current):
    return previous < current <= previous + 3

def is_safe_pair_descending(previous, current):
    return previous > current >= previous - 3


def is_safe(line):
    # create an iterator of pairs of elements
    pairs = pairwise(line)
    # get the first pair and use it to determine how pairs will be compared
    previous, current = next(pairs)
    if current > previous:
        is_safe_pair = is_safe_pair_ascending
    elif current < previous:
        is_safe_pair = is_safe_pair_descending
    else:
        return False
    # if the first pair is safe, proceed to compare all other pairs
    if is_safe_pair(previous, current):
        return all(is_safe_pair(previous, current) for previous, current in pairs)
    return False


with open(sys.argv[1]) as file:
    # read each line as an iterator over its integer element
    lines = ((int(item) for item in line.split()) for line in file)
    # count the number of "safe" lines
    result = sum(is_safe(line) for line in lines)

print(result)