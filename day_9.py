
def parse_input(file_name):
    with open(file_name, 'r') as input_file:
        lines = [[int(num) for num in line.strip('[]\n').split(',')] for line in input_file]
    return lines

def find_candidates(coords, top = True, left = True):
    # Find all coords in the list that are not strictly worse than others
    # in terms of being a corner
    # (e.g. if a coord N has a coord M that is both above and to the left of it,
    # then N cannot be the top-left as M would always make a bigger rectangle)
    
    # Rather than trying to handle directions differently, transform the grid so
    # we're always looking for top-leftmost
    coords = [[coord[0] if left else -coord[0],
               coord[1] if top else -coord[1]] for coord in coords]
    
    # Sorting coords allows for efficiencies later
    coords.sort()
    
    # Iteratively find candidates
    candidates = []
    while len(coords) > 0:
        # Get leftmost point, and exclude anything not above it - because we're
        # sorted, we know that the first element is both a) leftmost and b)
        # if multiple leftmost points, it's the highest [which is what we want]
        leftest = coords.pop(0)
        coords = [coord for coord in coords if coord[1] < leftest[1]]
        candidates.append(leftest)
    
    # Return to original coord system
    candidates = [[candidate[0] if left else -candidate[0],
                   candidate[1] if top else -candidate[1]] for candidate in candidates]
    
    return candidates

def get_area(coord_1, coord_2):
    # Calculate rectangle - account for each side being at least
    # 1 even when coords line up
    side_1 = abs(coord_1[0] - coord_2[0]) + 1
    side_2 = abs(coord_1[1] - coord_2[1]) + 1
    return side_1 * side_2

def find_rectangles_pt1(coords):
    # Get candidate coords for each corner
    toplefts = find_candidates(coords, top = True, left = True)
    toprights = find_candidates(coords, top = True, left = False)
    bottomlefts = find_candidates(coords, top = False, left = True)
    bottomrights = find_candidates(coords, top = False, left = False)
    # Find biggest rectangles with each pair of opposite corners
    max_rect = 0
    for tl in toplefts:
        for br in bottomrights:
            current_area = get_area(tl, br)
            if current_area > max_rect:
                max_rect = current_area
    for tr in toprights:
        for bl in bottomlefts:
            current_area = get_area(tr, bl)
            if current_area > max_rect:
                max_rect = current_area
                
    return max_rect

def check_path(paths, x_min, x_max, y_min, y_max):
    # Checks if any paths run betwen a given rectangle
    for path in paths:
        # If identical xs, path is vertical
        if path[0][0] == path[1][0]:
            # Only need to check if path overlaps with rectangle in x space
            if (path[0][0] > x_min) & (path[0][0] < x_max):
                path_y_min = min(path[0][1], path[1][1])
                path_y_max = max(path[0][1], path[1][1])
                # Checks ys to see if path starts before or after rectangle
                # If it doesn't, there's overlap
                if not ((path_y_min >= y_max) | (path_y_max <= y_min)):
                    return False
        # Otherwise path is horizontal - repeat logic for opposite direction
        else:
            if (path[0][1] > y_min) & (path[0][1] < y_max):
                path_x_min = min(path[0][0], path[1][0])
                path_x_max = max(path[0][0], path[1][0])
                # Checks ys to see if path starts before or after rectangle
                # If it doesn't, there's overlap
                if not ((path_x_min >= x_max) | (path_x_max <= x_min)):
                    return False
    # If we didn't return false anywhere, must be no overlap
    return True

def get_connections(coords):
    # Store incoming and outgoing connections for each coordinate to understand
    # which kind of corner it can be. First element is incoming second is outgoing
    # 0 is a connection going north, 1 going east, 2 south and 3 west
    connections = [[0 if coords[i-1][1] > coords[i][1]
                    else 1 if coords[i-1][0] < coords[i][0]
                    else 2 if coords[i-1][1] < coords[i][1]
                    else 3,
                    0 if coords[i+1][1] < coords[i][1]
                    else 1 if coords[i+1][0] > coords[i][0]
                    else 2 if coords[i+1][1] > coords[i][1]
                    else 3]
                    for i in range(0, len(coords) - 1)]
    # Extra one for last connection
    connections.append([0 if coords[-2][1] > coords[-1][1]
                    else 1 if coords[-2][0] < coords[-1][0]
                    else 2 if coords[-2][1] < coords[-1][1]
                    else 3,
                    0 if coords[0][1] < coords[-1][1]
                    else 1 if coords[0][0] > coords[-1][0]
                    else 2 if coords[0][1] > coords[-1][1]
                    else 3])
    return connections

def find_rectangles_pt2(coords):
    # Get all connections and use them to find candidate coordinates based
    # on incoming/outgoing lines for each corner. Some corners can only possibly
    # be one type, others can be up to three
    connections = get_connections(coords)
    # One iteration to find all candidates
    tl_candidates = []
    tr_candidates = []
    bl_candidates = []
    br_candidates = []
    # Check direction of path by looking at (one of the) rightmost element(s)
    # If it has an incoming/outgoing south path, we're going clockwise
    max_x_loc = [coord[0] for coord in coords].index(max([coord[0] for coord in coords]))
    clockwise = True if 2 in connections[max_x_loc] else False
    # Define which corners can be which candidates based on angle/direction
    if clockwise:
        tl_connections = [[0,0], [0,1], [0,2], [0,3], [1,0], [1,1], [2,1], [3,1]]
        tr_connections = [[0,2], [1,0], [1,1], [1,2], [1,3], [2,1], [2,2], [3,2]]
        bl_connections = [[0,0], [0,3], [1,0], [2,0], [3,0], [3,1], [3,2], [3,3]]
        br_connections = [[0,3], [1,3], [2,0], [2,1], [2,2], [2,3], [3,2], [3,3]]
    else:
        tl_connections = [[0,2], [1,2], [2,2], [2,3], [3,0], [3,1], [3,2], [3,3]]
        tr_connections = [[0,0], [0,1], [0,2], [0,3], [1,3], [2,3], [3,0], [3,3]]
        bl_connections = [[0,1], [1,1], [1,2], [2,0], [2,1], [2,2], [2,3], [3,1]]
        br_connections = [[0,0], [0,1], [1,0], [1,1], [1,2], [1,3], [2,0], [3,0]]
    for coord, connection in zip(coords, connections):
        if connection in tl_connections:
            tl_candidates.append(coord)
        if connection in tr_connections:
            tr_candidates.append(coord)
        if connection in bl_connections:
            bl_candidates.append(coord)
        if connection in br_connections:
            br_candidates.append(coord)
    # Compare opposite pairs, with additional check that there are no intervening
    # paths
    all_paths = [[coords[i], coords[(i+1) % len(coords)]] for i in range(0, len(coords))]
    max_rect = 0
    for tl in tl_candidates:
        for br in br_candidates:
            # Check path doesn't intersect but also whether the positioning is right to make a rect
            if (tl[0] <= br[0]) & (tl[1] <= br[1]):
                if check_path(all_paths, x_min = tl[0], y_min = tl[1], x_max = br[0], y_max = br[1]):
                    current_area = get_area(tl, br)
                    if current_area > max_rect:
                        max_rect = current_area
                        max_coords = [tl, br]
    for tr in tr_candidates:
        for bl in bl_candidates:
            if (tr[0] >= bl[0]) & (tr[1] <= bl[1]):
                if check_path(all_paths, x_min = bl[0], y_min = tr[1], x_max = tr[0], y_max = bl[1]):
                    current_area = get_area(tr, bl)
                    if current_area > max_rect:
                        max_rect = current_area
                        max_coords = [tr, bl]
    return max_rect


test = parse_input('day_9_test.txt')
find_rectangles_pt1(test) == 50

input = parse_input('day_9_input.txt')
pt1_answer = find_rectangles_pt1(input)

# Part 2
find_rectangles_pt2(test) == 24
pt2_answer = find_rectangles_pt2(input)

my_test = parse_input('day_9_my_test.txt')
find_rectangles_pt1(my_test)
find_rectangles_pt2(my_test)
