import re

def day11(filename):
    with open(filename) as f: lines = [line.strip() for line in f.readlines()]
    height = len(lines); width = len(lines[0])
    galaxies = [[y, x.start()] for y in range(height) for x in re.finditer('#', lines[y])]
    row_sum = [len([i for i in galaxies if i[0] == row]) for row in range(height)]
    col_sum = [len([i for i in galaxies if i[1] == col]) for col in range(width)]
    dist_sum = 0
    expand = 0
    for i in range(len(galaxies)):
        for j in range(i, len(galaxies)):
            gal1 = galaxies[i]; gal2 = galaxies[j]
            dist_sum += abs(gal2[0] - gal1[0]) + abs(gal2[1] - gal1[1])
            expand += row_sum[gal1[0]:gal2[0]].count(0)
            if gal1[1] > gal2[1]: gal1, gal2 = gal2, gal1
            expand += col_sum[gal1[1]:gal2[1]].count(0)
    return dist_sum, expand

dist_sum1, expand1 = day11('input')
print(dist_sum1 + expand1)
print(dist_sum1 + 999999 * expand1)
