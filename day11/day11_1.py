import sys, os
sys.path.append(os.path.abspath(".."))
from aoc21 import aoc

octopuses = []
for line in aoc.aoc():
    line_arr = []
    for c in list(line):
        line_arr.append(int(c))
    octopuses.append(line_arr)



def get_neighbours(pos):
    neighbours = []
    x_max = len(octopuses[0])
    y_max = len(octopuses)

    if pos[0] != 0:
        neighbours.append((pos[0]-1, pos[1]))
    if pos[1] != 0:
        neighbours.append((pos[0], pos[1]-1))
    if pos[0] != x_max-1:
        neighbours.append((pos[0]+1, pos[1]))
    if pos[1] != y_max-1:
        neighbours.append((pos[0], pos[1]+1))

    if pos[0] != 0 and pos[1] != 0:
        neighbours.append((pos[0]-1, pos[1]-1))
    if pos[0] != x_max-1 and pos[1] != 0:
        neighbours.append((pos[0]+1, pos[1]-1))
    if pos[0] != 0 and pos[1] != y_max-1:
        neighbours.append((pos[0]-1, pos[1]+1))
    if pos[0] != x_max-1 and pos[1] != y_max-1:
        neighbours.append((pos[0]+1, pos[1]+1))

    return neighbours


W  = '\033[0m'  # white (normal)
R  = '\033[31m' # red

def print_octopuses(octopuses, flashed):
    for y in range(len(octopuses)):
        out = ""
        for x in range(len(octopuses[0])):
            if (x,y) in flashed:
                out += R + str(octopuses[y][x]) + W
            else:
                out += str(octopuses[y][x])
        print(out)

#print("Before any round:")
#print_octopuses(octopuses, [])

flashes = 0
rounds = 100
for round in range(1, rounds+1):
    flashed = []

    newly_flashed = []

    for y in range(len(octopuses)):
        for x in range(len(octopuses[y])):
            octopuses[y][x] += 1
            if octopuses[y][x]>9:
                flashed.append((x, y))
                newly_flashed.append((x, y))
                octopuses[y][x] = 0
    
    while len(newly_flashed) != 0:
        sec_flashes = []
        for pos in newly_flashed:
            neighbours = list(filter(lambda pos: pos not in flashed and pos not in newly_flashed and pos not in sec_flashes, get_neighbours(pos)))
            for n in neighbours:
                octopuses[n[1]][n[0]] += 1
                if octopuses[n[1]][n[0]] > 9:
                    octopuses[n[1]][n[0]] = 0
                    flashed.append(n)
                    sec_flashes.append(n)
        
        newly_flashed = sec_flashes

    flashes += len(flashed)
#    print(f"\nRound {round}: {flashes}")
#    if round <= 10 or round % 10 == 0:
#        print_octopuses(octopuses, flashed)

print(f"After {rounds} rounds the amount of recorded flashes equals {flashes}")