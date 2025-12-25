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
        self.buttons_pressed = [0 for button in self.buttons]
        self.sum_presses = 0
        self.available_buttons = list(self.buttons)
        self.relevant_buttons = [-1 for joltage in self.joltage_targets]
        self.next_target_joltage = -1
        self.steps_to_next_joltage = -1
        self.next_sum_presses = -1
        self.succeeded = False
        self.failed = False
        self.update_available_buttons()
        self.update_joltage_targets()
        
    
    def check_success_failure(self):
        # Fail if any joltage goes below 0, succeed if they're all exactly 0
        if any([target < 0 for target in self.joltage_targets]):
            self.failed = True
        if all([target == 0 for target in self.joltage_targets]):
            self.succeeded = True
        if not (self.failed or self.succeeded):
            # Fail if some joltages are unreachable with available buttons
            if any([(num_buttons == 0) & (target > 0) for num_buttons, target in zip(self.relevant_buttons, self.joltage_targets)]):
                self.failed = True
    
    def update_relevant_buttons(self):
        # Update the list of how many buttons are relevant for each joltage
        unrolled_buttons = [joltage for button in self.available_buttons for joltage in button]
        self.relevant_buttons = [unrolled_buttons.count(i) for i in range(0, len(self.joltage_targets))]
    
    def shortcut_single_button_updates(self, button, times_to_press):
        # Where only one button can affect a joltage, apply it immediately
        which_button = self.buttons.index(button)
        self.buttons_pressed = [presses + times_to_press if i == which_button else presses
                                for i, presses in enumerate(self.buttons_pressed)]
        self.sum_presses += times_to_press
        self.joltage_targets = [target - times_to_press if i in button else target
                                for i, target in enumerate(self.joltage_targets)]
        self.check_success_failure()
        if not (self.failed or self.succeeded):
            self.update_available_buttons()
    
    def update_joltage_targets(self):
        # Shortcut where only one button can affect a joltage
        while any([button == 1 for button in self.relevant_buttons]) & (not (self.failed or self.succeeded)):
            joltage_to_target = self.relevant_buttons.index(1)
            # Find the button which affects that joltage
            # Using next() is OK because there's only one
            button_to_press = next(button for button in self.available_buttons if joltage_to_target in button)
            times_to_press = self.joltage_targets[joltage_to_target]
            self.shortcut_single_button_updates(button_to_press, times_to_press)
        if not (self.failed or self.succeeded):
            # Find which joltage is the one that next requires least combinations to reach
            # Use eq for combinations with replacement to find no of combinations to next
            # joltage - we want easiest one (i.e. least combns)
            # This is greedy but hopefully it'll work out
            steps = [factorial(no_buttons + joltage_reqd - 1)/(factorial(no_buttons - 1) * factorial(joltage_reqd)) if
                     ((joltage_reqd > 0) & (no_buttons > 0)) else 0 for no_buttons, joltage_reqd in zip(self.relevant_buttons, self.joltage_targets)]
            self.steps_to_next_joltage = min([step for step, target in zip(steps, self.joltage_targets) if target > 0])
            self.next_target_joltage = steps.index(self.steps_to_next_joltage)
            self.next_sum_presses = self.joltage_targets[self.next_target_joltage] + self.sum_presses
    
    def update_available_buttons(self):
        # Get indices of joltages which have been reduced to 0
        zero_joltages = [i for i, target in enumerate(self.joltage_targets) if target == 0]
        # Remove buttons which target any zero joltage from those available
        self.available_buttons = [button for button in self.available_buttons
                                             if not any ([joltage in zero_joltages for joltage in button])]
        self.update_relevant_buttons()
        self.check_success_failure()
        
    def press_buttons(self, presses):
        button_counts = [presses.count(self.buttons[i]) for i in range(0, len(self.buttons))]
        self.buttons_pressed = [current_count + new_count for current_count, new_count
                                in zip(self.buttons_pressed, button_counts)]
        self.sum_presses += sum(button_counts)
        # Subtract joltages of pressed buttons from targets
        unrolled_presses = [joltage for button in presses for joltage in button]
        self.joltage_targets = [target - unrolled_presses.count(i) for i, target in enumerate(self.joltage_targets)]
        self.check_success_failure()
        if not (self.failed or self.succeeded):
            self.update_available_buttons()
            self.update_joltage_targets()
        

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

def reach_target_joltages(machine, verbose = True):
    all_machines = [machine]
    current_min = inf
    # Store already calculated combinations for quick lookup
    combns_dict = {}
    while len(all_machines) > 0:
        if verbose:
            print(str(len(all_machines)) + ' possibilities in memory')
        # Extract the machine we want to work on
        stepslist = [mchn.steps_to_next_joltage for mchn in all_machines]
        current_machine = all_machines.pop(stepslist.index(min(stepslist)))
        if verbose:
            print('Current branch presses: ' + str(current_machine.sum_presses))
        # Find subset of buttons we press to get to the next joltage
        buttons_to_use = tuple([button for button in current_machine.available_buttons
                                if current_machine.next_target_joltage in button])
        times_to_press = current_machine.joltage_targets[current_machine.next_target_joltage]
        if verbose:
            print('Finding ' + str(current_machine.steps_to_next_joltage) + ' combinations of ' +
              str(buttons_to_use) + " buttons and " + str(times_to_press) + " presses")
        # Get all the combination that would get there
        if (buttons_to_use, times_to_press) not in combns_dict:
            press_combinations = [combn for combn in
                                  combinations_with_replacement(buttons_to_use,
                                                               times_to_press)]
            combns_dict[(buttons_to_use, times_to_press)] = press_combinations
        else:
            press_combinations = combns_dict[(buttons_to_use, times_to_press)]
        # Add machine for each combination
        min_changed = False
        for counter, combn in enumerate(press_combinations):
            if verbose & (counter % 10000 == 0):
                print('Added ' + str(counter) + ' combinations')
            new_machine = copy.copy(current_machine)
            new_machine.press_buttons(list(combn))
            # Check for whether we've finished and update current min
            if new_machine.succeeded:
                if new_machine.sum_presses < current_min:
                    current_min = new_machine.sum_presses
                    min_changed = True
                    if verbose:
                        print('Found at ' + str(new_machine.sum_presses))
            # Only add it to the test set if it hasn't
            # succeeded or failed, and it wouldn't match or exceed the current min
            # when next worked on
            if ((not new_machine.failed) &
                (not new_machine.succeeded)  & 
                (new_machine.next_sum_presses < current_min)):
                all_machines.append(new_machine)
        # Remove any existing machines that will go higher than a min that was found
        if min_changed:
            all_machines = [mchn for mchn in all_machines if mchn.next_sum_presses < current_min]
    return (current_min)
    

# Test
test = parse_input('day_10_test.txt')
sum([find_min_presses(mchn) for mchn in test]) == 7

# Actuals
input = parse_input('day_10_input.txt')
pt1_answer = sum([find_min_presses(mchn) for mchn in input])

# Part 2
sum([reach_target_joltages(mchn) for mchn in test]) == 33
pt2_answers = []
for i in range(65, 80):
    print('Processing machine ' + str(i))
    start = time.time()
    answer = reach_target_joltages(input[i], verbose = False)
    end = time.time()
    print('Took ' + str(end - start) + ' seconds')
    pt2_answers.append((answer, end - start))