import sys, os
sys.path.append(os.path.abspath(".."))
from aoc21 import aoc

input = aoc.aoc()

# Keep shall be true for oxygen and zero for co2
def extract_number(input, keep):
    input = input.copy()
    n_bits = len(input[0])
    for b in range(0, n_bits):
        amount_ones = len(list(filter(lambda input: input[b] == '1', input)))
        amount_zero = len(input) - amount_ones

        dominant_bit = False
        if amount_ones == amount_zero:
            dominant_bit = keep
        else:
            # keep most common
            dominant_bit = amount_ones > amount_zero
            if not keep:
                # keep least common
                dominant_bit = not dominant_bit

        input = list(filter(lambda input: int(input[b]) == int(dominant_bit), input))
        if len(input) <= 1:
            break

    return int(input[0], 2)


o2  = extract_number(input, 1)
co2 = extract_number(input, 0)

print(f"O_2: {o2}\nCO_2: {co2}\nRating: {o2*co2}")