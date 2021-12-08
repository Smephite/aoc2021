import sys, os
sys.path.append(os.path.abspath(".."))
from aoc21 import aoc

segment_display = {
    0: ['a', 'b', 'c',      'e', 'f', 'g'],
    1: [          'c',           'f'],
    2: ['a',      'c', 'd', 'e',      'g'],
    3: ['a',      'c', 'd',      'f', 'g'],
    4: [     'b', 'c', 'd',      'f'],
    5: ['a', 'b',      'd',      'f', 'g'],
    6: ['a', 'b',      'd', 'e', 'f', 'g'],
    7: ['a',      'c',           'f'],
    8: ['a', 'b', 'c', 'd', 'e', 'f', 'g'],
    9: ['a', 'b', 'c', 'd',      'f', 'g']
}



# length <=> number map
# 2 = 1
# 3 = 7
# 4 = 4
# 5 = 5,2,3
# 6 = 0, 6, 9
# 7 = 8

numbers = []

for line in aoc.aoc():
    input = line.split(" | ")
    number_signals = input[0].split(" ")

    # There are the numbers uniquely defined
    unique_number_signals = list(filter(lambda w : len(w) in [2, 3, 4, 7], number_signals))
    unique_number_signals.sort(reverse=True)

    signal_number_mapping = {}
    signal_equivalents = {}

    # initialize all possible signals [a-g]
    for i in segment_display[8]:
        signal_number_mapping[i] = []
        signal_equivalents[i] = ''


    for unique_signal_comb in unique_number_signals:
        # the number this signal combination is matched to 
        derrived_number = list(filter(lambda w: len(segment_display[w]) == len(unique_signal_comb), segment_display.keys()))[0]

        for signal in unique_signal_comb:
            signal_number_mapping[signal].append(derrived_number)
    

    # count occurrance of different signals
    for signal in filter(lambda x: len(x) > 0, set(signal_number_mapping.keys())):
        occurrance = len(signal_number_mapping[signal])
        possible_numbers = signal_number_mapping[signal]
        possible_numbers.sort()
        if possible_numbers == [7, 8]:
            # its a! (this is a unique combination)
            signal_equivalents['a'] = signal
    
    # count the occurrance of each signal in the whole input 
    signal_occurrances = dict(map(lambda x: (x, 0), segment_display[8]))

    for signal_comb in number_signals:
        for signal in signal_comb:
            signal_occurrances[signal] += 1
    

    # number of occurrances for each signal
    # e = 4 -- unique
    # b = 6 -- unique
    # d = 7
    # g = 7
    # c = 8
    # a = 8
    # f = 9 -- unique

    # derrive b, e, f from unique occurrance numbers 
    e_candidate = list(filter(lambda x: signal_occurrances[x]==4, signal_occurrances.keys()))
    assert(len(e_candidate) == 1)
    signal_equivalents['e'] = e_candidate[0]
    
    b_candidate = list(filter(lambda x: signal_occurrances[x]==6, signal_occurrances.keys()))
    assert(len(b_candidate) == 1)
    signal_equivalents['b'] = b_candidate[0]

    f_candidate = list(filter(lambda x: signal_occurrances[x]==9, signal_occurrances.keys()))
    assert(len(b_candidate) == 1)
    signal_equivalents['f'] = f_candidate[0]

    # c and a have the same occurrance number but we already know what a is, thus we can derrive c

    c_candidate = list(filter(lambda x: signal_occurrances[x]==8 and not x == signal_equivalents['a'], signal_occurrances.keys()))
    assert(len(c_candidate) == 1)
    signal_equivalents['c'] = c_candidate[0]

    # we are left missing the translation of d and g;
    # luckily they have unique occurrances when only looking at the unique numbers [1, 4, 7, 8] which were derrived previously
    missing = {}
    for missing_signal in filter(lambda s: s not in signal_equivalents.values(), segment_display[8]):
        signal_occurrance_in_unique = len(signal_number_mapping[missing_signal])
            # Signal occurrances in unique numbers
            # 1, 4, 7, 8
            # a 2 [7, 8]
            # b 2 [4, 8]
            # d 2 [4, 8]       - we are interested in n==2
            # e 1 [8]
            # g 1 [8]          - we are interested in n==1
            # c 4 [1, 4, 7, 8]
            # f 4 [1, 4, 7, 8]

        if (signal_occurrance_in_unique == 1):
            signal_equivalents['g'] = missing_signal 
        elif (signal_occurrance_in_unique == 2):
            signal_equivalents['d'] = missing_signal
        else:
            assert(False) # we shouldn't be here...
        
    # create a translation matrix
    backwards_equivalent = dict(map(lambda key: (signal_equivalents[key], key), signal_equivalents.keys()))

    # translate the input "output numbers" to use the normal signal format
    output_def = ""
    for c in input[1]:
        if c == " ":
            output_def += " "
        else:
            output_def += backwards_equivalent[c]
    
    
    number_output = []

    # we now can use our mapping in segment_display to determine the digit displayed in each output
    for number_signals in output_def.split(" "):
        number_signals = list(number_signals)
        number_signals.sort()
        number = list(filter(lambda digit: segment_display[digit] == number_signals, segment_display.keys()))
        assert(len(number) == 1)
        number = number[0]
        number_output.append(number)

    # output is a n digit number
    number = int("".join(map(lambda x: str(x), number_output)))
    numbers.append(number)

# sum them all up
print("The sum of all numbers is", sum(numbers))
