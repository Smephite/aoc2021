import sys, os
sys.path.append(os.path.abspath("."))
import aoc

input = aoc.aoc()
starting_comp = input[0]

insertions = {}

for rep in input[2:]:
    [from_comp, insert] = rep.split(" -> ")
    insertions[from_comp] = insert

def next_compound(compound):
    next = ""

    for i in range(len(compound) - 1):
        matching_compounds = list(filter(lambda x : x == compound[i:i+2], insertions.keys()))
        assert(len(matching_compounds) <= 1)

        next += compound[i]

        if len(matching_compounds) != 0:
            next += insertions[matching_compounds[0]]

    next += compound[-1]

    return next

compound = starting_comp

for _ in range(10):
    compound = next_compound(compound)

elements = set(list(compound))
element_count = dict(map(lambda element: (element, len(list(filter(lambda e: e == element, compound)))), elements))

max_element = list(filter(lambda element: element_count[element] == max(element_count.values()), elements))
min_element = list(filter(lambda element: element_count[element] == min(element_count.values()), elements))

print(f"#most_common - #least_common = {element_count[max_element[0]] - element_count[min_element[0]]}")