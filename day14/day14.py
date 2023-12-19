import copy

def move(rock_mat):
    for i in range(len(rock_mat)):
        for j in range(len(rock_mat[0])):
            if rock_mat[i][j] == 'O':
                dest = i
                while dest > 0 and rock_mat[dest - 1][j] == '.':
                    dest -= 1
                rock_mat[i][j] = '.'
                rock_mat[dest][j] = 'O'
    return


def part1(filename):
    with open(filename) as f: data = [list(line.strip()) for line in f.readlines()]
    load = 0
    move(data)
    for i in range(len(data)):
        load += data[i].count('O') * (len(data) - i)
    return load


def rotate(data):
    newdata = [[None for _ in range(len(data))] for _ in range(len(data[0]))]
    for i in range(len(data)):
        for j in range(len(data[0])):
            newdata[j][len(data)-i-1] = data[i][j]
    return newdata


def part2(filename):
    with open(filename) as f: data = [list(line.strip()) for line in f.readlines()]
    move(data)
    last_copies = []
    turns = 0
    repeat = False
    cycle_size = 0
    while not repeat:
        if turns % 4 == 0: last_copies.append(copy.deepcopy(data))
        move(data)
        data = rotate(data)
        turns += 1
        if turns % 4 != 0: continue
        # check for cycle
        load = 0
        for j in range(len(data)):
            load += data[j].count('O') * (len(data) - j)
        for l_idx, prev in enumerate(last_copies):
            if data == prev:
                repeat = True
                cycle_size = len(last_copies) - l_idx
                break
    cycles = turns // 4
    last_copies.append(data)
    print('found cycle of size', cycle_size, 'after', cycles, 'cycles')
    equiv = last_copies[(1000000000 - cycles) % cycle_size + cycles - cycle_size]
    load = 0
    for j in range(len(equiv)):
        load += equiv[j].count('O') * (len(equiv) - j)
    return load


print(part1('input'))
print(part2('input'))
