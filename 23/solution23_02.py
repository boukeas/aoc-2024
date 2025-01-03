from collections import defaultdict
import sys


# cliques[n] will store the set of all cliques of size n
# (each clique will be stored as a sorted tuple)
cliques = defaultdict(set)

# read input as a mapping between computers and the other computers
# they are connected to; also store the connections as 2-cliques
with open(sys.argv[1]) as file:
    connections = defaultdict(set)
    for line in file:
        connection = line.strip().split("-")
        computer1, computer2 = connection
        connections[computer1].add(computer2)
        connections[computer2].add(computer1)
        cliques[2].add(tuple(sorted(line.strip().split("-"))))

# iteratively compute n-cliques from (n-1)-cliques
size = 3
while True:
    print(size)
    # iterate over all (n-1)-cliques
    for clique in cliques[size - 1]:
        clique = set(clique)
        # iterate over all computers and their connections
        for computer, connected in connections.items():
            common = clique.intersection(connected)
            # form an n-clique if the computer is connected to
            # all the computers in the (n-1)-clique
            if common == clique:
                cliques[size].add(tuple(sorted([computer, *common])))
    if len(cliques[size]) == 0:
        break
    size += 1

result = ",".join(cliques[size-1].pop())
print(result)
