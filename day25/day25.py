import re

class Node:
    def __init__(self, name):
        self.name = name
        self.edges = []

    def __str__(self):
        return f'Node {self.name}, connected to: {self.edges}'

    def connect(self, other):
        if other not in self.edges:
            self.edges.append(other)

    def degree(self):
        return len(self.edges)

def find_shortest_path(graph, start, dest, blacklist):
    frontier = [(start, [])]
    explored = {}
    shortest_path = None
    while frontier:
        next_ring = []
        for node, path in frontier:
            explored[node] = path
            for adj in graph[node].edges:
                if (adj not in explored.keys() and adj not in frontier
                  and (node, adj) not in blacklist and (adj, node) not in blacklist):
                    next_ring.append((adj, path + [(node, adj)]))
                if adj == dest and (node, dest) not in blacklist and (dest, node) not in blacklist:
                    shortest_path = path + [(node, dest)]
                    break
            if shortest_path: break
        if shortest_path: break
        frontier = next_ring
    return shortest_path

def part1(filename):
    with open(filename) as f: nodeinfo = [re.findall('\w+', line) for line in f.readlines()]
    graph = {}
    # make graph
    for node in nodeinfo:
        for other in node[1:]:
            if node[0] not in graph.keys():
                graph[node[0]] = Node(node[0])
            if other not in graph.keys():
                graph[other] = Node(other)
            graph[node[0]].connect(other)
            graph[other].connect(node[0])
    #for a in graph.keys():
    #    print(graph[a])
    #print(explored)
    start = 'lkr'
    groups = {start: 1}
    sure = {start: True}
    for dest in graph.keys():
        if dest == start: continue
        blacklist = []
        shortest_path = None
        for i in range(4):
            shortest_path = find_shortest_path(graph, start, dest, blacklist)
            if shortest_path: blacklist += shortest_path
            else:
                groups[dest] = 2
                sure[dest] = False
                break
        if shortest_path:
            groups[dest] = 1
            sure[dest] = True
    start2 = 'jcr'
    sure[start2] = True
    for dest in graph.keys():
        if dest == start2 or groups[dest] == 1: continue
        blacklist = []
        shortest_path = None
        for i in range(4):
            shortest_path = find_shortest_path(graph, start2, dest, blacklist)
            if shortest_path: blacklist += shortest_path
            else:
                break
        if shortest_path:
            groups[dest] = 2
            sure[dest] = True
    group1 = [key for key in groups.keys() if groups[key] == 1 and sure[key]]
    group2 = [key for key in groups.keys() if groups[key] == 2 and sure[key]]
    unsure = [key for key in groups.keys() if not sure[key]]
    print(unsure)
    count2 = len(group2)
    count1 = len(group1)
    print(f'Length of groups: {len(groups.values())}, # in group 1: {count1}, # in group 2: {count2}')
    return count1 * count2

print(part1('input'))
