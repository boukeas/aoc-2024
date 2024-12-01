from collections import Counter
import sys

# read the entries in the file as an iterator over pairs
with open(sys.argv[1]) as file:
    pairs = (tuple(int(item) for item in line.split()) for line in file.readlines())

# "unzip" the pairs into two lists
l1, l2 = zip(*pairs)

# use a Counter for the number of occurrences of the items in the second list
occurences_l2 = Counter(l2)

# "calculate a total similarity score by adding up each number in the left list
# after multiplying it by the number of times that number appears in the right list"
result = sum(item * occurences_l2[item] for item in l1)
print(result)