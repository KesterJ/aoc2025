from math import prod

def parse_worksheet_pt1(file_name):
    with open(file_name, 'r') as input_file:
        lines = [line.split() for line in input_file]
        problems = [i for i in zip(*lines)]
    return problems

def solve_problem(problem):
    numbers = [int(i) for i in problem[:-1]]
    operation = problem[-1]
    if operation == '+':
        return sum(numbers)
    elif operation == '*':
        return prod(numbers)

# Test case    
test_problems = parse_worksheet_pt1('day_6_test.txt')
sum([solve_problem(problem) for problem in test_problems]) == 4277556

# Actual
problems = parse_worksheet_pt1('day_6_input.txt')
pt1_answer = sum([solve_problem(problem) for problem in problems])

def parse_worksheet_pt2(file_name):
    with open(file_name, 'r') as input_file:
        lines = [line.strip('\n')[::-1] for line in input_file]
    columns = [list(x) for x in zip(*lines)]
    problems = []
    problem = []
    for column in columns:
        if not all(char == ' ' for char in column):
            # Add number part of column
            problem.append(''.join(column[:-1]))
            # If operator, add it and move onto new problem
            if column[-1] in ['+', '*']:
                problem.append(column[-1])
                problems.append(problem)
                problem = []
    return problems

# Test
test_problems_2 = parse_worksheet_pt2('day_6_test.txt')    
sum([solve_problem(problem) for problem in test_problems_2]) == 3263827

# Actual
problems_2 = parse_worksheet_pt2('day_6_input.txt')
pt2_answer = sum([solve_problem(problem) for problem in problems_2])