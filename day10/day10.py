import copy
import sys
sys.setrecursionlimit(10000)

pipes = {'|': [[1, 0], [-1, 0]], '-': [[0, -1], [0, 1]],
         'L': [[-1, 0], [0, 1]], 'F': [[0, 1], [1, 0]],
         '7': [[1, 0], [0, -1]], 'J': [[0, -1], [-1, 0]],
         '.': [], 'S': [[1, 0], [-1, 0], [0, -1], [0, 1]]}

def findpath(lines):
    pos_y = [l.count('S') for l in lines].index(1)
    pos_x = lines[pos_y].index('S')
    from_dir = []
    path = [[pos_y, pos_x]]
    for source in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
        if source in pipes[lines[pos_y - source[0]][pos_x - source[1]]]:
            pos_y -= source[0]
            pos_x -= source[1]
            path.append([pos_y, pos_x])
            from_dir = source
            break
    while lines[pos_y][pos_x] != 'S':
        dirs = copy.deepcopy(pipes[lines[pos_y][pos_x]])
        dirs.remove(from_dir)
        pos_y += dirs[0][0]
        pos_x += dirs[0][1]
        path.append([pos_y, pos_x])
        from_dir = [-i for i in dirs[0]]
    return path


def part1(filename):
    with open(filename) as f: lines = [line.strip() for line in f.readlines()]
    return len(findpath(lines)) // 2


def crawl(corners, tiles, pos_y, pos_x):
    [h, w] = [len(tiles), len(tiles[0])]
    [up, right, down, left] = [True, True, True, True]
    corners[pos_y][pos_x] = 'O'
    if pos_y == 0:
        up = False
    elif corners[pos_y-1][pos_x] == 'O':
        up = False
    elif pos_x % w != 0 and [0, 1] in pipes[tiles[pos_y-1][pos_x-1]] and [0, -1] in pipes[tiles[pos_y-1][pos_x]]:
        up = False
    if pos_x == w:
        right = False
    elif corners[pos_y][pos_x+1] == 'O':
        right = False
    elif pos_y % h != 0 and [1, 0] in pipes[tiles[pos_y-1][pos_x]] and [-1, 0] in pipes[tiles[pos_y][pos_x]]:
        right = False
    if pos_y == h:
        down = False
    elif corners[pos_y+1][pos_x] == 'O':
        down = False
    elif pos_x % w != 0 and [0, 1] in pipes[tiles[pos_y][pos_x-1]] and [0, -1] in pipes[tiles[pos_y][pos_x]]:
        down = False
    if pos_x == 0:
        left = False
    elif corners[pos_y][pos_x-1] == 'O':
        left = False
    elif pos_y % h != 0 and [1, 0] in pipes[tiles[pos_y-1][pos_x-1]] and [-1, 0] in pipes[tiles[pos_y][pos_x-1]]:
        left = False
    if up: crawl(corners, tiles, pos_y-1, pos_x)
    if right: crawl(corners, tiles, pos_y, pos_x+1)
    if down: crawl(corners, tiles, pos_y+1, pos_x)
    if left: crawl(corners, tiles, pos_y, pos_x-1)


def part2(filename):
    with open(filename) as f: lines = [line.strip() for line in f.readlines()]
    path = findpath(lines)
    [h, w] = [len(lines), len(lines[0])]
    pathonly = [[lines[y][x] for x in range(w)] for y in range(h)]
    for y in range(h):
        for x in range(w):
            if [y, x] not in path:
                pathonly[y][x] = '.'
    tiles = [['U' for _ in range(w)] for _ in range(h)] # temporary
    corners = [['U' for _ in range(w+1)] for _ in range(h+1)]
    crawl(corners, pathonly,0, 0)
    interior_points = 0
    for y in range(h):
        for x in range(w):
            if [y, x] in path:
                tiles[y][x] = 'P'
            elif corners[y][x] != 'O' or corners[y+1][x] != 'O' or corners[y][x+1] != 'O' or corners[y+1][x+1] != 'O':
                tiles[y][x] = 'I'
                interior_points += 1
    for trow in tiles: print(''.join(trow))
    for crow in corners: print(''.join(crow))
    return interior_points

print(part1('input'))
print(part2('input'))
