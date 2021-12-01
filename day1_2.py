import sys

fileName = ""
if len(sys.argv) == 2:
    fileName = str(sys.argv[1])
else:
    fileName = input("Path to puzzle input: ")

with open(fileName) as file:
    larger = 0
    values = [None, None, None]
    last_value = None
    
    for line in file.readlines():
        line = line.replace("\n", "")
        value = int(line)
        current_added = None
        for (k,v) in enumerate(values):
            was_empty = v is None
            if v is None:
                values[k] = []
            values[k].append(value)
            if was_empty:
                break # fill first 3 values only into corret arrays
        
        current_added = None

        for v in values:
            if v is None:
                continue
            if len(v) == 3:
                current_added = sum(v)
                v.clear()
                break
        if last_value != None and current_added != None:
            if last_value < current_added:
                larger+=1
        if current_added != None:
            last_value = current_added
    print(f'We got {larger} values larger than their previous.')