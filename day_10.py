import re
import copy
from math import factorial
from itertools import combinations, combinations_with_replacement
from functools import reduce

class Machine:
    # Stores target and buttons as input, but also as numbers which can be
    # manipulated with bitwise operations
    def __init__(self, target, buttons, joltage):
        self.target = target
        self.target_bw = sum([2**i for i, chr in enumerate(target) if chr =='#'])
        self.buttons = [tuple([int(i) for i in button.split(',')]) for button in buttons]
        self.buttons_bw = [sum([2**i for i in button]) for button in self.buttons]
        self.joltage_targets = [int(i) for i in joltage.split(',')]
        self.buttons_pressed = [0 for button in self.buttons]
        self.available_buttons = list(self.buttons)
        self.update_available_buttons()
        self.next_target_joltage = -1
        self.steps_to_next_joltage = -1
        self.update_joltage_targets()
        
    def update_joltage_targets(self):
        # Find which joltage is the one that next requires least combinations to reach
        unrolled_buttons = [joltage for button in self.available_buttons for joltage in button]
        relevant_buttons = [unrolled_buttons.count(i) for i in range(0, len(self.joltage_targets))]
        # Use eq for combinations with replacement to find no of combinations to next
        # joltage - we want easiest one (i.e. least combns)
        # This is greedy but hopefully it'll work out
        steps = [factorial(no_buttons + joltage_reqd - 1)/(factorial(no_buttons - 1) * factorial(joltage_reqd)) if
                 joltage_reqd > 0 else 0 for no_buttons, joltage_reqd in zip(relevant_buttons, self.joltage_targets)]
        self.steps_to_next_joltage = min([step for step, target in zip(steps, self.joltage_targets) if target > 0])
        self.next_target_joltage = steps.index(self.steps_to_next_joltage)        
    
    def update_available_buttons(self):
        # Get indices of joltages which have been reduced to 0
        zero_joltages = [i for i, target in enumerate(self.joltage_targets) if target <= 0]
        # Remove buttons which target any zero joltage from those available
        self.available_buttons = [button for button in self.available_buttons
                                             if not any ([joltage in zero_joltages for joltage in button])]
    
    def press_buttons(self, presses):
        button_counts = [presses.count(self.buttons[i]) for i in range(0, len(self.buttons))]
        self.buttons_pressed = [current_count + new_count for current_count, new_count
                                in zip(self.buttons_pressed, button_counts)]
        # Subtract joltages of pressed buttons from targets
        unrolled_presses = [joltage for button in presses for joltage in button]
        for joltage_index in range(0, len(self.joltage_targets)):
            self.joltage_targets[joltage_index] -= unrolled_presses.count(joltage_index)
        

def parse_input(file_name):
    with open(file_name, 'r') as input_file:
        lines = [line for line in input_file]
        machines = [Machine(target = re.findall('\[(.*)\]', line)[0],
                            buttons = re.findall('\((.*?)\)', line),
                            joltage = re.findall('\{(.*)\}', line)[0]) for line in lines]
    return machines

def presses_result(buttons):
    # Applies bitwise XOR to all buttons in the set
    return reduce(lambda x,y: x^y, buttons)

def find_min_presses(current_machine):
    for i in range(1, len(current_machine.buttons_bw) + 1):
        # Get result of all button press combinatiosn of length i
        results = [presses_result(list(combn)) for combn in combinations(current_machine.buttons_bw, i)]
        if any([result == current_machine.target_bw for result in results]):
            return i
    # Return None as an error code (i.e. we didn't get to the target)
    return None

def reach_target_joltages(machine):
    all_machines = [machine]    
    # I mean this is terrible but we escape it by returning a value
    while True:
        # Extract the machine we want to work on
        stepslist = [mchn.steps_to_next_joltage + sum(mchn.buttons_pressed) for mchn in all_machines]
        current_machine = all_machines.pop(stepslist.index(min(stepslist)))
        # Find subset of buttons we press to get to the next joltage
        buttons_to_use = [button for button in current_machine.available_buttons
                          if current_machine.next_target_joltage in button]
        times_to_press = current_machine.joltage_targets[current_machine.next_target_joltage]
        # Get all the combination that would get there and add copies of machine for each
        press_combinations = combinations_with_replacement(buttons_to_use,
                                                           times_to_press)
        # Add machines but only if they don't have the same button presses as another
        # (only need to check those with same total number of presses) and they don't
        # have any joltages that have been reduced below 0
        total_presses = times_to_press + sum(current_machine.buttons_pressed)
        existing_presses = [mchn.buttons_pressed for mchn in all_machines if sum(mchn.buttons_pressed) == total_presses]    
        for i, combn in enumerate(press_combinations):
            new_machine = copy.deepcopy(current_machine)
            new_machine.press_buttons(list(combn))
            # Check for whether we've finished
            if all([target == 0 for target in new_machine.joltage_targets]):
                    return sum(new_machine.buttons_pressed)
            if (new_machine.buttons_pressed not in existing_presses) & (
                    all([target >= 0 for target in new_machine.joltage_targets])):
                new_machine.update_available_buttons()
                # Do another check after button update that all joltages can be reached
                # by existing buttons
                if all(([i in 
                         [joltage for button in new_machine.available_buttons for joltage in button] for 
                         i, target in enumerate(new_machine.joltage_targets) if target > 0])):
                    new_machine.update_joltage_targets()
                    all_machines.append(new_machine)
                    existing_presses.append(new_machine.buttons_pressed)
    

# Test
test = parse_input('day_10_test.txt')
sum([find_min_presses(mchn) for mchn in test]) == 7

# Actuals
input = parse_input('day_10_input.txt')
pt1_answer = sum([find_min_presses(mchn) for mchn in input])

# Part 2
sum([reach_target_joltages(mchn) for mchn in test]) == 33
