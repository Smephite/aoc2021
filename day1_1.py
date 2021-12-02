import aoc

input = aoc.aoc()

larger = 0
last_value = None

for line in input:
    value = int(line)
    if last_value != None:
        if last_value < value:
            larger += 1
    last_value = value

print(f'We got {larger} values larger than their previous.')