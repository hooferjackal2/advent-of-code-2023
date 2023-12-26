import re
import math
import copy

qualities = ['x','m','a','s']

def process_part(part, workflows, workflow_name):
    if workflow_name == 'R': return 0
    if workflow_name == 'A': return sum(part)
    rules = workflows[workflow_name]
    for rule in rules:
        if ':' not in rule: return process_part(part, workflows, rule)
        cond, result = rule.split(':')
        qual = qualities.index(cond[0])
        val = int(re.search('\d+',cond).group())
        if '<' in cond and part[qual] < val:
            return process_part(part, workflows, result)
        if '>' in cond and part[qual] > val:
            return process_part(part, workflows, result)
    return 0

def process_range(part_range, workflows, workflow_name):
    if workflow_name == 'R': return 0
    if workflow_name == 'A': return math.prod(end - start for start, end in part_range)
    rules = workflows[workflow_name]
    num_valid = 0
    for rule in rules:
        if ':' not in rule: return num_valid + process_range(part_range, workflows, rule)
        cond, result = rule.split(':')
        qual = qualities.index(cond[0])
        start, end = part_range[qual]
        val = int(re.search('\d+',cond).group())
        if '<' in cond:
            if val <= start: continue
            if end <= val: return num_valid + process_range(part_range, workflows, result)
            if start < val < end:
                new_range = copy.deepcopy(part_range)
                new_range[qual] = (start, val)
                num_valid += process_range(new_range, workflows, result)
                part_range[qual] = (val, end)
        if '>' in cond:
            if val >= end - 1: continue
            if start - 1 >= val: return num_valid + process_range(part_range, workflows, result)
            if start - 1 < val < end - 1:
                new_range = copy.deepcopy(part_range)
                new_range[qual] = (val + 1, end)
                num_valid += process_range(new_range, workflows, result)
                part_range[qual] = (start, val + 1)
    return num_valid

def get_workflows(lines):
    workflow_strs = [line.strip() for line in lines if len(line) > 0 and line[0].isalpha()]
    workflows = {}
    for workflow in workflow_strs:
        name = re.match('\w+', workflow).group()
        workflow = workflow[:-1].split('{')[1].split(',')
        workflows[name] = workflow
    return workflows

def part1(filename):
    with open(filename) as f: lines = f.readlines()
    workflows = get_workflows(lines)
    part_strs = [line.strip() for line in lines if len(line) > 0 and line[0] == '{']
    parts = [[int(val) for val in re.findall('\d+', part)] for part in part_strs]
    print(parts)
    return sum(process_part(part, workflows, 'in') for part in parts)

def part2(filename):
    with open(filename) as f: lines = f.readlines()
    workflows = get_workflows(lines)
    part_range = [(1, 4001) for _ in range(4)]
    return process_range(part_range, workflows, 'in')

print(part1('input'))
print(part2('input'))
