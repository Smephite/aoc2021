import sys, os
sys.path.append(os.path.abspath("."))
import aoc

input = aoc.aoc()
starting_comp = input[0]

insertions = {}

def combine_dict(dict1, dict2):
    out = {}

    for k in set(list(dict1.keys()) + list(dict2.keys())):
        if k in dict1.keys() and k in dict2.keys():
            out[k] = dict1[k] + dict2[k]
        elif k in dict1.keys():
            out[k] = dict1[k]
        else:
            out[k] = dict2[k]
    return out

for rep in input[2:]:
    [from_comp, insert] = rep.split(" -> ")
    insertions[from_comp] = insert


cache = {}

def return_elements_between(A, B, max_depth, depth=0):
    if A+B+str(depth) in cache.keys():
        return cache[A+B+str(depth)]

    if A+B not in insertions or depth == max_depth:
        cache[A+B+str(depth)] = {}
        return {}
    
    left = return_elements_between(A, insertions[A+B], max_depth, depth+1)
    right = return_elements_between(insertions[A+B], B, max_depth, depth+1)

    comb = combine_dict(combine_dict(left, right), {insertions[A+B]: 1})

    cache[A+B+str(depth)] = comb
    
    return comb


elements = {}

depth = 40

for i in range(len(starting_comp)-1):
    elem = return_elements_between(starting_comp[i], starting_comp[i+1], depth)
    elem = combine_dict(elem, {starting_comp[i]: 1})
    elements = combine_dict(elements, elem)

elements = combine_dict(elements, {starting_comp[-1]: 1})


print(f"#most_common - #least_common = {max(elements.values())-min(elements.values())}")