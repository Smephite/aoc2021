import sys, os
from typing import List, Tuple
sys.path.append(os.path.abspath("."))
import aoc

east = []
south = []

input = aoc.aoc()
max_y = len(input)
max_x = len(input[0])

Field = Tuple[List[Tuple[int, int]], List[Tuple[int, int]]]

for y in range(len(input)):
    line = input[y]
    for x in range(len(line)):
        c = line[x]
        if c == '>':
            east.append((x, y))
        elif c == 'v':
            south.append((x,y))

#print(east, south)

def step(field):
    (east, south) = field
    new_e, new_s = [], []
    for c in east:
        (x, y) = c
        new = ((x+1) % max_x, y)
        if new in east or new in south:
            new_e.append(c)
            continue
        new_e.append(new)
    for c in south:
        (x, y) = c
        new = (x, (y+1) % max_y)
        if new in new_e or new in south:
            new_s.append(c)
            continue
        new_s.append(new)
    return (new_e, new_s)

def print_field(field):
    for y in range(max_y):
        for x in range(max_x):
            p = (x, y)
            if p not in field[0] and p not in field[1]:
                print(".", end="")
            elif p in field[0]:
                print(">", end="")
            elif p in field[1]:
                print("v", end="")
        print("")

field = (east, south)
i = 0
while True:
    print("Move", i)
#    print_field(field)
    n_f = step(field)
    if n_f == field:
        break
    field = n_f
    i+=1

print(f"The cucumbers stopped moving after {i+1} steps.")