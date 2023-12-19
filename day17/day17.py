import numpy as np

def generate_graphs(heatmap, min, max):
    # nodes are tuples: (y, x, next) where next is 0/1 for horiz/vert
    height = len(heatmap)
    width = len(heatmap[0])
    graph = {}
    best_temp = {}
    for y in range(height):
        for x in range(width):
            # store best temp
            best_temp[y, x, 0] = float('inf')
            best_temp[y, x, 1] = float('inf')
            # store all valid pairs
            graph[y, x, 0] = []
            graph[y, x, 1] = []
            for k in range(min, max+1):
                if x+k < width: graph[y, x, 0].append(((y, x+k, 1), sum(heatmap[y,x+1:x+k+1])))
                if x-k >= 0: graph[y, x, 0].append(((y, x-k, 1), sum(heatmap[y,x-k:x])))
                if y+k < height: graph[y, x, 1].append(((y+k, x, 0), sum(heatmap[y+1:y+k+1,x])))
                if y-k >= 0: graph[y, x, 1].append(((y-k, x, 0), sum(heatmap[y-k:y,x])))
    # starting positions
    best_temp[0, 0, 0] = 0
    best_temp[0, 0, 1] = 0
    return graph, best_temp


def node_add(pq, item, best_temp):
    idx = 0
    while idx < len(pq) and best_temp[item] > best_temp[pq[idx]]:
        idx += 1
    pq.insert(idx, item)


def day17(filename, part):
    with open(filename) as f: heatmap = [[int(ch) for ch in row.strip()] for row in f]
    height = len(heatmap)
    width = len(heatmap[0])
    heatmap = np.array(heatmap)
    graph, best_temp = generate_graphs(heatmap, 1, 3) if part==1 else generate_graphs(heatmap, 4, 10)
    pq = []
    for y in range(height):
        for x in range(width):
            node_add(pq, (y, x, 0), best_temp)
            node_add(pq, (y, x, 1), best_temp)
    # run dijkstra's
    while pq:
        curr = pq.pop(0)
        for node, weight in graph[curr]:
            if best_temp[curr] + weight < best_temp[node]:
                best_temp[node] = best_temp[curr] + weight
                pq.remove(node)
                node_add(pq, node, best_temp)
    # compare best temps for (height, width, 0) and (height, width, 1)
    return min(best_temp[height-1, width-1, 0], best_temp[height-1, width-1, 1])


print(day17('input', 1))
print(day17('input', 2))
