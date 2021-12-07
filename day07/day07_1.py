import sys, os
sys.path.append(os.path.abspath(".."))
from aoc21 import aoc

input = list(map(lambda x: int(x), aoc.aoc()[0].split(",")))

positions = [0 for _ in range(0, max(input))]
for i in range(0, max(input)):
    for x in input:
        positions[i] += abs(x-i)

print(f"The least fuel usage for the crab ships is {min(positions)}")