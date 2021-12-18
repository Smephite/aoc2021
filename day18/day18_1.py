import sys, os
from typing import Union
import math

sys.path.append(os.path.abspath("."))
import aoc

class SnailNumber:

    def __init__(self, left : Union['SnailNumber',int], right : Union['SnailNumber',int], parent : Union[None, 'SnailNumber'] = None) -> None:
        self.left = left
        self.right = right
        self.parent = parent
        self.is_left = None
    
    def update(self):
        self.is_left = self.parent.left == self if self.parent != None else None

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return f"[{self.left},{self.right}]"


    def __add__(self, other):
        num  = SnailNumber(self, other)#.reduce()
        num.left.parent = num
        num.right.parent = num
        num.left.update()
        num.right.update()
        return num.reduce()

    def find_deepest_number(self, target_depth, depth=0):
        if isinstance(self.left, int) and isinstance(self.right, int):
            return None if target_depth > depth else self

        if not isinstance(self.left, int):
            left_search = self.left.find_deepest_number(target_depth, depth+1)
            if left_search != None:
                return left_search
        
        if not isinstance(self.right, int):
            return self.right.find_deepest_number(target_depth, depth+1)
        
        return None
    
    def reduce(self, once=False) -> 'SnailNumber':
        next = self
        while True:
            explode = next.depth() >= 4
            (max_int, max_int_parent) = next.max_regular()
            split = max_int >= 10
            if not explode and not split:
                break
            
            if explode:
                deepest = self.find_deepest_number(4)
                assert(deepest != None) # hmm
                assert(deepest.is_left != None) # else we are the parent node and thus cannot explode (we also shouldn't need to?)

                if not deepest.is_left: # we are on the right of an pair thus we want to add our left number to the right most number of left
                    next_left = deepest.parent.left
                    if isinstance(next_left, int):
                        # first iteration
                        deepest.parent.left = deepest.parent.left + deepest.left
                    else: # find the right most of the left tree
                        while True:
                            if isinstance(next_left.right, int):
                                next_left.right = next_left.right + deepest.left
                                break
                            else:
                                next_left = next_left.right
                    # find next right
                    next_right = deepest
                    # tranverse tree until we are the left element
                    while next_right is not None and not next_right.is_left:
                        next_right = next_right.parent
                    if next_right is not None and next_right.is_left is not None:
                        next_right = next_right.parent
                        # if next_right was None we were the right most element in the tree
                        # now next_right is the parent node of a tree where we want to find the left most of the right branch
                        if isinstance(next_right.right, int): #there is no tree
                            next_right.right = next_right.right + deepest.right
                        else:
                            next_right = next_right.right
                            while True:
                                if isinstance(next_right.left, int):
                                    next_right.left = next_right.left + deepest.right
                                    break
                                else:
                                    next_right = next_right.left # tranverse to the left
                    deepest.parent.right = 0
                else: # we are the left side of an pair
                    next_right = deepest.parent.right
                    # find left most element of the parent.right tree
                    if isinstance(next_right, int):
                        # first iteration
                        deepest.parent.right = deepest.parent.right + deepest.right
                    else:
                        while True:
                            if isinstance(next_right.left, int):
                                next_right.left = next_right.left + deepest.right
                                break
                            else:
                                next_right = next_right.left
                    # find next left
                    next_left = deepest
                    # tranverse there tree until we are the right element
                    while next_left is not None and next_left.is_left:
                        next_left = next_left.parent
                    
                    if next_left is not None and next_left.parent is not None:
                        # if next_left was None we were the left most element in the tree
                        # now next_left is the parent node of a tree where we want to find the right most of the left branch
                        next_left = next_left.parent
                        if isinstance(next_left.left, int):
                            next_left.left = next_left.left + deepest.left
                        else:
                            next_left = next_left.left
                            while True:
                                if isinstance(next_left.right, int):
                                    next_left.right = next_left.right + deepest.left
                                    break
                                else:
                                    next_left = next_left.right
                    deepest.parent.left = 0
            else: #split
                if isinstance(max_int_parent.left, int) and max_int_parent.left == max_int:
                    max_int_parent.left = SnailNumber(math.floor(max_int/2), math.ceil(max_int/2))
                    max_int_parent.left.parent = max_int_parent
                    max_int_parent.left.update()
                elif isinstance(max_int_parent.right, int) and max_int_parent.right == max_int:
                    max_int_parent.right = SnailNumber(math.floor(max_int/2), math.ceil(max_int/2))
                    max_int_parent.right.parent = max_int_parent
                    max_int_parent.right.update()
            
            if once:
                break
        return next
        
            


    def max_regular(self):
        regs = []
        if isinstance(self.left, int):
            if self.left >= 10:
                regs.append((self.left, self))
        else:
            regs.append(self.left.max_regular())
        if isinstance(self.right, int):
            if self.right >= 10:
                regs.append((self.right, self))
        else:
            regs.append(self.right.max_regular())
        
        not_none = list(filter(lambda x:x[1] is not None, regs))
        return not_none[0] if len(not_none) != 0 else (0, None)

    def is_reduced(self):
        return self.depth() < 4 and self.max_regular() < 10

    def depth(self, depth=0):
        depths = [depth]
        if not isinstance(self.left, int):
            depths.append(self.left.depth(depth+1))
        if not isinstance(self.right, int):
            depths.append(self.right.depth(depth+1))
        return max(depths)

    def magnitude(self):
        mag = 0
        if isinstance(self.left, int):
            mag += 3*self.left
        else:
            mag += 3*self.left.magnitude()
        if isinstance(self.right, int):
            mag += 2*self.right
        else:
            mag += 2*self.right.magnitude()
        return mag

def parse_snailnumber(str : str) -> tuple[SnailNumber, str]:
    assert(str[0] == "[") # snail number must be a pair
    str=str[1:]
    if str[0] == "[":
        (left, str) = parse_snailnumber(str)
    else:
        left = int(str.split(",")[0])
        str = str[str.index(","):]
    
    assert(str[0] == ",")
    str=str[1:]
    if str[0] == "[":
        (right, str) = parse_snailnumber(str)
    else:
        right = int(str.split("]")[0])
        str = str[str.index("]"):]
    assert(str[0] == "]")
    str = str[1:]

    nr = SnailNumber(left, right)

    if not isinstance(left, int):
        left.parent = nr
        left.update()
    if not isinstance(right, int):
        right.parent = nr
        right.update()
        

    return (nr, str)

def parse(input: str) -> SnailNumber:
    (number, string) = parse_snailnumber(input)
    assert(string == "")
    return number


num = None

for line in aoc.aoc():
    if num == None:
        num = parse(line)
    else:
        num += parse(line)

print(f"The added magnitude is {num.magnitude()}.")