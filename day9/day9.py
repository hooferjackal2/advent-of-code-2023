import re, numpy as np

def extrapolate(data, l, part):
    seqs = [data] + [[]] * (l - 1)
    for i in range(1, l): seqs[i] = seqs[i-1][1:l-i+1] - seqs[i-1][0:l-i]
    if part == 1: return sum([s[-1] for s in seqs])
    if part == 2: return sum(s[0] for s in seqs[0::2]) - sum(s[0] for s in seqs[1::2])

def solve(filename, part):
    with open(filename) as f: raw_data = f.readlines()
    all_data = [np.array(re.findall('\S+', row), dtype='i') for row in raw_data]
    return np.sum(np.array([extrapolate(data, len(data), part) for data in all_data]))

print(solve('input', 1))
print(solve('input', 2))
