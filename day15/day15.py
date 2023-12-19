import re


def score(step):
    value = 0
    for ch in step:
        value += ord(ch)
        value = (value * 17) % 256
    return value


def part1(filename):
    with open(filename, 'r') as f: data = f.read().strip()
    steps = data.split(',')
    return sum([score(step) for step in steps])

def part2(filename):
    with open(filename, 'r') as f: data = f.read().strip()
    boxes = [[] for _ in range(256)]
    steps = data.split(',')
    for step in steps:
        label = re.search('[a-z]+', step).group()
        boxno = score(label)
        if '-' in step:
            for lens in boxes[boxno]:
                if label in lens: boxes[boxno].remove(lens)
        if '=' in step:
            focal = int(re.search('\d+', step).group())
            replace = True
            for i, lens in enumerate(boxes[boxno]):
                if label in lens:
                    boxes[boxno][i] = (label, focal)
                    replace = False
            if replace: boxes[boxno].append((label, focal))
    total_power = 0
    for idx, box in enumerate(boxes):
        for i, (_, focal) in enumerate(box):
            total_power += (idx+1)*(i+1)*focal
    return total_power

print(part1('input'))
print(part2('input'))
