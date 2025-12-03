def get_input(file_loc):
    with open(file_loc, 'r') as input_file:
        banks = [[int(char) for char in line.strip('\n')] for line in input_file]
    return banks
        
def get_joltage_pt1(bank):
    # Get index of first max digit that isn't in last position
    first_digit_loc = bank[:-1].index(max(bank[:-1]))
    first_digit = bank[first_digit_loc]
    # Now can take second digit from everything to the right
    second_digit = max(bank[first_digit_loc + 1:])
    return first_digit * 10 + second_digit

def get_joltage_pt2(bank):
    digits = []
    current_digit_loc = 0
    # Same logic as in the first part function but repeated more times
    # We end up with the digits in our list in reverse
    for i in range(-11, 0):
        current_digit = max(bank[current_digit_loc:i])
        current_digit_loc += bank[current_digit_loc:i].index(current_digit) + 1
        digits.append(current_digit)
    # Last digit done separately as we need different indexing style
    # and don't need to find its location
    current_digit = max(bank[current_digit_loc:])
    digits.append(current_digit)
    # multiply and add up digits 
    total = sum([(10 ** (11 -j)) * digit for j, digit in enumerate(digits)])
    return total

# Run
test_input = get_input('day_3_test.txt')
test_answer = [get_joltage_pt1(bank) for bank in test_input]
# Check test answer
sum(test_answer) == 357

# Actuals
input = get_input('day_3_input.txt')
answer = [get_joltage_pt1(bank) for bank in input]
total = sum(answer)

# Part 2
test_answer_2 = [get_joltage_pt2(bank) for bank in test_input]
# Check test answer
sum(test_answer_2) == 3121910778619

# Actuals
answer_2 = [get_joltage_pt2(bank) for bank in input]
total_2 = sum(answer_2)