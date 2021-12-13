import sys, os
sys.path.append(os.path.abspath("."))
import aoc

in_folding_instructions = False

dots = []
folding = []

for line in aoc.aoc():
    if in_folding_instructions:
        [axis, number] = line.split("=")
        folding.append((axis.split(" ")[2], int(number)))
    else:
        if line == "":
            in_folding_instructions = True
        else:
            [x, y] = line.split(",")
            dots.append((int(x),int(y)))

for f in folding:
    new_dots = []
    if f[0] == 'x':
        # fold left plane to right
        for d in dots:
            if d[0] < f[1]:
                new_dots.append(d)
            else:
                new_dots.append((2*f[1]-d[0], d[1]))
    if f[0] == 'y':
        # fold left plane to right
        for d in dots:
            if d[1] < f[1]:
                new_dots.append(d)
            else:
                new_dots.append((d[0], 2*f[1]-d[1]))
    dots = list(set(new_dots))

max_x = max(map(lambda pos: pos[0], dots))
max_y = max(map(lambda pos: pos[1], dots))

for y in range(max_y+1):
    for x in range(max_x+1):
        print('█' if (x, y) in dots else ' ', end="")
    print("")