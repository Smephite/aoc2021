import sys, os
sys.path.append(os.path.abspath(".."))
from aoc21 import aoc


opening = ['(', '{', '[', '<']
matches = {'(':')', '{':'}', '[':']', '<':'>'}

scores = {')':1, ']':2, '}':3, '>':4}

score_list = []


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
    
    if illegal is not None:
        continue
    
    closing = []

    chunk.reverse()

    for c in chunk:
        closing.append(matches[c])
    
    local_score = 0

    for c in closing:
        local_score*=5
        local_score+=scores[c]
    score_list.append(local_score)


score_list.sort()
final_score = score_list[int(len(score_list)/2)]
print(f"Final score {final_score}")