from re import search

# Get inputs
with open("day_2_input.txt", "r") as input_file:
    inputs = input_file.readlines()[0].split(',')
    inputs = [input.split('-') for input in inputs]

# Function to find match
def find_repeat(string):
    strlen = len(string)
    if strlen % 2 == 1:
        return False
    elif string[0 : (strlen // 2)] == string[(strlen // 2) : strlen]:
        return True
    else:
        return False

def find_repeat_part2(string):
    if search('^(\\d+)\\1+$', string):
        return True
    else:
        return False

# Get ranges and find matches
matches = []
for input in inputs:
    for id in range(int(input[0]), int(input[1]) + 1):
        if find_repeat(str(id)):
            matches.append(id)
            
part_1 = sum(matches)

matches_2 = []
for input in inputs:
    for id in range(int(input[0]), int(input[1]) + 1):
        if find_repeat_part2(str(id)):
            matches_2.append(id)
            
part_2 = sum(matches_2)


