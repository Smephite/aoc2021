import sys, os
sys.path.append(os.path.abspath("."))
import aoc

from functools import reduce, cache
from itertools import product

input = aoc.aoc()
p1 = int(input[0][28:])
p2 = int(input[1][28:])


scores = [0, 0]
locations = [p1, p2]

WIN_CONDITION = 21


@cache
def recursive(pos1, pos2, scores = (0, 0)):
    wins = [0, 0]
    
    for d1 in product([1, 2, 3], repeat=3):
        pp1 = (pos1 + sum(d1) - 1) % 10 + 1
        sc1 = scores[0] + pp1
        if sc1 >= WIN_CONDITION:
            wins[0] += 1
            continue

        for d2 in product([1, 2, 3], repeat=3):
            pp2 = (pos2 + sum(d2) - 1) % 10 + 1
            sc2 = scores[1] + pp2
            
            if sc2 >= WIN_CONDITION:
                wins[1] += 1
                continue

            ww = recursive(pp1, pp2, (sc1, sc2))
            wins[0] += ww[0]
            wins[1] += ww[1]
    return wins

print("The player winning in most universe is winning in", max(recursive(p1, p2)), "universes.")