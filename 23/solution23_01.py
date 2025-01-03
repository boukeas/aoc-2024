from itertools import combinations
from collections import defaultdict
import sys


# read input as a mapping between computers and the other computers
# they are connected to
with open(sys.argv[1]) as file:
    connections = defaultdict(set)
    for line in file:
        computer1, computer2 = line.strip().split("-")
        connections[computer1].add(computer2)
        connections[computer2].add(computer1)

cliques_3 = set()
# iterate over all computers that start with "t" and their connections
for computer, connected in connections.items():
    if computer.startswith('t'):
        # iterate over every pair of connections and form a 3-clique if
        # the pair is also connected to each other
        for computer1, computer2 in combinations(connected, 2):
            if computer1 in connections[computer2]:
                cliques_3.add(tuple(sorted([computer, computer1, computer2])))

result = len(cliques_3)
print(result)
