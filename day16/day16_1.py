import sys, os
sys.path.append(os.path.abspath("."))
import aoc
import math
input = bytes.fromhex(aoc.aoc()[0])
    

version_sum = 0

def decode_package(input, index, depth = 0):
    global version_sum

    version = int(input[index:index+3], 2)
    id = int(input[index+3:index+6], 2)
    
    version_sum += version

    index = index+6

    prefix = "".join([" " for _ in range(depth)])


    if id == 4:
        # decode number
        num = 0
        index_bit = int(input[index])
        while True:
            num = num << 4
            current_bits = int(input[index+1:index+5], 2)
            num += current_bits
            index+=5

            if index_bit == 0:
                break
            index_bit = int(input[index])
        #print(f"{prefix} v{version} @ {id} -> {num}")
        
        return (index, num)
    else:
        length_type_id = int(input[index])
        if length_type_id == 0:
            # fixed length
            total_length = int(input[index+1:index+16], 2)
            #print(f"{prefix} v{version} @ {id} -> {length_type_id}; {total_length}")
            
            new_index = index+16
            while (index+16+total_length - new_index) > 10:
                (new_index, data) = decode_package(input, new_index, depth+1)

            index = new_index

        elif length_type_id == 1:
            # fixed num packets
            num_packets = int(input[index+1:index+12], 2)
            #print(f"{prefix} v{version} @ {id} -> {length_type_id}; {num_packets}")
            new_index = index+12
            for _ in range(0, num_packets):
                (new_index, data) = decode_package(input, new_index, depth+1)
            index = new_index





    return (index, 0)

in_str = bin(int.from_bytes(input, "big"))[2:]

while len(in_str) % 4 != 0:
    in_str = "0" + in_str

decode_package(in_str, 0)


print("The version sum is", version_sum)