import sys, os
sys.path.append(os.path.abspath("."))
import aoc

edges = []
nodes = []

for line in aoc.aoc():
    [pos_from, pos_to] = line.split("-")
    nodes += [pos_from, pos_to]
    edges.append((pos_from, pos_to))

nodes = list(set(nodes))

graph = {}

for node in nodes:
    graph[node] = list(map(lambda edge: edge[1] if edge[0] == node else edge[0], filter(lambda edge: edge[0] == node or edge[1] == node, edges)))


def find_paths(position, end, graph, to_be_visited_twice, visited = [], path = [], completed_paths = []):
    path.append(position)

    if position == end:
        completed_paths.append(path)
        return path

    possible_next = list(
        filter(
            lambda connection:
             connection not in visited
              or
            (
                len(list(filter(lambda c: c == connection, visited))) == 1 
                and connection == to_be_visited_twice
            )
        , graph[position]))

    if position[0].islower():
        visited.append(position)

    paths = []
    for next in possible_next:
        next_paths = find_paths(next, end, graph, to_be_visited_twice, visited[:], path[:], completed_paths)
        if next_paths != []:
            paths.append([next_paths])
    return paths

all_paths = []

for char in list(filter(lambda c : c.islower() and c not in ['start', 'end'], nodes)):
    
    completed_paths = []
    find_paths('start', 'end', graph, char, [], [], completed_paths)
    all_paths += completed_paths

all_paths = list(set(map(lambda desc: "".join(desc), all_paths)))

print(f"There are {len(all_paths)} possible ways.")