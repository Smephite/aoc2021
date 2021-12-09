import sys, os
sys.path.append(os.path.abspath(".."))
from aoc21 import aoc

def get_neighbours(x, y, max_x, max_y):
    neighbours = []

    if x != 0:
        neighbours.append((x-1, y))
    if x != max_x - 1:
        neighbours.append((x+1, y))
    if y != 0:
        neighbours.append((x, y-1))
    if y != max_y - 1:
        neighbours.append((x, y+1))
    
    return neighbours

input = aoc.aoc()

minima = []

for y in range(len(input)):
    row = input[y]
    for x in range(len(row)):
        value = int(row[x])
        lower_neighbours  = list(filter(lambda pos: int(input[pos[1]][pos[0]]) <= value, get_neighbours(x, y, len(row), len(input))))
        
        if len(lower_neighbours) == 0:
            minima.append((x, y))

risk_level = sum(map(lambda minima: int(input[minima[1]][minima[0]]), minima)) + len(minima)

print("Risk level:", risk_level)
