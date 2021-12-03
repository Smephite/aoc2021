import aoc

input = aoc.aoc()

gamma = 0
epsilon = 0

n_bits = len(str(input[0]))

for i in range(0, n_bits):
    count_zero = 0
    for line in input:
        count_zero += str(line)[i] == '0'

    dominant_bit = count_zero < int(len(input) / 2)
    gamma+=dominant_bit << (n_bits - 1 - i)
    epsilon+=(not dominant_bit) << (n_bits - 1 - i)


print(f"Gamma: {gamma}\nEpsilon: {epsilon}")
print(f"Gamma: {'{:05b}'.format(gamma)}\nEpsilon {'{:05b}'.format(epsilon)}")
print(f"The power consumption is {epsilon*gamma}")