import sys, os
sys.path.append(os.path.abspath(".."))
from aoc21 import aoc

input = aoc.aoc()

starting_entities = list(map(lambda x: int(x), input[0].split(",")))

days = 256

entities = [0 for i in range(0, 9)]

for entity in starting_entities:
    entities[entity] += 1

for _ in range(0, days):
    new_entities = [0 for i in range(0, 9)]
    for i in range(0, 9):
        index = 8-i
        if index == 0:
            new_entities[8] += entities[0]
            new_entities[6] += entities[0]
        else:
            new_entities[index-1] += entities[index]
    entities = new_entities

print(f"After {days} days, there will be {sum(entities)} fish!")