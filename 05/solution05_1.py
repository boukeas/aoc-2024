import sys
from collections import defaultdict
from itertools import pairwise


# read the input
with open(sys.argv[1]) as file:
    # for each "preceding|succeeding" constraint, record the succeeding number
    # in the set of numbers that need to come after the preceding number
    after = defaultdict(set)
    for line in file:
        line = line.strip()
        if line:
            preceding, succeeding = (int(item) for item in line.split("|"))
            after[preceding].add(succeeding)
        else:
            # empty line, terminate the constraint section
            break
    # for each sequence, check if it is valid and sort it if it is not
    result = 0
    for line in file:
        line = line.strip()
        sequence = [int(item) for item in line.split(",")]
        # validity: check if consequtive pairs of numbers violate constraints
        valid = True
        for preceding, succeeding in pairwise(sequence):
            if succeeding not in after[preceding]:
                valid = False
                break
        if valid:
            result += sequence[len(sequence) // 2]

    print(result)
