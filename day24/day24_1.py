import sys, os
sys.path.append(os.path.abspath("."))
import aoc, math

from itertools import product

#x = inp[n] != (z%26) + [12, 13, -13, 11, 15, -14, -8, 14, -9, -11, -6, -5]

#y = 25*x +1 -> (1, 26)
#z = floor(z / [1, 26])*y + (inp[n]+[add_mod])*x

comparison_mod = [12, 13, 12, -13, 11, 15, -14, 12, -8, 14, -9, -11, -6, -5]
addition_mod = [1, 9, 11, 6,  6, 13, 13, 5, 7,  2, 10, 14, 7,  1]
div_mod =      [1, 1, 1,  26, 1, 1,  26, 1, 26, 1, 26, 26, 26, 26]

assert(len(comparison_mod) == len(addition_mod) and len(addition_mod) == len(div_mod))

# we derrived this function by educated guesses and looking at the puzzle input, lol
def solve(digit, n = 0, z=0):
    x = digit != (z%26) + comparison_mod[n]
    return math.floor(z / div_mod[n])*(25*x+1) + (digit+addition_mod[n])*x

def solve2(digit, n, z):
    if digit != (z%26) + comparison_mod[n]:                            # last value on stack + comp_mod != digit 
        if div_mod[n] == 1:
            print("push", digit)
            return z*26 + (digit+addition_mod[n])                      # append push digit + add_mod to stack
        else:
            print("replace", (z%26) + comparison_mod[n])
            return math.floor(z / 26) * 26 + (digit + addition_mod[n]) # replace last element of stack with digit + add_mod
    else:
        if div_mod[n] == 1:
            print("nop")
            return z                 # nop
        else:
            print("pop", digit)
            return math.floor(z / 26) # remove last element from stack

# in our case:
# push input[0]  + 1
# push input[1]  + 9
# push input[2]  + 11
# pop. input[3]  == POP - 13
# push input[4]  + 6
# push input[5]  + 13
# pop. input[6]  == POP - 14
# push input[7]  + 5
# pop. input[8]  == POP - 8
# push input[9]  + 2
# pop. input[10] == POP - 9
# pop. input[11] == POP - 11
# pop. input[12] == POP - 6
# pop. input[13] == POP - 5

#INPUT[0]                        
#INPUT[1]                        
#INPUT[2]                        
#INPUT[3]  ==  input[2] - 2      
#INPUT[4]                        
#INPUT[5]                        
#input[6]  ==  input[5] - 1      
#INPUT[7]                        
#input[8]  ==  input[7] - 3      
#INPUT[9]                        
#input[10] ==  input[9] - 7      
#input[11] ==  input[4] - 5      
#input[12] ==  input[1] + 3      
#input[13] ==  input[0] - 4      


# the highest number therefor is 
# 96979989692495



def solve_str(str):
    assert(len(str) == 14)
    z = 0
    n = 0
    for c in list(str):
        z = solve2(int(c), n, z)
        n += 1
    return z

print(solve_str("96979989692495"))

