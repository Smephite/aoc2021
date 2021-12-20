import sys, os
from typing import Tuple, Union
sys.path.append(os.path.abspath("."))
import aoc

input = aoc.aoc()

img_filter = list(map(lambda k: k=='#', input[0]))

class Picture:
    lit_pixels   : list[tuple[int, int]]
    known_pixels : list[tuple[int, int]]
    default      : bool
    def __init__(self, lit_pixels, known_pixels = None, default = False) -> None:
        self.lit_pixels = lit_pixels
        if known_pixels == None:
            self.known_pixels = list(lit_pixels)
        else:
            self.known_pixels = known_pixels
        self.default = default

assert(len(img_filter) == 512)

picture = Picture([])


line_index = 0
for line in input[1:]:
    if line == "":
        continue
    col_index = 0
    for c in list(line):
        if c == '#':
            picture.lit_pixels.append((col_index, line_index))
        picture.known_pixels.append((col_index, line_index))
        col_index+=1
    line_index+=1


def get_area(pos : Tuple[int, int]) -> list[Tuple[int, int]]:
    neigh = [(pos[0]+x, pos[1]+y) for y in range(-1, 2) for x in range(-1, 2)]
    return neigh

def area_to_binary(pos : Union[Tuple[int, int],list[Tuple[int, int]]], image : Picture) -> int:
    pixels = pos if isinstance(pos, list) else get_area(pos)
    assert(len(pixels) == 9)
    num = 0
    for index in range(0, 9):
        num = num << 1
        if pixels[index] in image.lit_pixels or (pixels[index] not in image.known_pixels and image.default):
            num += 1
    return num 
    

def enhance_pixel(old_picture : Picture, new_picture : Picture, pixel : Tuple[int, int], filter: list[bool], depth = 0):
    if depth > 1 or pixel in new_picture.known_pixels:
        return

    area = get_area(pixel)
    filter_val = filter[area_to_binary(area, old_picture)]
    new_picture.known_pixels.append(pixel)
    if filter_val:
        new_picture.lit_pixels.append(pixel)

    for p in area:
        if p in old_picture.known_pixels:
            continue
        enhance_pixel(old_picture, new_picture, p, filter, depth+1)

    


    pass

def enhance_picture(picture: Picture, filter: list[bool]):
    unlit_area = filter[0]
    lit_area = filter[0x1ff]
    sourrounding = False
    if picture.default:
        sourrounding = lit_area # by default everything will be lit thus every unchanged sector will return 0x1ff 
                                # therefore the next default will be filter[0x1ff]
    else:
        sourrounding = unlit_area # opposite to above

    next_picture = Picture([], None, sourrounding)

    for pixel in picture.known_pixels:
        enhance_pixel(picture, next_picture, pixel, filter)
    
    return next_picture

def print_picture(picture: Picture):
    min_x = min(picture.known_pixels, key=lambda p: p[0])[0]
    max_x = max(picture.known_pixels, key=lambda p: p[0])[0]
    min_y = min(picture.known_pixels, key=lambda p: p[1])[1]
    max_y = max(picture.known_pixels, key=lambda p: p[1])[1]

    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if (x, y) in picture.lit_pixels:
                print("#", end="")
            else:
                print(".", end="")
        print("")

for i in range(50):
    print(i)
    #print_picture(picture)
    picture = enhance_picture(picture, img_filter)
    #print("======")
print(len(picture.lit_pixels))
