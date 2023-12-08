import re
import math


def setup(filename):
    with open(filename) as f: lines = f.readlines()
    path = lines[0].strip()
    edge_dict = {e[0]: [e[1], e[2]] for e in [re.findall('\w+', l) for l in lines[2:]]}
    return path, edge_dict


def follow_map(path, edge_dict, position):
    moves = 0
    while position != 'ZZZ':
        position = edge_dict[position][0 if path[moves % len(path)] == 'L' else 1]
        moves += 1
    return moves


def find_cycle(path, edge_dict, position):
    moves = 0
    history = []
    while True:
        history.append([position, moves % len(path)])
        position = edge_dict[position][0 if path[moves % len(path)] == 'L' else 1]
        moves += 1
        if [position, moves % len(path)] in history:
            last_pos = history.index([position, moves % len(path)])
            z_moves = [[move[0], i] for i, move in enumerate(history) if move[0][-1] == 'Z']
            print(f"cycle found! position='{position}', moves='{moves % len(path)}', abs moves='{moves}', last_pos='{last_pos}'")
            print(z_moves)
            return z_moves[0][1]


def part1(filename):
    path, edge_dict = setup(filename)
    start = 'AAA'
    return follow_map(path, edge_dict, start)


def part2(filename):
    path, edge_dict = setup(filename)
    start = [pos for pos in edge_dict.keys() if pos[-1] == 'A']
    cycle_lens = [find_cycle(path, edge_dict, pos) for pos in start]
    return math.lcm(*cycle_lens)


print(part1('input'))
print(part2('input'))
