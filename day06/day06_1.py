import sys, os
sys.path.append(os.path.abspath(".."))
from aoc21 import aoc

input = aoc.aoc()

entities = list(map(lambda x: int(x), input[0].split(",")))

days = 80

for _ in range(0, days):
    new_entities = []
    for entity in entities:
        if entity == 0:
            new_entities.append(6) # old fish
            new_entities.append(8) # new fish
        else:
            new_entities.append(entity-1)
    entities = new_entities

print(f"After {days} days, there will be {len(entities)} fish!")