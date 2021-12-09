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

max_y = len(input)
max_x = len(input[0])

var_input = [[0 for _ in range(max_x)] for _ in range(max_y)]

for x in range(max_x):
    for y in range(max_y):
        var_input[y][x] = int(input[y][x])

input = var_input

minima = []

for y in range(max_y):
    row = input[y]
    for x in range(max_x):
        value = row[x]
        lower_neighbours  = list(filter(lambda pos: input[pos[1]][pos[0]] <= value, get_neighbours(x, y, len(row), len(input))))
        
        if len(lower_neighbours) == 0:
            minima.append((x, y))

basins = []

for minimum in minima:


    value = input[minimum[1]][minimum[0]]
    to_explore = list(filter(lambda pos: input[pos[1]][pos[0]] > value and input[pos[1]][pos[0]] != 9, get_neighbours(minimum[0], minimum[1], max_x, max_y)))

    explored = [minimum]

    while len(to_explore) > 0:
        exploring = to_explore.pop(0)
        val = input[exploring[1]][exploring[0]]
        explored.append(exploring)
        if val == 9:
            continue
        to_explore += list(filter(lambda pos: input[pos[1]][pos[0]] > val and pos not in explored and pos not in to_explore and input[pos[1]][pos[0]] != 9, get_neighbours(exploring[0], exploring[1], max_x, max_y)))

    basins.append(len(explored))


basins.sort()
max_basins = (basins[-3:])

mult = 1

for b in max_basins:
    mult *= b

print(f"The multiplied basin area is {mult}")
