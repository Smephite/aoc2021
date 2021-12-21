import sys, os
sys.path.append(os.path.abspath("."))
import aoc

input = aoc.aoc()
p1 = int(input[0][28:])
p2 = int(input[1][28:])


scores = [0, 0]
locations = [p1, p2]

turn = 0
roll = 0
d = 0
rolls = 0
while max(scores)<1000:
    rolls+=3
    roll_sum = int(((roll+3)*(roll+4) - roll*(roll+1))/2)
    roll = (roll + 3) % 100
    locations[turn] = (locations[turn]+roll_sum - 1) % 10 + 1
    scores[turn] += locations[turn]
    turn = (turn+1) % 2

print("The losing players score * #dicerolls = ", min(scores) * rolls)