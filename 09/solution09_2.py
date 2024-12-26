from typing import NamedTuple
import sys


class File(NamedTuple):
    id: int
    size: int
    gap: int


# read the input as a single long string
with open(sys.argv[1]) as file:
    filemap = file.read().strip()

# iterate over the pairs of numbers in the input "filemap" and create
# a list of File objects, storing each file's id, size and succeeding gap
id = 0
files = []
numbers = iter(filemap)
while True:
    size = int(next(numbers))
    try:
        gap = int(next(numbers))
        files.append(File(id, size, gap))
    except StopIteration:
        files.append(File(id, size, 0))
        break
    id += 1

# for each size of gap, store the smallest index from which the search
# for such a gap should begin
gap_indices = {
    size: 0
    for size in range(1, 10)
}

source_index = len(files) - 1
while source_index > 1:
    # the "source" is the file to be moved
    source = files[source_index]
    # search for a gap large enough to hold the file to be moved,
    # starting from the appropriate index
    # (the "target" is the file after which the "source" will be moved)
    target_index = gap_indices[source.size]
    while target_index < source_index and files[target_index].gap < source.size:
        target_index += 1
    # store the position where the gap was found: subsequent searches
    # for a gap of that size should start after this position
    gap_indices[source.size] = target_index + 1
    # check if (and how) the file should be moved
    if target_index + 1 < source_index:
        # remove the source file from its original position
        del files[source_index]
        # update the gap after the file preceeding the "source"
        files[source_index - 1] = files[source_index - 1]._replace(
            gap=files[source_index - 1].gap + source.size + source.gap
        )
        # insert the source file after the target file
        # (updating the gap that succeeds it)
        files.insert(
            target_index + 1,
            source._replace(gap=files[target_index].gap - source.size)
        )
        # remove the gap after the target file
        files[target_index] = files[target_index]._replace(gap=0)
    elif target_index + 1 == source_index:
        # special case: the "source" is already next to the target
        # increase the gap after the source to include the gap after the target
        files[target_index + 1] = files[source_index]._replace(
            gap=files[source_index - 1].gap + files[source_index].gap
        )
        # remove the gap after the target file
        files[target_index] = files[target_index]._replace(gap=0)
    else:
        # the current "source" cannot be moved, advance to the file before it
        source_index -= 1

checksum = 0
index = 0
for (id, size, gap) in files:
    for position in range(size):
        checksum += index * id
        index += 1
    index += gap
print(checksum)