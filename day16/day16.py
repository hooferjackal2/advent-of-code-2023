import copy


def move(y, x, angle):
    if angle == 0: return y-1, x, angle
    if angle == 1: return y, x+1, angle
    if angle == 2: return y+1, x, angle
    if angle == 3: return y, x-1, angle


def traverse(mirrors, explored, ever_explored, entry, is_only):
    y, x, angle = entry
    while 0 <= y < len(mirrors) and 0 <= x < len(mirrors[0]) and angle not in explored[y][x]:
        if is_only and ever_explored and angle in ever_explored[y][x]:
            return 0
        explored[y][x].append(angle)
        if ever_explored and angle not in ever_explored[y][x]: ever_explored[y][x].append(angle)
        if mirrors[y][x] == '\\':
            angle = 3 - angle
        elif mirrors[y][x] == '/':
            angle = 2 * (angle//2) - angle%2 + 1
        elif mirrors[y][x] == '|' and angle % 2 == 1:
            angle = 0
            traverse(mirrors, explored, ever_explored, (y+1, x, 2), False)
            is_only = False
        elif mirrors[y][x] == '-' and angle % 2 == 0:
            angle = 1
            traverse(mirrors, explored, ever_explored, (y, x-1, 3), False)
            is_only = False
        y, x, angle = move(y, x, angle)
    return sum([sum(len(point) > 0 for point in row) for row in explored])

def part1(filename):
    with open(filename) as f: data = [list(l.strip()) for l in f.readlines()]
    explored = [[[] for _ in data[0]] for _ in data]
    start = (0, 0, 1)
    num_explored = traverse(data, explored, None, start, True)
    visual = '\n'.join(''.join(('#' if len(l) > 0 else '.') for l in row) for row in explored)
    #print(visual)
    return num_explored

def part2(filename):
    with open(filename) as f: data = [list(l.strip()) for l in f.readlines()]
    explored = [[[] for _ in data[0]] for _ in data]
    ever_explored = copy.deepcopy(explored)
    height = len(data)
    width = len(data[0])
    max_explored = 0
    for i in range(height):
        left_start = (i, 0, 1)
        right_start = (i, width-1, 3)
        num_explored = traverse(copy.deepcopy(data), copy.deepcopy(explored), ever_explored, left_start, True)
        max_explored = max(max_explored, num_explored)
        num_explored = traverse(copy.deepcopy(data), copy.deepcopy(explored), ever_explored, right_start, True)
        max_explored = max(max_explored, num_explored)
    for i in range(width):
        top_start = (0, i, 2)
        bottom_start = (height-1, i, 0)
        num_explored = traverse(copy.deepcopy(data), copy.deepcopy(explored), ever_explored, top_start, True)
        max_explored = max(max_explored, num_explored)
        num_explored = traverse(copy.deepcopy(data), copy.deepcopy(explored), ever_explored, bottom_start, True)
        max_explored = max(max_explored, num_explored)
    return max_explored

print(part1('input'))
print(part2('input'))
