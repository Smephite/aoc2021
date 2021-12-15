import sys, os
sys.path.append(os.path.abspath("."))
import aoc

import heapq

class Node:
    def __init__(self, position, risk_level) -> None:
        self.distance = None
        self.previous = None
        self.position = position
        self.risk_level = risk_level
        self.visited = False

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return f"Node[{self.position}, {self.risk_level}, {self.distance}, {self.previous.position if self.previous is not None else None}]"

    
    def get_min_distance(self) -> int:
        return self.distance
    def get_previous_node(self):
        return self.previous

input = aoc.aoc()

nodes = {}

for y in range(len(input)):
    for x in range(len(input[0])):
        for xx in range(5):
            for yy in range(5):
                pos = (x + xx*len(input[0]), y+yy*len(input))
                value = int(input[y][x]) + xx + yy
                if value > 9:
                    value-=9
                node = Node(pos, value)
                nodes[pos] = node

nodes[(0, 0)].distance = 0

pos_output = (len(input)*5-1, len(input[0])*5-1)

to_explore = []

heapq.heapify(to_explore)

to_explore.append((0, (0, 0))) # add starting node

while True:

    current_node = None
    while current_node == None:
        current_node = heapq.heappop(to_explore)
        if current_node == None:
            break # empty
        if nodes[current_node[1]].visited:
            current_node = None

    if current_node == None:
        print(f"There is no path!")
        break

    current_node = nodes[current_node[1]]

    if current_node.position == pos_output:
        break

    current_node.visited = True

    position = current_node.position

    for pos in (position[0], position[1]+1), (position[0], position[1]-1), (position[0]+1, position[1]), (position[0]-1, position[1]):
        if pos not in nodes:
            continue

        n = nodes[pos]

        dist = current_node.distance + n.risk_level

        if n.distance != None and n.distance < dist:
            continue
        
        n.previous = current_node
        n.distance = dist
        
        heapq.heappush(to_explore, (dist, n.position))

print(f"The lowest total risk is {nodes[pos_output].distance}")