import sys, os
sys.path.append(os.path.abspath("."))
import aoc
from itertools import product
from array import * 
import multiprocessing.dummy as mp 

code = aoc.aoc()

w,x,y,z, inp = 0, 0, 0, 0, 13

final = ""

def indexed(c, current=False):
    global w,x,y,z
    if current:
        if c=='w':
            return f"w{w}"
        if c=='x':
            return f"x{x}"
        if c=='y':
            return f"y{y}"
        if c=='z':
            return f"z{z}"
        else:
            return c

    if c=='w':
        w+=1
        return f"w{w-1}"
    if c=='x':
        x+=1
        return f"x{x-1}"
    if c=='y':
        y+=1
        return f"y{y-1}"
    if c=='z':
        z+=1
        return f"z{z-1}"
    else:
        return c

for ins in reversed(code):
    ins = ins.split(" ")

    target = indexed(ins[1])

    if ins[0] == "inp":
        val = f"in[{inp}]"
        inp -=1
    elif ins[0] == "add":
        val = f"({indexed(ins[1], True)} + {indexed(ins[2], True)})"
    elif ins[0] == "mul":
        val = f"{indexed(ins[1], True)} * {indexed(ins[2], True)}"
    elif ins[0] == "div":
        val = f"{indexed(ins[1], True)} / {indexed(ins[2], True)}"
    elif ins[0] == "mod":
        val = f"({indexed(ins[1], True)} % {indexed(ins[2], True)})"
    elif ins[0] == "eql":
        val = f"(1 if {indexed(ins[2], True)} == {indexed(ins[1])} else 0)"
    else:
        print(ins)
        assert(False)
    
    if final == "":
        final = f"{target} = {val}"
    else:
        final = final.replace(target, val)
print(final)