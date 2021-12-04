import sys, os
sys.path.append(os.path.abspath(".."))
from aoc21 import aoc

input = aoc.aoc()

x = 0
y = 0
aim = 0

for l in input:
    ops = l.split(" ")
    dist = int(ops[1])
    if ops[0] == "up":
        aim-=dist
    elif ops[0] == "down":
        aim+=dist
    elif ops[0] == "forward":
        x+=dist
        y+=aim*dist

print(f"The final answer is {x*y}")
    