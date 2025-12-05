def parse_inputs(file_name):
    with open(file_name, 'r') as input_file:
        lines = [line.strip('\n') for line in input_file]
    split_loc = lines.index('')
    ranges = [[int(id) for id in (line.split('-'))] for line in lines[:split_loc]]
    ingredients = [int(id) for id in lines[split_loc + 1:]]
    return (ranges, ingredients)

def check_fresh(id, ranges):
    for id_range in ranges:
        if (id >= id_range[0]) & (id <= id_range[1]):
            return True
    return False

def check_ingredients(ingredients, ranges):
    is_fresh = [check_fresh(ingredient, ranges) for ingredient in ingredients]
    return sum(is_fresh)

def get_all_fresh(ranges):
    ranges.sort()
    i = 0
    # Remove overlaps
    while i < len(ranges) - 1:
        # Check for overlap
        if ranges[i][1] >= ranges[i+1][0]:
            ranges[i][1] = max(ranges[i][1], ranges[i+1][1])
            ranges.pop(i+1)
        else:
            i += 1
    # Get coverage
    return sum([id_range[1] - id_range[0] + 1 for id_range in ranges])

# Checks
test_ranges, test_ingredients = parse_inputs('day_5_test.txt')
check_ingredients(test_ingredients, test_ranges) == 3

# Part 1
ranges, ingredients = parse_inputs('day_5_input.txt')
pt1_answer = check_ingredients(ingredients, ranges)

# Part 2
get_all_fresh(test_ranges) == 14
pt2_answer = get_all_fresh(ranges)
