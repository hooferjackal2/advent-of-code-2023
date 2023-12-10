import re, numpy as np

# lol
# solve = lambda i: [f := open(i[0]), a := [np.array(re.findall('\d+', l.replace(i[1],''))).astype(float) for l in f.readlines()], x := a[0], r := a[1], int(np.prod(x - 2*(np.floor((x-np.sqrt(x**2-4*r))/2)) - 1))][-1]
def solve(filename, trim):
    with open(filename) as f: lines = f.readlines()
    [x, r] = [np.array(re.findall('\d+', l.replace(trim,'')), float) for l in lines]
    return int(np.prod(x - 2*(np.floor((x-np.sqrt(x**2-4*r))/2)) - 1))

print('Part 1:', solve('input', ''), 'Part 2:', solve('input', ' '))
