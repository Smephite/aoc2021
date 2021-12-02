import aoc

input = aoc.aoc()

x = 0
y = 0

for l in input:
    ops = l.split(" ")
    dist = int(ops[1])
    if ops[0] == "up":
        y-=dist
    elif ops[0] == "down":
        y+=dist
    elif ops[0] == "forward":
        x+=dist

print(f"The final answer is {x*y}")
    