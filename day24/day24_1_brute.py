import sys, os
sys.path.append(os.path.abspath("."))
import aoc
from itertools import product
from array import * 
import multiprocessing.dummy as mp 
import math

code = aoc.aoc()
def run(number):
    w,x,y,z = 0,0,0,0
    i = 0
#    assert(isinstance(number, str) and len(number) == 14)
    inp_index = 0
    for line in code:
        if line == "":
         #   print(f"{i}:", w, x, y, z)
            i = 0
         #   print("")

        #print(f"{i}:", w, x, y, z)
        i+=1
        sp = line.split(" ")
        instr = sp[0]

        if instr == "inp":
            if inp_index >= len(number):
                print("Warning: Tried to read digit with no input left!")
                break
            val = int(number[inp_index])
            inp_index+=1
            if sp[1] == "w":
                w = val
            elif sp[1] == "x":
                x = val
            elif sp[1] == "y":
                y = val
            elif sp[1] == "z":
                z = val
            else:
                assert(False)
        if instr == "add":
            applier = sp[2]
            if applier in "wxyz":
                if applier == "w":
                    val = w
                elif applier == "x":
                    val = x
                elif applier == "y":
                    val = y
                elif applier == "z":
                    val = z
            else:
                val = int(applier)
            if sp[1] == "w":
                w += val
            elif sp[1] == "x":
                x += val
            elif sp[1] == "y":
                y += val
            elif sp[1] == "z":
                z += val
        if instr == "mul":
            applier = sp[2]
            if applier in "wxyz":
                if applier == "w":
                    val = w
                elif applier == "x":
                    val = x
                elif applier == "y":
                    val = y
                elif applier == "z":
                    val = z
            else:
                val = int(applier)
            if sp[1] == "w":
                w *= val
            elif sp[1] == "x":
                x *= val
            elif sp[1] == "y":
                y *= val
            elif sp[1] == "z":
                z *= val
        if instr == "div":
            applier = sp[2]
            if applier in "wxyz":
                if applier == "w":
                    val = w
                elif applier == "x":
                    val = x
                elif applier == "y":
                    val = y
                elif applier == "z":
                    val = z
            else:
                val = int(applier)
            if sp[1] == "w":
                w = int(w/val)
            elif sp[1] == "x":
                x = int(x/val)
            elif sp[1] == "y":
                y = int(y/val)
            elif sp[1] == "z":
                z = int(z/val)
        if instr == "mod":
            applier = sp[2]
            if applier in "wxyz":
                if applier == "w":
                    val = w
                elif applier == "x":
                    val = x
                elif applier == "y":
                    val = y
                elif applier == "z":
                    val = z
            else:
                val = int(applier)
            if sp[1] == "w":
                w %= val
            elif sp[1] == "x":
                x %= val
            elif sp[1] == "y":
                y %= val
            elif sp[1] == "z":
                z %= val
        if instr == "eql":
            applier = sp[2]
            if applier in "wxyz":
                if applier == "w":
                    val = w
                elif applier == "x":
                    val = x
                elif applier == "y":
                    val = y
                elif applier == "z":
                    val = z
            else:
                val = int(applier)

            if sp[1] == "w":
                w = (1 if val == w else 0)
            elif sp[1] == "x":
                x = (1 if val == x else 0)
            elif sp[1] == "y":
                y = (1 if val == y else 0)
            elif sp[1] == "z":
                z = (1 if val == z else 0)
    return (w,x,y,z)

valid = []

for n in product(list("987654321"), repeat=14):
    txt = "".join(list(n))
    
    val = int(txt)
    if run(txt)[3] == 0:
        print(txt, "is valid!")
        break