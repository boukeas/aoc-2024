import sys

# read the entries in the file as an iterator over pairs
with open(sys.argv[1]) as file:
    pairs = (tuple(int(item) for item in line.split()) for line in file.readlines())

# "unzip" the pairs into two *sorted* lists
l1, l2 = (sorted(l) for l in zip(*pairs))

# the result is the sum of the "distances" of the corresponding items
result = sum(abs(item1-item2) for item1, item2 in zip(l1, l2))
print(result)
