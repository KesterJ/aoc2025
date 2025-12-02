from numpy import cumsum

# Get inputs
with open("day_1_input.txt", "r") as input_file:
    inputs = [line.rstrip('\n')for line in input_file]

# Parse to directions
parsed = [(1 if x[0] == 'R' else - 1) * int(x[1:]) for x in inputs]
parsed.insert(0, 50)

# Get sum
positions = cumsum(parsed)

# Answer
total = sum(positions % 100 == 0)

# Part 2
# Check the different hundred ranges to track clicks
# Because the ranges run X00-X99, we need to account for two special
# cases specifically when going left - if we go left and end on 0, we
# don't change range but should click so we so need to add one; if we
# go left starting from 0, we change range but shouldn't have a new
# click, so we take one away
passes = [abs(position // 100 - positions[i-1] // 100) +
          (1 if ((position < positions[i - 1]) & (position % 100 == 0)) else 0) -
          (1 if ((position < positions[i - 1]) & (positions[i - 1] % 100 == 0)) else 0)
          for i, position in enumerate(positions)][1:]

new_total = sum(passes)

