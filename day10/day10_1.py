import sys, os
sys.path.append(os.path.abspath(".."))
from aoc21 import aoc


opening = ['(', '{', '[', '<']
matches = {'(':')', '{':'}', '[':']', '<':'>'}

scores = {')':3, ']':57, '}':1197, '>':25137}

score = 0

for line in aoc.aoc():
    chunk = []
    illegal = None
    for c in list(line):
        if c in opening:
            chunk.append(c)
        else:
            required_closing = matches[chunk.pop()]
            if required_closing != c:
                illegal = c
                break
    
    if illegal is None and len(chunk) != 0:
        continue
    
    if illegal is not None:
        score += scores[illegal]
print(f"Total score: {score}")