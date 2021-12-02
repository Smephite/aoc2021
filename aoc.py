import sys
from typing import List

def aoc() -> List[str]:
    fileName = ""
    if len(sys.argv) == 2:
        fileName = str(sys.argv[1])
    else:
        fileName = input("Path to puzzle input: ")
    raw_input = []
    with open(fileName) as file:
        for line in file.readlines():
            line = line.replace("\n", "")
            raw_input.append(line)
    return raw_input