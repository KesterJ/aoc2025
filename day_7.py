def get_manifold(file_name):
    with open(file_name, 'r') as input_file:
        manifold = [line.strip('\n') for line in input_file]
    return manifold

def follow_beam(manifold):
    # Initialise beam position
    beam_pos = [manifold[0].index('S')]
    splits = 0
    for line in manifold[1:]:
        new_beam_pos = []
        for beam in beam_pos:
            if line[beam] == '.':
                new_beam_pos.append(beam)
            elif line[beam] == '^':
                splits += 1
                new_beam_pos.append(beam - 1)
                new_beam_pos.append(beam + 1)
        new_beam_pos = list(set(new_beam_pos))
        beam_pos = new_beam_pos
    return splits

def add_or_insert(dict, key, value):
    # If a key already exists in a dict, increment existing value;
    # If not, create it with the given value
    if key in dict:
        dict[key] += value
    else:
        dict[key] = value

def follow_all_beams(manifold):
    # Initialise beam position
    beam_pos = {manifold[0].index('S'): 1}
    for line in manifold[1:]:
        new_beam_pos = {}
        for beam in beam_pos:
            if line[beam] == '.':
                add_or_insert(new_beam_pos, beam, beam_pos[beam])
            elif line[beam] == '^':
                add_or_insert(new_beam_pos, beam - 1, beam_pos[beam])
                add_or_insert(new_beam_pos, beam + 1, beam_pos[beam])
        beam_pos = new_beam_pos
    total_paths = sum([beam_pos[beam] for beam in beam_pos])
    return total_paths

# Test
test = get_manifold('day_7_test.txt')
follow_beam(test) == 21

# Actual
manifold = get_manifold('day_7_input.txt')
pt1_answer = follow_beam(manifold)

# Part 2
follow_all_beams(test) == 40
pt2_answer = follow_all_beams(manifold)
