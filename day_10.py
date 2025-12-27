import re
import copy
from math import factorial, inf
from itertools import combinations, combinations_with_replacement
from functools import reduce
import time

class Machine:
    # Stores target and buttons as input, but also as numbers which can be
    # manipulated with bitwise operations
    def __init__(self, target, buttons, joltage):
        self.target = target
        self.target_bw = sum([2**i for i, chr in enumerate(target) if chr =='#'])
        self.buttons = [tuple([int(i) for i in button.split(',')]) for button in buttons]
        self.buttons_bw = [sum([2**i for i in button]) for button in self.buttons]
        self.joltage_targets = [int(i) for i in joltage.split(',')]
        

def parse_input(file_name):
    with open(file_name, 'r') as input_file:
        lines = [line for line in input_file]
        machines = [Machine(target = re.findall('\[(.*)\]', line)[0],
                            buttons = re.findall('\((.*?)\)', line),
                            joltage = re.findall('\{(.*)\}', line)[0]) for line in lines]
    return machines

def presses_result(buttons):
    if len(buttons) == 0:
        return 0
    else:
        # Applies bitwise XOR to all buttons in the set
        return reduce(lambda x,y: x^y, buttons)

def find_min_presses(current_machine):
    for i in range(1, len(current_machine.buttons_bw) + 1):
        # Get result of all button press combinations of length i
        results = [presses_result(list(combn)) for combn in combinations(current_machine.buttons_bw, i)]
        if any([result == current_machine.target_bw for result in results]):
            return i
    # Return None as an error code (i.e. we didn't get to the target)
    return None

def check_bit(number, position):
    # Checks if the bit in a particular position is set in a number
    if number & (1 << position):
        return True
    else:
        return False

def solve_pt_2(machine):
    #Get odd joltages and bitwise representation
    odds = [True if joltage % 2 == 1 else False for joltage in machine.joltage_targets]
    odds_bw = sum([2**i for i, odd in enumerate(odds) if odd])
    solutions_list = []
    # Find all combinations that reduce odd joltages by 1
    for i in range(0, len(machine.buttons_bw) + 1):
        # Go through of all button press combinations of length i
        for combn in combinations(machine.buttons_bw, i):
            if presses_result(list(combn)) == odds_bw:
                # Decompose bitwise presses into counts for each button
                press_counts = [2**x for btn in list(combn)
                                for x in range(0, len(machine.joltage_targets))
                                if check_bit(btn, x)]
                reductions = [press_counts.count(2**y) for y in range(0, len(machine.joltage_targets))]
                new_joltages = [current - reduction for current, reduction in zip(machine.joltage_targets, reductions)]
                # Only go further if all joltages stayed above 0
                if all([j >= 0 for j in new_joltages]):
                    current_steps = i
                    if all([j == 0 for j in new_joltages]):
                        solutions_list.append(current_steps)
                    else:
                        new_joltages = [j / 2 for j in new_joltages]
                        new_machine = copy.copy(machine)
                        new_machine.joltage_targets = new_joltages
                        extra_steps = solve_pt_2(new_machine)
                        if extra_steps != None:
                            solutions_list.append((2 * extra_steps) + current_steps)
    # Return None if we didn't get a return yet (i.e. impossible)
    breakpoint()
    if len(solutions_list) == 0:
        return None
    else:
        return min(solutions_list)

# Test
test = parse_input('day_10_test.txt')
sum([find_min_presses(mchn) for mchn in test]) == 7

# Actuals
input = parse_input('day_10_input.txt')
pt1_answer = sum([find_min_presses(mchn) for mchn in input])

#Part 2
pt2_answer = []
for i, mchn in enumerate(input):
    print('Machine ' + str(i))
    pt2_answer.append(solve_pt_2(mchn))
total_pt2 = sum(pt2_answer)