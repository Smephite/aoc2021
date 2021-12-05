import sys, os
from typing import List
sys.path.append(os.path.abspath(".."))
from aoc21 import aoc

lines : List[str]= aoc.aoc()
positions = {}

for line in lines:
    data = line.split(" -> ")
    start = data[0].split(",")
    end = data[1].split(",")

    start_x = int(start[0])
    start_y = int(start[1])
    end_x = int(end[0])
    end_y = int(end[1])

    if end_x < start_x:
        temp = end_x
        end_x = start_x
        start_x = temp

    if end_y < start_y:
        temp = end_y
        end_y = start_y
        start_y = temp

    if start_x != end_x and start_y != end_y:
        continue # only consider straight lines

    if start_x == end_x:
        for y in range(start_y, end_y + 1):

            pos = f"{start_x},{y}"
            if pos not in positions.keys():
                positions[pos] = 0
            positions[pos] = positions[pos]+1
    elif start_y == end_y:
        for x in range(start_x, end_x + 1):

            pos = f"{x},{start_y}"
            if pos not in positions.keys():
                positions[pos] = 0
            positions[pos] = positions[pos]+1


print("The amount of points with overlap counter >=2 is:", len(list(filter(lambda x: x>=2, positions.values()))))