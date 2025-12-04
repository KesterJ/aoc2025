import numpy as np

def get_rolls(file_name):
    with open(file_name, 'r') as input_file:
        rolls = np.array([[1 if char=='@' else 0 for char in line.strip('\n')] for line in input_file])
    return rolls

def add_offsets(roll_map):
    map_height, map_width = roll_map.shape 
    # Create empty array to fill with offsets
    neighbours = np.zeros((map_height, map_width))
    # Add values of north cells
    neighbours[:-1,:] += roll_map[1:,:]
    #South
    neighbours[1:,:] += roll_map[:-1,:]
    #East
    neighbours[:,:-1] += roll_map[:,1:]
    #West
    neighbours[:,1:] += roll_map[:,:-1]
    #NE
    neighbours[:-1,:-1] += roll_map[1:,1:]
    #NW
    neighbours[:-1,1:] += roll_map[1:,:-1]
    #SE
    neighbours[1:,:-1] += roll_map[:-1,1:]
    #SW
    neighbours[1:,1:] += roll_map[:-1,:-1]
    return neighbours

def solve_pt1(roll_map):
    neighbour_map = add_offsets(roll_map)
    return ((neighbour_map < 4) & (roll_map == 1)).sum()

def solve_pt2(roll_map):
    current_map = roll_map.copy()
    finished = False
    while not finished:
        neighbour_map = add_offsets(current_map)
        # Check if all remaining rolls have 4 or more neighbours
        if ((neighbour_map < 4) & (current_map == 1)).any():
            current_map[neighbour_map < 4] = 0
        else:
            finished = True
    return roll_map.sum() - current_map.sum()
    
# Part 1
test_input = get_rolls('day_4_test.txt')
solve_pt1(test_input) == 13
real_input = get_rolls('day_4_input.txt')
total_pt1 = solve_pt1(real_input)

# Part 2
solve_pt2(test_input) == 43
total_pt2 = solve_pt2(real_input)
