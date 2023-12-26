import copy

class Node:
    def __init__(self, location):
        self.location = location
        self.edges = {}
        self.sources = []

    def __str__(self):
        return f'Node with location={self.location}, edges={[str(key.location)+": "+str(self.edges[key]) for key in self.edges.keys()]}'

def get_nodes(data, start_node, part=1):
    height, width = (len(data), len(data[0]))
    nodes = [start_node]
    frontier = [start_node]
    while frontier:
        node = frontier.pop()
        outgoing = []
        y, x = node.location
        if 0 <= y-1 < height and data[y-1][x] == '^': outgoing.append((y-1, x))
        if 0 <= y+1 < height and data[y+1][x] == 'v': outgoing.append((y+1, x))
        if 0 <= x-1 < width and data[y][x-1] == '<': outgoing.append((y, x-1))
        if 0 <= x+1 < width and data[y][x+1] == '>': outgoing.append((y, x+1))
        for path in outgoing:
            steps = 2
            oy, ox = path
            slope = data[oy][ox]
            data[oy][ox] = '#'
            if slope == '^': oy -= 1
            if slope == 'v': oy += 1
            if slope == '<': ox -= 1
            if slope == '>': ox += 1
            while data[oy][ox] == '.':
                data[oy][ox] = '#'
                if data[oy-1][ox] != '#': oy -= 1
                elif data[oy+1][ox] != '#': oy += 1
                elif data[oy][ox-1] != '#': ox -= 1
                elif data[oy][ox+1] != '#': ox += 1
                steps += 1
            slope = data[oy][ox]
            data[oy][ox] = '#'
            if slope == '^': oy -= 1
            if slope == 'v': oy += 1
            if slope == '<': ox -= 1
            if slope == '>': ox += 1
            steps += 1
            new_node = None
            for existing in nodes:
                if existing.location == (oy, ox):
                    new_node = existing
            if not new_node:
                new_node = Node((oy, ox))
                nodes.append(new_node)
                frontier.append(new_node)
            node.edges[new_node] = steps
            if part == 1: new_node.sources.append(node)
            if part == 2: new_node.edges[node] = steps
    if part == 2: return nodes
    sorted_nodes = []
    frontier = [start_node]
    while frontier:
        node = frontier.pop()
        sorted_nodes.append(node)
        for dest in node.edges.keys():
            is_start = True
            for source in dest.sources:
                if source not in sorted_nodes:
                    is_start = False
            if is_start: frontier.append(dest)
    return sorted_nodes

def part1(filename):
    with open(filename) as f: data = [list(line.strip()) for line in f.readlines()]
    height, width = (len(data), len(data[0]))
    data[1][1] = 'v' # for consistency
    data[height-2][width-2] = 'v' # same
    start_node = Node((0, 1))
    # find all nodes/edges
    sorted_nodes = get_nodes(data, start_node)
    # topological sort
    # DAG algorithm
    longest_paths = {node: 0 for node in sorted_nodes}
    for node in sorted_nodes:
        for dest in node.edges.keys():
            if longest_paths[dest] < longest_paths[node] + node.edges[dest]:
                longest_paths[dest] = longest_paths[node] + node.edges[dest]
    return longest_paths[sorted_nodes[-1]]

def max_path_search(start_node, end_loc, used_nodes):
    if start_node.location == end_loc:
        return 0
    used_nodes.append(start_node)
    max_dist = -float('inf')
    for dest in start_node.edges.keys():
        if dest not in used_nodes:
            max_dist = max(max_dist, start_node.edges[dest] + max_path_search(dest, end_loc, used_nodes.copy()))
    return max_dist

def part2(filename):
    with open(filename) as f: data = [list(line.strip()) for line in f.readlines()]
    height, width = (len(data), len(data[0]))
    data[1][1] = 'v' # for consistency
    data[height-2][width-2] = 'v' # same
    start_node = Node((0, 1))
    # find all nodes/edges
    nodes = get_nodes(data, start_node, part=2)
    for node in nodes: print(node)
    # modified DFS to find longest path
    return max_path_search(start_node, (height-1, width-2), [])

print(part1('input'))
print(part2('input'))
