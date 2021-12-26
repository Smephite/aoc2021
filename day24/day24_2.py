import sys, os
sys.path.append(os.path.abspath("."))
import aoc, math
# with the same usage of educated guesses as in part 1 we can determine:
# the lowest number is 
# 51316214181141

comparison_mod = [12, 13, 12, -13, 11, 15, -14, 12, -8, 14, -9, -11, -6, -5]
addition_mod = [1, 9, 11, 6,  6, 13, 13, 5, 7,  2, 10, 14, 7,  1]
div_mod =      [1, 1, 1,  26, 1, 1,  26, 1, 26, 1, 26, 26, 26, 26]

def solve(digit, n = 0, z=0):
    x = digit != (z%26) + comparison_mod[n]
    return math.floor(z / div_mod[n])*(25*x+1) + (digit+addition_mod[n])*x

def solve_str(str):
    assert(len(str) == 14)
    z = 0
    n = 0
    for c in list(str):
        z = solve(int(c), n, z)
        n += 1
    return z

print(solve_str("51316214181141"))
