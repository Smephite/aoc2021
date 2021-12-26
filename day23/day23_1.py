import sys, os
sys.path.append(os.path.abspath("."))
import aoc

from functools import cache

input = aoc.aoc()
alphabet = list("ABCDEFGHIJKLMONOPQRSTUVWXYZ")
alphabet_map = dict(map(lambda x: (alphabet[x], x), range(len(alphabet))))

values = dict(map(lambda x: (alphabet[x], 10**x), range(len(alphabet))))

len_depth = len(input)-3
rooms = []
hallway = input[1][1:-1]
for c in range(len(input[0])):
    if input[2][c] == '#':
        continue
    room = []
    for b in range(len_depth):
        char = input[b+2][c]
        room.append(char)
    rooms.append(room)


def get_plan(hallway, rooms):
    str = ""
    for _ in range(len(hallway)+2):
        str += "#"
    str +="\n#"
    
    for h in range(len(hallway)):
        str += hallway[h]
    str +="#\n###"
    for r in range(len(rooms)):
        str+=(f"{rooms[r][0]}#")
    str+="##\n"
    for d in range(1, len(rooms[0])):
        str+="  "
        for r in range(len(rooms)):
            str+=f"#{rooms[r][d]}"
        str+="#\n"
    str+="  "

    for _ in range(2*len(rooms)+1):
        str+="#"
    return str
def distance(x_from, y_from, x_to, y_to):
    if x_from == x_to:
        dist = abs(y_from-y_to)
    elif y_from == y_to and y_from == 0:
        dist = abs(x_from, x_to)
    else:
        dist= y_from + y_to + abs(x_from-x_to)

    return dist

def get_room_x(room):
    return 2 + room*2

def may_move(from_p, to_p, hallway):
    
    if from_p[0] > to_p[0]:
        tmp = from_p
        from_p = to_p
        to_p = (tmp[0], tmp[1])
    else:
        from_p = (from_p[0]+1, from_p[1])
        to_p = (to_p[0]+1, to_p[1])
#    print(hallway[from_p[0]:to_p[0]], from_p, to_p)
    return not any(map(lambda b : b != '.', hallway[from_p[0]:to_p[0]]))

def get_moveable_pos(hallway, rooms):
    moves = []
    for rr in range(len(rooms)):
        r = rooms[rr]
        room_x = get_room_x(rr)
        first = r[0]
        scnd = r[1]
        
        possible_hallways = []
        # first is empty we are able to move the first
        for i in range(room_x-1, -1, -1):
            if i%2 == 0 and i != 0: # in front of room
                continue
            if hallway[i] != '.':
                break # blocked by other
            possible_hallways.append(i)
        for i in range(room_x+1, len(hallway)):
            if i%2 == 0 and i != len(hallway)-1: # in front of room
                continue
            if hallway[i] != '.':
                break # blocked by other
            possible_hallways.append(i)
            

        if first == '.':
            if scnd == '.':
                # scnd is also empty
                continue
            if alphabet_map[scnd] == rr:
                continue # is already in the correct room


            for h in possible_hallways:
                moves.append(((room_x, 2), (h, 0)))
            if rooms[alphabet_map[scnd]][1] == '.' and may_move((room_x, 2), (get_room_x(alphabet_map[scnd]), 2), hallway):
                # can move into correct room 2nd slot
                moves.append(((room_x, 2), (get_room_x(alphabet_map[scnd]), 2)))
            elif (rooms[alphabet_map[scnd]][1] == scnd and rooms[alphabet_map[scnd]][0]) == '.'  and may_move((room_x, 2), (get_room_x(alphabet_map[scnd]), 1), hallway):
                # can move into correct room 1st slot
                moves.append(((room_x, 2), (get_room_x(alphabet_map[scnd]), 1)))
        else:
            assert(scnd != '.') # first should not be filled before 2nd

            if scnd == first and alphabet_map[scnd] == rr: # both are correctly placed
                continue

            # else we need to move
            for h in possible_hallways:
                moves.append(((room_x, 1), (h, 0)))
#            print(r, rooms[alphabet_map[first]])
            if rooms[alphabet_map[first]][1] == '.'  and may_move((room_x, 1), (get_room_x(alphabet_map[first]), 2), hallway):
                # can move into correct room 2nd slot
                moves.append(((room_x, 1), (get_room_x(alphabet_map[first]), 2)))
            elif (rooms[alphabet_map[first]][1] == first and rooms[alphabet_map[first]][0]) == '.'  and may_move((room_x, 1), (get_room_x(alphabet_map[first]), 1), hallway):
                # can move into correct room 1st slot
                moves.append(((room_x, 1), (get_room_x(alphabet_map[first]), 1)))
    for i in range(len(hallway)):
        if hallway[i] == '.':
            continue
        corr_room = alphabet_map[hallway[i]]
#        print(i, "->", get_room_x(corr_room), hallway[i], rooms[corr_room])
        if not may_move((i, 0), (get_room_x(corr_room), 0), hallway):
            continue # cannot move to room
        if rooms[corr_room][0] != '.' or (rooms[corr_room][1] != hallway[i] and rooms[corr_room][1] != '.'):
            continue
#        print("Move!")
        if rooms[corr_room][1] == '.':
            moves.append(((i, 0),(get_room_x(corr_room), 2)))
        else:
            moves.append(((i, 0),(get_room_x(corr_room), 1)))


    return moves

def get_char_at(x, y, hallway, rooms):
    if y == 0:
        return hallway[x]
    return rooms[int(x/2)-1][y-1]

def is_solved(rooms):
    for i in range(len(rooms)):
        c = alphabet[i]
        if rooms[i][0] != c or rooms[i][1] != c:
            return False
    return True

def make_move(hallway, rooms, move):
    n_r = [list(row) for row in rooms]
    n_h = list(hallway)
    if move[0][1] == 0:
        # move from hallway
        n_h[move[0][0]] = '.'
        assert(move[1][1] != 0) # we cannot move from hallway to hallway
        n_r[int(move[1][0]/2)-1][move[1][1]-1] = hallway[move[0][0]]
    else:
        # move from room
        n_r[int(move[0][0]/2)-1][move[0][1]-1] = '.'
        if move[1][1] == 0:
            # move to hallway
            n_h[move[1][0]] = rooms[int(move[0][0]/2)-1][move[0][1]-1]
            #print(rooms[int(move[0][0]/2)-1][move[0][1]-1])
        else:
            # move to room
            n_r[int(move[1][0]/2)-1][move[1][1]-1] = rooms[int(move[0][0]/2)-1][move[0][1]-1]
    return (n_h, n_r)

def print_depth(depth, *values):
    if len(values) == 1 and isinstance(values[0], str):
        for s in values[0].split("\n"):
            print("-"*depth + s)

def heuristic(hallway, rooms, move, cost):
    if move[1][1] > 0: # move to room
        return 0
    else:
        return cost


def solve(hallway, rooms, cost = 0, depth=0):

    if depth > 11:
        return None

#    print_depth(depth, get_plan(hallway, rooms))
    if is_solved(rooms):
        print("Solved!", cost)
        return cost


    possible_moves = get_moveable_pos(hallway, rooms)


    if len(possible_moves) == 0:
        return None

    possible_moves = sorted(
        map(lambda data:
         (data, distance(data[0][0], data[0][1], data[1][0], data[1][1]) * values[get_char_at(data[0][0], data[0][1], hallway, rooms)]),
         possible_moves)
        , key=lambda data: heuristic(hallway, rooms, data[0], data[1])
     
    )
#    print(possible_moves)

#    if depth == 0:
#        possible_moves = [(((6, 1), (3, 0)), 40)]
    
#    print_depth(depth, possible_moves)
    #print(possible_moves)
    def rec_value(move, depth):
        (move, new_cost) = move 
        (n_h, n_r) = make_move(hallway, rooms, move)
        return solve(n_h, n_r, cost + new_cost, depth+1)
    mm = list(filter(lambda b: b != None, map(lambda b: rec_value(b, depth), possible_moves)))

    return None if len(mm) == 0 else min(mm)
    


print(solve(hallway, rooms))
#hal = [".", ".", ".", ".",".", "A",".", "D",".", ".","."]
#rms= [[".", "A"], [".", "B"], [".", "C"], [".", "D"]]
#print(get_plan(hal, rms))
#print(get_moveable_pos(hal, rms, []))