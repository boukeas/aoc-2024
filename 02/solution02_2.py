from itertools import pairwise
import sys


def is_safe_pair_ascending(previous, current):
    return previous < current <= previous + 3

def is_safe_pair_descending(previous, current):
    return previous > current >= previous - 3


def is_safe(line, is_safe_pair):
    # create an iterator of pairs of elements
    pairs = pairwise(line)
    # get the first pair
    previous, current = next(pairs)
    nb_unsafe_pairs = 0
    if is_safe_pair(previous, current):
        previous, current = next(pairs)
    else:
        # the first pair isn't safe, so move on to the next pair...
        first = previous
        previous, current = next(pairs)
        if is_safe_pair(first, current) or is_safe_pair(previous, current):
            # ... and check if a safe pair can be formed with one of the first two elements
            nb_unsafe_pairs += 1
            previous, current = next(pairs)
        else:
            return False
    # if the first triplet is safe, proceed to compare all other pairs
    while nb_unsafe_pairs <= 1:
        if is_safe_pair(previous, current):
            try:
                previous, current = next(pairs)
            except StopIteration:
                return True
        else:
            # this pair isn't safe, skip the second item in the pair and proceed
            # (i.e. `previous` remains the same, `current` advances)
            nb_unsafe_pairs += 1
            try:
                _, current = next(pairs)
            except StopIteration:
                return nb_unsafe_pairs <= 1
    return False


with open(sys.argv[1]) as file:
    # read each line as an iterator over its integer element
    lines = (tuple(int(item) for item in line.split()) for line in file)
    # count the number of "safe" lines
    # (for every line, try checking for safe ascending and then descending because
    # it's not straightforward to directly determine which of the two applies)
    result = sum(
        (is_safe(line, is_safe_pair_ascending) or is_safe(line, is_safe_pair_descending))
        for line in lines
    )

print(result)