import sys

fileName = ""
if len(sys.argv) == 2:
    fileName = str(sys.argv[1])
else:
    fileName = input("Path to puzzle input: ")

with open(fileName) as file:
    last_value = None
    larger = 0
    for line in file.readlines():
        line = line.replace("\n", "")
        value = int(line)
        if last_value != None:
            if last_value < value:
                larger += 1
        last_value = value
    print(f'We got {larger} values larger than their previous.')