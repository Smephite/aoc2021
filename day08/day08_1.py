import sys, os
sys.path.append(os.path.abspath(".."))
from aoc21 import aoc

encounters = 0

for line in aoc.aoc():
    input = line.split(" | ")
    output_number_def = input[1].split(" ")
    for signals in output_number_def:
        if len(signals) in [2, 3, 4, 7]:
            encounters+=1

print(f"We have {encounters} unique numbers")