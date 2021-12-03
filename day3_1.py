import aoc

input = aoc.aoc()

gamma = 0
epsilon = 0

n_bits = len(str(input[0]))

for b in range(0, n_bits):
    count_zero = len(list(filter(lambda input: input[b]=='0', input)))

    dominant_bit = count_zero < int(len(input) / 2)
    gamma+=dominant_bit << (n_bits - 1 - b)
    epsilon+=(not dominant_bit) << (n_bits - 1 - b)


print(f"Gamma: {gamma}\nEpsilon: {epsilon}")
print(f"Gamma: {'{:05b}'.format(gamma)}\nEpsilon {'{:05b}'.format(epsilon)}")
print(f"The power consumption is {epsilon*gamma}")