import sys, os
from typing import List, Tuple
sys.path.append(os.path.abspath("."))
import aoc


Volume = Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int]]

instructions = []

for line in aoc.aoc():
    instrs = line.split(" ")
    modifier = instrs[0] == "on"
    (x, y, z) = instrs[1].split(",")
    x = x[2:]
    y = y[2:]
    z = z[2:]

    (x_start, x_end) = x.split("..")
    (y_start, y_end) = y.split("..")
    (z_start, z_end) = z.split("..")

    x_range = (int(x_start), int(x_end))
    y_range = (int(y_start), int(y_end))
    z_range = (int(z_start), int(z_end))

    instructions.append((modifier, x_range, y_range, z_range))

instructions.reverse()

def define_cube(x : Tuple[int, int], y : Tuple[int, int], z : Tuple[int, int]):
    return(x, y, z)

def get_volume(area : Volume):
    (x, y, z) = area
    
    return (x[1]-x[0]+1)*(y[1]-y[0]+1)*(z[1]-z[0]+1)

def get_intersection(A : Volume, B: Volume):
    if A is None or B is None:
        return None
    (Ax, Ay, Az) = A
    (Bx, By, Bz) = B
    if Ax[1] < Bx[0] or Ax[0] > Bx[1] or Ay[1] < By[0] or Ay[0] > By[1] or Az[1] < Bz[0] or Az[0] > Bz[1]:
        return None

    x_min = max(Ax[0], Bx[0])
    x_max = min(Ax[1], Bx[1])
    y_min = max(Ay[0], By[0])
    y_max = min(Ay[1], By[1])
    z_min = max(Az[0], Bz[0])
    z_max = min(Az[1], Bz[1])
    
    return define_cube((x_min, x_max), (y_min, y_max), (z_min, z_max))


def get_intersect_volume(A : Volume, B : Volume):

    return get_volume(get_intersection(A, B))


def get_intersect_volume_mult(A : Volume, B : List[Volume]):
    if len(B) == 0:
        return 0

    vol = 0
    cut_out = list(sorted(B, key=lambda c : get_volume(c)))

    already_cut_out = []

    for c in cut_out:
        intersect = get_intersection(A, c)
        
        if intersect is None or get_volume(intersect) <= 0: # no_intersection
            continue
        vol += get_volume(intersect) - get_intersect_volume_mult(c, already_cut_out)
        already_cut_out.append(intersect)

    return vol

def bound_number(num, min = -50, max = 50):
    if num < min:
        return min
    if num > max:
        return max
    return num

def out_of_bounds(vals, minB = -50, maxB = 50):
    (min, max) = vals
    return (min < minB and max < minB) or (min > maxB and max > maxB)

written = []

cubes = 0

for ins in instructions:
    (mod, x, y, z) = ins

    area = define_cube(x, y, z)
    if mod: # turn on
        intersect = get_intersect_volume_mult(area, written)
        cubes  += get_volume(area) - intersect
    written.append(area)
        
print("There are", cubes, "cubes on.")