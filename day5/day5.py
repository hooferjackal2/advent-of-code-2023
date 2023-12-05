import re


def part1(filename):
    with open(filename) as f: lines = ''.join(f.readlines()).split(':')[1:]
    seeds = map(int, re.findall('\d+', lines[0]))
    data = map(lambda i: re.compile('[\d\s]+').search(i).group(), lines[1:])
    map_arrs = []
    for map_str in data:
        map_arr = list(map(lambda x: [int(i) for i in re.findall('\d+', x)], re.findall('\d+ \d+ \d+\n', map_str)))
        map_arrs.append(map_arr)
    results = []
    for s in seeds:
        for m in map_arrs:
            s = next((s for s in [s+r[0]-r[1] if r[1]<=s<r[1]+r[2] else None for r in m] if s), s)
        results.append(s)
    return min(results)


def part2(filename):
    with open(filename) as f: lines = ''.join(f.readlines()).split(':')[1:]
    pair_strs = re.findall('\d+ \d+', lines[0])
    seed_ranges = list(map(lambda x: [int(x[0]), int(x[0])+int(x[1])], [re.findall('\d+', pair) for pair in pair_strs]))
    data = map(lambda i: re.compile('[\d\s]+').search(i).group(), lines[1:])
    map_arrs = []
    for map_str in data:
        map_arr = list(map(lambda x: [int(i) for i in re.findall('\d+', x)], re.findall('\d+ \d+ \d+\n', map_str)))
        map_arrs.append(map_arr)
    results = []
    for srange in seed_ranges:
        curr_ranges = [srange]
        for m in map_arrs:
            next_ranges = [] # "output" data - input for the next map
            for crange in curr_ranges:
                range_slices = [crange] # one function can "slice" a range an arbitrary number of times
                for row in m:
                    new_slices = []
                    for rslice in range_slices:
                        if rslice[0] >= row[1]+row[2] or rslice[1] <= row[1]: # range doesn't match
                            new_slices.append(rslice)
                            continue
                        if rslice[0] < row[1]: # range overhangs left side
                            new_slices.append([rslice[0], row[1]])
                            rslice[0] = row[1]
                        if rslice[1] > row[1]+row[2]: # range overhangs right side
                            new_slices.append([row[1]+row[2], rslice[1]])
                            rslice[1] = row[1]+row[2]
                        next_ranges.append([rslice[0]+row[0]-row[1], rslice[1]+row[0]-row[1]])
                    range_slices = new_slices
                next_ranges += range_slices # append everything that didn't get matched in the map
            curr_ranges = next_ranges
        results.append(min([r[0] for r in curr_ranges]))
    print(results)
    return min(results)


print(part1('input'))
print(part2('input'))
