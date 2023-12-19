def fill(site):
    for si, row in enumerate(site):
        inshape = False
        prevch = '.'
        inrow = False
        frombottom = False
        for i, ch in enumerate(row):
            if prevch == '.' and row[i] == '#':
                inshape = not inshape
            if prevch == '#' and row[i] == '#':
                inrow = True
                if si < len(site)-1 and site[si+1][i-1] == '#': frombottom = True
            if row[i] == '.' and inrow:
                inrow = False
                tobottom = si < len(site)-1 and site[si+1][i-1] == '#'
                if frombottom == tobottom:
                    inshape = not inshape
                frombottom = False
            prevch = row[i]
            if inshape and not inrow: row[i] = '#'

def part1(filename):
    with open(filename) as f: lines = [line.strip().split(' ') for line in f.readlines()]
    instructions = [(line[0], int(line[1]), line[2][2:-1]) for line in lines]
    top = 0
    bot = 0
    lft = 0
    rgt = 0
    y = 0
    x = 0
    for inst in instructions:
        angle, dist, color = inst
        if angle == 'U':
            y -= dist
            top = min(top, y)
        if angle == 'D':
            y += dist
            bot = max(bot, y)
        if angle == 'L':
            x -= dist
            lft = min(lft, x)
        if angle == 'R':
            x += dist
            rgt = max(rgt, x)
    site = [['.' for _ in range(rgt-lft+1)] for _ in range(bot-top+1)]
    y = -top
    x = -lft
    for inst in instructions:
        angle, dist, color = inst
        if angle == 'U':
            for i in range(dist):
                site[y-i][x] = '#'
            y -= dist
        if angle == 'D':
            for i in range(dist):
                site[y+i][x] = '#'
            y += dist
        if angle == 'L':
            for i in range(dist):
                site[y][x-i] = '#'
            x -= dist
        if angle == 'R':
            for i in range(dist):
                site[y][x+i] = '#'
            x += dist
    fill(site)
    #for row in site:
    #    print(''.join(row))
    return sum(row.count('#') for row in site)

def part2(filename):
    with open(filename) as f: lines = [line.strip().split(' ') for line in f.readlines()]
    instructions = [(line[2][2:-2], line[2][-2]) for line in lines]
    # get path in coords
    coords = []
    y = 0
    x = 0
    for inst in instructions:
        coords.append((y, x))
        dist, angle = inst
        dist = int(dist, 16)
        if angle == '3': y -= dist # up
        if angle == '1': y += dist # down
        if angle == '2': x -= dist # left
        if angle == '0': x += dist # right
    ycoords = sorted(set(y for y, _ in coords))
    xcoords = sorted(set(x for _, x in coords))
    graphpos = [(ycoords.index(y) * 2, xcoords.index(x) * 2) for y, x in coords]
    # initialize graph
    site = [['.' for _ in range(2*len(xcoords)+1)] for _ in range(2*len(ycoords)+1)]
    # draw path
    for i, point in enumerate(graphpos):
        y2, x2 = point
        y1, x1 = graphpos[i-1]
        if y2 > y1:
            for y in range(y1,y2+1): site[y][x1] = '#'
        if y2 < y1:
            for y in range(y2,y1+1): site[y][x1] = '#'
        if x2 > x1:
            for x in range(x1,x2+1): site[y1][x] = '#'
        if x2 < x1:
            for x in range(x2,x1+1): site[y1][x] = '#'
    # fill in path
    fill(site)
    # calculate area per square
    for row in site:
        print(''.join(row))
    volume = 0
    for y, row in enumerate(site):
        for x, block in enumerate(row):
            if block == '.': continue
            yval = 1 if y % 2 == 0 else ycoords[y // 2 + 1] - ycoords[y // 2] - 1
            xval = 1 if x % 2 == 0 else xcoords[x // 2 + 1] - xcoords[x // 2] - 1
            volume += yval*xval
    return volume

print(part1('input'))
print(part2('input'))
