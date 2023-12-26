def take_step(reachable, tiles, sides=(True, True, True, True)):
    bottom, left, top, right = sides
    next_reachable = []
    side_len = len(tiles)
    for y, x in reachable:
        for dy, dx in [(1,0),(-1,0),(0,1),(0,-1)]:
            if ((0 <= y+dy or not top) and (y+dy < side_len or not bottom) and
                (0 <= x+dx or not left) and (x+dx < side_len or not right) and
                tiles[(y+dy) % side_len][(x+dx) % side_len] != '#'): next_reachable.append((y+dy, x+dx))
    return list(set(next_reachable))

def part1(filename):
    with open(filename) as f: tiles = [list(line.strip()) for line in f.readlines()]
    reachable = []
    for i, row in enumerate(tiles):
        if 'S' in row:
            reachable.append((i, row.index('S')))
    num_steps = 64
    for _ in range(num_steps):
        reachable = take_step(reachable, tiles)
    return len(reachable)

def part2(filename):
    with open(filename) as f: tiles = [list(line.strip()) for line in f.readlines()]
    start_y, start_x = 0, 0
    for i, row in enumerate(tiles):
        if 'S' in row:
            start_y = i
            start_x = row.index('S')
    l_s = len(tiles)
    total_plots = 0
    # calculate X1 and X2
    Xmax = [-1, -1]
    nextXmax = [0, 0]
    reachable = [(start_y, start_x)]
    steps = 0
    while Xmax != nextXmax:
        reachable = take_step(reachable, tiles)
        steps += 1
        Xmax[steps % 2] = nextXmax[steps % 2]
        nextXmax[steps % 2] = len(reachable)
    start_steps = 26501365
    # for n, e, s, w:
    xstart_side = max(0, start_steps - (l_s // 2 + 1))
    edge_starts = [(0, start_x), (start_y, l_s-1), (l_s-1, start_x), (start_y, 0)]
    edge_sides = [(False, True, True, True), (True, False, True, True),
             (True, True, False, True), (True, True, True, False)]
    n_edge = [0, 0, 0, 0]
    X_edge = [0, 0, 0, 0]
    for i, start in enumerate(edge_starts):
        # calculate n
        steps = 0
        past_len = 0
        reachable = [start]
        while len(reachable) != Xmax[(steps+1) % 2] or past_len != Xmax[steps % 2]:
            past_len = len(reachable)
            reachable = take_step(reachable, tiles)
            steps += 1
        n_edge[i] = steps
        # directly determine Xedge
        edge_steps = xstart_side - ((xstart_side - n_edge[i]) // l_s * l_s)
        reachable = [start]
        for _ in range(edge_steps):
            reachable = take_step(reachable, tiles, edge_sides[i])
        X_edge[i] = len(reachable)
        # accumulate plots
        k = max(0, (xstart_side - n_edge[i]) // l_s)
        total_plots += (k // 2 * sum(Xmax)
            + (Xmax[1] if k % 2 == 1 else 0)
            + X_edge[i])

    # for nw, ne, se, sw:
    xstart_corner = max(0, start_steps - (l_s + 1))
    corner_starts = [(0, 0), (0, l_s - 1), (l_s - 1, l_s - 1), (l_s - 1, 0)]
    corner_sides = [(False, True, True, False), (False, False, True, True),
                  (True, False, False, True), (True, True, False, False)]
    n_corner = [0, 0, 0, 0]
    X_slice = [0, 0, 0, 0]
    X_wedge = [0, 0, 0, 0]
    for i, start in enumerate(corner_starts):
        # calculate n
        steps = 0
        past_len = 0
        reachable = [start]
        while len(reachable) != Xmax[steps % 2] or past_len != Xmax[(steps-1) % 2]:
            past_len = len(reachable)
            reachable = take_step(reachable, tiles)
            steps += 1
        n_corner[i] = steps
        # directly determine Xslice
        corner_steps = xstart_corner - ((xstart_corner - n_corner[i]) // l_s * l_s)
        reachable = [start]
        for _ in range(corner_steps):
            reachable = take_step(reachable, tiles, edge_sides[i])
        X_slice[i] = len(reachable)
        # directly determine Xwedge
        reachable = [start]
        for _ in range(corner_steps):
            reachable = take_step(reachable, tiles, corner_sides[i])
        X_wedge[i] = len(reachable)
        # accumulate plots
        k = max(0, (xstart_corner - n_corner[i]) // l_s)
        num_X1 = (k // 2) ** 2 + (k if k % 2 == 1 else 0)
        num_X2 = (k // 2) ** 2 + k // 2
        total_plots += num_X1 * Xmax[1] + num_X2 * Xmax[0] + k * X_slice[i] + X_wedge[i]
    total_plots += Xmax[1]
    return total_plots

#print(part1('input'))
print(part2('input'))
