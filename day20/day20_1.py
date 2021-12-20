import sys, os
sys.path.append(os.path.abspath("."))
import aoc

input = aoc.aoc()

img_filter = list(map(lambda k: k=='#', input[0]))

class Picture:
    def __init__(self, pixels, calculated = None, default = False) -> None:
        self.lit_pixels = pixels
        if calculated == None:
            self.calculated = pixels
        else:
            self.calculated = calculated
        self.default = default


assert(len(img_filter) == 512)

image = []
calc = []

line_index = 0
for line in input[1:]:
    if line == "":
        continue
    col_index = 0
    for c in list(line):
        if c == '#':
            image.append((col_index, line_index))
        calc.append((col_index, line_index))
        col_index+=1
    line_index+=1

picture = Picture(image, calc)

def get_neighbours(pos):
    neigh = [(pos[0]+x, pos[1]+y) for y in range(-1, 2) for x in range(-1, 2)]
    return neigh
    
def count_lit(pixels, image) -> int:
    return len(list(filter(lambda p: p in image, pixels)))

def arr_to_binary(pixels, image : Picture) -> int:
    assert(len(pixels) == 9)
    num = 0
    for index in range(0, 9):
        num = num << 1
        if pixels[index] in image.lit_pixels or (pixels[index] not in image.calculated and image.default):
            num += 1

    return num 
    


def enhance_pixel(old_picture: Picture, new_image, pixel, calculated, depth = 0, rec_depth = 0):
    if depth >= 2 or pixel in calculated:
        return
    neighbours = get_neighbours(pixel)
    calculated.append(pixel)
    
    bits = arr_to_binary(neighbours, old_picture)
    if img_filter[bits]:
        new_image.append(pixel)
    
    if bits == 0 or bits == 0x1ff:
        depth += 1


    for n in neighbours:
        if n in old_picture.calculated:
            continue
        enhance_pixel(old_picture, new_image, n, calculated, depth, rec_depth+1)
    
    

def enhance_image(old_picture: Picture):
    new_image = []
    calculated = []
    for pixel in old_picture.calculated:
        enhance_pixel(old_picture, new_image, pixel, calculated)
    
    default = False
    if img_filter[0] and not old_picture.default:
        default = True
    return Picture(new_image, calculated, default)

new_image = enhance_image(picture)
new_image = enhance_image(new_image)
print(len(new_image.lit_pixels))