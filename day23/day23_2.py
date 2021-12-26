#https://gist.github.com/adah1972/f4ec69522281aaeacdba65dbee53fade
from collections import namedtuple
import functools
import json
import six

Serialized = namedtuple('Serialized', 'json')


def hashable_cache(cache):
    def hashable_cache_internal(func):
        def deserialize(value):
            if isinstance(value, Serialized):
                return json.loads(value.json)
            else:
                return value

        def func_with_serialized_params(*args, **kwargs):
            _args = tuple([deserialize(arg) for arg in args])
            _kwargs = {k: deserialize(v) for k, v in six.viewitems(kwargs)}
            return func(*_args, **_kwargs)

        cached_func = cache(func_with_serialized_params)

        @functools.wraps(func)
        def hashable_cached_func(*args, **kwargs):
            _args = tuple([
                Serialized(json.dumps(arg, sort_keys=True))
                if type(arg) in (list, dict) else arg
                for arg in args
            ])
            _kwargs = {
                k: Serialized(json.dumps(v, sort_keys=True))
                if type(v) in (list, dict) else v
                for k, v in kwargs.items()
            }
            return cached_func(*_args, **_kwargs)
        hashable_cached_func.cache_info = cached_func.cache_info
        hashable_cached_func.cache_clear = cached_func.cache_clear
        return hashable_cached_func

    return hashable_cache_internal


import sys, os
sys.path.append(os.path.abspath("."))
import aoc


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

rooms[0].insert(1, 'D')
rooms[0].insert(1, 'D')
rooms[1].insert(1, 'C')
rooms[1].insert(2, 'B')
rooms[2].insert(1, 'B')
rooms[2].insert(2, 'A')
rooms[3].insert(1, 'A')
rooms[3].insert(2, 'C')



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
    moves_from = []

    for origin_r_id in range(len(rooms)):
        origin_r = rooms[origin_r_id]
        origin_x = get_room_x(origin_r_id)
        first_char = 0
        while first_char < len(origin_r) and origin_r[first_char] == '.':
            first_char += 1
        empty = first_char == len(origin_r)
        if empty:
            continue # we cannot move anything from here
        room_char = origin_r[first_char]
        if origin_r_id == alphabet_map[room_char] and not any(map(lambda c: c != room_char, origin_r[first_char:])):
            continue # we are already correct
        moves_from.append((origin_x, first_char + 1))
    for hallway_id in range(len(hallway)):
        if hallway[hallway_id] == '.':
            continue
        moves_from.append((hallway_id, 0))
    for p_from in moves_from:
        from_char = rooms[int(p_from[0]/2)-1][p_from[1]-1] if p_from[1] != 0 else hallway[p_from[0]]
        target_room_id = alphabet_map[from_char]
        target_room = rooms[target_room_id]

        first_char = 0
        while first_char < len(target_room) and target_room[first_char] == '.':
            first_char += 1
        empty = first_char == len(target_room)

        if first_char != 0: # move into correct room
            
            if empty or not any(map(lambda c: c != from_char,target_room[first_char:])):
                 # room not ready
                p_to = (get_room_x(target_room_id), first_char)
                if may_move(p_from, p_to, hallway):
                    moves.append((p_from, p_to))
        
        if p_from[1] > 0: # we are in a room thus we may move to the hallway
            for i in range(p_from[0]-1, -1, -1):
                if i%2 == 0 and i != 0: # in front of room
                    continue
                if hallway[i] != '.':
                    break # blocked by other
                moves.append((p_from, (i, 0)))
            for i in range(p_from[0]+1, len(hallway)):
                if i%2 == 0 and i != len(hallway)-1: # in front of room
                    continue
                if hallway[i] != '.':
                    break # blocked by other
                moves.append((p_from, (i, 0)))
    
    return moves

def get_char_at(x, y, hallway, rooms):
    if y == 0:
        return hallway[x]
    return rooms[int(x/2)-1][y-1]

def is_solved(rooms):
    for i in range(len(rooms)):
        c = alphabet[i]
        for cc in rooms[i]:
            if cc != c:
                return False

    return True

def make_move(hallway, rooms, move):
    n_r = [list(row) for row in rooms]
    n_h = list(hallway)
    if move[0][1] == 0:
        # move from hallway
        n_h[move[0][0]] = '.'
        assert(n_r[int(move[1][0]/2)-1][move[1][1]-1] == '.')
        assert(move[1][1] != 0) # we cannot move from hallway to hallway
        n_r[int(move[1][0]/2)-1][move[1][1]-1] = hallway[move[0][0]]
    else:
        # move from room
        n_r[int(move[0][0]/2)-1][move[0][1]-1] = '.'
        if move[1][1] == 0:
            assert(n_h[move[1][0]] == '.')
            # move to hallway
            n_h[move[1][0]] = rooms[int(move[0][0]/2)-1][move[0][1]-1]
            #print(rooms[int(move[0][0]/2)-1][move[0][1]-1])
        else:
            # move to room
            assert(n_r[int(move[1][0]/2)-1][move[1][1]-1] == '.')
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
        cost = values[get_char_at(move[0][0], move[0][1], hallway, rooms)]
        dist = distance(move[0][0], move[0][1], move[1][0], move[1][1])
        return cost*dist*dist


mmin = sys.maxsize

@hashable_cache(functools.cache)
def solve(hallway, rooms, cost = 0, depth=0):
    global mmin
    if depth > 30:
        return None

#    print_depth(depth, get_plan(hallway, rooms))
    if is_solved(rooms):
        mmin = min(mmin, cost)
        print("Solved!", cost, mmin)
        return cost


    possible_moves = get_moveable_pos(hallway, rooms)



    #print(get_plan(hallway, rooms))
    #print(possible_moves)

    if len(possible_moves) == 0:
        #print("No Moves!")
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
        #print(f"{move}:")
        (n_h, n_r) = make_move(hallway, rooms, move)
        return solve(n_h, n_r, cost + new_cost, depth+1)
    mm = list(filter(lambda b: b != None, map(lambda b: rec_value(b, depth), possible_moves)))

    return None if len(mm) == 0 else min(mm)
    
print(get_plan(hallway, rooms))

print(solve(hallway, rooms))
#hal = [".", ".",
#   ".",
#       ".",
#   ".",
#       ".",
#   ".",
#       "A",
#   ".",
#       ".","."]
#rms= [["A", "A", "A"], ["B", "B", "B"], ["C", "C", "C"], ["C", "C", "D"]]
#print(get_plan(hal, rms))
#print(get_moveable_pos(hal, rms))