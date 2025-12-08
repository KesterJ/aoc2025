from math import prod

def parse_input(file_name):
    with open(file_name, 'r') as input_file:
        nodes = [[int(num) for num in line.strip('\n').split(',')] for line in input_file]
    return nodes

def initialise_node_dict(nodes):
    # Create a dictionary with an ID for each node, followed
    # by its coordinates and then a space for the network ID
    # it belongs to; starts at -1 for no network
    return {id: [node, -1] for id, node in enumerate(nodes)}

def get_straight_line_distance(node1, node2):
    x = abs(node1[0] - node2[0])
    y = abs(node1[1] - node2[1])
    z = abs(node1[2] - node2[2])
    return (x ** 2 + y ** 2 + z ** 2) ** 0.5

def find_sorted_distances(node_dict):
    # Find distances between each pair of nodes in a 
    # dictionary and sort them smallest to largest
    distances = []
    for i in range(0, len(node_dict) - 1):
        for j in range(i + 1, len(node_dict)):
            distances.append([[i, j],
                              get_straight_line_distance(node_dict[i][0], node_dict[j][0])])
    return sorted(distances, key = lambda distances: distances[1])

def connect_pair(pair, node_dict):
    # Update dictionary with connection between the pair of nodes;
    # exactly how depends on if they are part of existing network
    if (node_dict[pair[0]][1] == -1) & (node_dict[pair[1]][1] == -1):
        new_id = max([network[1] for network in node_dict.values()]) + 1
        node_dict[pair[0]][1] = new_id
        node_dict[pair[1]][1] = new_id
    elif node_dict[pair[0]][1] == -1:
        node_dict[pair[0]][1] = node_dict[pair[1]][1]
    elif node_dict[pair[1]][1] == -1:
        node_dict[pair[1]][1] = node_dict[pair[0]][1]
    # If neither are empty, we only need to act if they are different
    elif node_dict[pair[0]][1] != node_dict[pair[1]][1]:
        network_to_keep = max(node_dict[pair[0]][1], node_dict[pair[1]][1])
        network_to_drop = min(node_dict[pair[0]][1], node_dict[pair[1]][1])
        # Update dictionary so one network is replaced
        node_dict |= {key: [value[0], network_to_keep] for key, value in node_dict.items() if value[1] == network_to_drop}

def get_sorted_network_sizes(node_dict):
    # Counts how many times each network appears in the dictionary
    all_networks = [value[1] for value in node_dict.values() if value[1] != -1]
    counts = dict()
    for network in all_networks:
        counts[network] = counts.get(network, 0) + 1
    return sorted(counts.values(), reverse = True)

def find_connections(nodes, num_connections, largest_n):
    node_dict = initialise_node_dict(nodes)
    node_distances = find_sorted_distances(node_dict)
    for connection_pair in node_distances[0:num_connections]:
        connect_pair(connection_pair[0], node_dict)
    sizes = get_sorted_network_sizes(node_dict)
    return prod(sizes[0:largest_n])

def connect_all(nodes):
    node_dict = initialise_node_dict(nodes)
    node_distances = find_sorted_distances(node_dict)
    num_nodes = len(node_dict)
    visited_nodes = []
    counter = 0
    while num_nodes - len(visited_nodes) > 0:
        visited_nodes = list(set(visited_nodes + node_distances[counter][0]))
        counter += 1
    final_nodes = node_distances[counter - 1][0]
    return prod([node_dict[node][0][0] for node in final_nodes])

# Test
test = parse_input('day_8_test.txt')
find_connections(test, 10, 3) == 40

# Actual
input = parse_input('day_8_input.txt')
pt1_answer = find_connections(input, 1000, 3)

# Part 2
connect_all(test) == 25272
pt2_answer = connect_all(input)
