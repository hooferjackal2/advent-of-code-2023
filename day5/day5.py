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


def seed_range_closest(srange, map_arrs):
    curr_ranges = [srange]
    for m in map_arrs:
        next_map_ranges = []  # "output" data - input for the next map
        unmatched_ranges = curr_ranges
        for row in m:
            next_unmatched_ranges = []
            for urange in unmatched_ranges:
                if urange[0] >= row[1] + row[2] or urange[1] <= row[1]:  # range doesn't match
                    next_unmatched_ranges.append(urange)
                    continue
                if urange[0] < row[1]:  # range overhangs left side
                    next_unmatched_ranges.append([urange[0], row[1]])
                    urange[0] = row[1]
                if urange[1] > row[1] + row[2]:  # range overhangs right side
                    next_unmatched_ranges.append([row[1] + row[2], urange[1]])
                    urange[1] = row[1] + row[2]
                next_map_ranges.append([urange[0] + row[0] - row[1], urange[1] + row[0] - row[1]])
            unmatched_ranges = next_unmatched_ranges
        next_map_ranges += unmatched_ranges  # append everything that didn't get matched in the map
        curr_ranges = next_map_ranges
    return min([r[0] for r in curr_ranges])

def part2(filename):
    with open(filename) as f: lines = ''.join(f.readlines()).split(':')[1:]
    pair_strs = re.findall('\d+ \d+', lines[0])
    seed_ranges = list(map(lambda x: [int(x[0]), int(x[0])+int(x[1])], [re.findall('\d+', p) for p in pair_strs]))
    data = map(lambda i: re.compile('[\d\s]+').search(i).group(), lines[1:])
    map_arrs = [list(map(lambda x: [int(i) for i in re.findall('\d+', x)], re.findall('\d+ \d+ \d+\n', s))) for s in data]
    results = [seed_range_closest(srange, map_arrs) for srange in seed_ranges]
    return min(results)


print(part1('input'))
print(part2('input'))
