import copy
import re


def part1(filename):
    partsum = 0
    file = open(filename, "r")
    lines = file.readlines()
    char_array = []
    for line in lines:
        line = list(line.strip())
        char_array.append(line)
    valid_map = copy.deepcopy(char_array)
    for i in range(len(valid_map)):
        for j in range(len(valid_map[0])):
            valid_map[i][j] = False
            for i2 in range(-1,2):
                for j2 in range(-1,2):
                    try:
                        if char_array[i+i2][j+j2] not in '0123456789.':
                            valid_map[i][j] = True
                    except IndexError:
                        pass
    for i in range(len(lines)):
        partmatches = re.finditer('\d+',lines[i])
        for match in partmatches:
            valid = False
            for j in range(match.start(), match.end()):
                if valid_map[i][j]:
                    valid = True
            if valid:
                partsum += int(match.group())
    return partsum


def part2(filename):
    ratiosum = 0
    file = open(filename, "r")
    lines = file.readlines()
    char_array = []
    for line in lines:
        line = list(line.strip())
        char_array.append(line)
    gear_map = copy.deepcopy(char_array)
    for i in range(len(gear_map)):
        for j in range(len(gear_map[0])):
            gear_map[i][j] = []
    for i in range(len(lines)):
        partmatches = re.finditer('\d+',lines[i])
        for match in partmatches:
            for j in range(match.start()-1, match.end()+1):
                for i2 in range(-1, 2):
                    try:
                        gear_map[i+i2][j].append(int(match.group()))
                    except IndexError:
                        pass
    for i in range(len(gear_map)):
        for j in range(len(gear_map[0])):
            if char_array[i][j] == '*' and len(gear_map[i][j]) == 2:
                ratiosum += gear_map[i][j][0] * gear_map[i][j][1]
    return ratiosum

print(part1("input"))
print(part2("input"))
