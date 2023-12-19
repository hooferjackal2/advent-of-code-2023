import re
import math
k = 1

def num_sols(row, nums):
    if len(row) < sum(nums)+len(nums)-1: return 0
    elif row[0] == '.': return num_sols(row[1:], nums)
    elif row[0] == '#':
        if len(nums) == 1:
            if '.' in row[:nums[0]]: return 0
            elif len(row) == nums[0]: return 1
            else: return 0 if '#' in row[nums[0]:] else 1
        elif '.' not in row[:nums[0]] and row[nums[0]] != '#':
            return num_sols(row[nums[0]+1:], nums[1:] if len(nums) > 1 else [])
        else: return 0 # contradiction found
    elif row[0] == '?':
        return num_sols(['.']+row[1:], nums) + num_sols(['#']+row[1:], nums)

def list_sols(row, nums):
    if len(row) < sum(nums)+len(nums)-1: return []
    elif row[0] == '.': return ['.'+sol for sol in list_sols(row[1:], nums)]
    elif row[0] == '#':
        if len(nums) == 1:
            if '.' in row[:nums[0]]: return []
            elif len(row) == nums[0]: return ['#'*len(row)]
            else: return [] if '#' in row[nums[0]:] else ['#'*nums[0] + '.'*len(row[nums[0]:])]
        elif '.' not in row[:nums[0]] and row[nums[0]] != '#':
            return ['#'*nums[0]+'.'+sol for sol in list_sols(row[nums[0]+1:], nums[1:])] if len(nums) > 1 else []
        else: return [] # contradiction found
    elif row[0] == '?':
        return list_sols(['.']+row[1:], nums) + list_sols(['#']+row[1:], nums)

def part1(filename):
    with open(filename) as f: lines = [line.split(' ') for line in f.readlines()]
    problems = [(list(line[0]), list(map(int, line[1].split(',')))) for line in lines]
    return sum([num_sols(row, nums) for row, nums in problems])


match_hashes = re.compile('#+')

def type_a(row, nums, saved):
    #print("type a row=", row, "nums=", nums)
    if len(row) < sum(nums) + len(nums) - 1: return 0
    else: return math.comb(len(row) - sum(nums) + 1, len(nums))

def type_b(row, nums, saved):
    #print("type b row=", row, "nums=", nums)
    if len(row) < sum(nums)+len(nums)-1: return 0 # not enough space
    if (row, str(nums)) in saved.keys():
        #print(f"saved time! row={row}, nums={nums}, combs={saved[(row, str(nums))]}")
        return saved[(row, str(nums))]
    block = match_hashes.search(row)
    combs = 0
    for i, num in enumerate(nums):
        if num >= block.end() - block.start():
            for j in range(max(0,block.end()-num), min(block.start()+1,len(row)-num+1)):
                if j+num < len(row) and row[j+num] == 0: continue
                combs += solve(row[:max(j-1,0)], nums[:i], saved) * solve(row[j+num+1:], nums[i+1:], saved)
        else: continue
    saved[(row, str(nums))] = combs
    return combs

# def type_c(row, nums, saved):
#     print('type c')
#     if len(row) < sum(nums)+len(nums)-1: return 0 # not enough space
#     block = match_hashes.search(row)
#     combs = 0
#     for i, num in enumerate(nums):
#         if num >= block.end() - block.start():
#             for j in range(max(0,block.end()-num), min(block.start()+1,len(row)-num)):
#                 combs += type_a(row[:j-1], nums[:i], saved) * solve(row[j+num+1:], nums[i+1:], saved)
#         else: continue
#     saved[(row, str(nums))] = combs
#     return 0


def type_c(row, nums, saved):
    if len(row) < sum(nums)+len(nums)-1: return 0 # not enough space
    groups = re.split('\.+', ''.join(row), 1)
    combs = solve(groups[1], nums, saved) # default - don't add anything to bucket 1
    #print("combs is now", combs, "row=", row, "nums=", nums, "groups=", groups)
    first_nums = []
    for i, num in enumerate(nums):
        if len(groups[0]) >= sum(first_nums) + len(first_nums) + num:
            first_nums.append(num)
            combs += solve(groups[0], first_nums, saved) * solve(groups[1], nums[i+1:], saved)
        else: break
    return combs

def solve(row, nums, saved):
    if not nums:
        return 0 if '#' in row else 1
    if '.' in row:
        return type_c(row, nums, saved)
    blocks = re.findall('#+', row)
    if len(blocks) >= 1:
        return type_b(row, nums, saved)
    #elif len(blocks) == 1:
    #    return type_b(row, nums, saved)
    else:
        return type_a(row, nums, saved)

def part2(filename):
    with open(filename) as f: lines = [line.split(' ') for line in f.readlines()]
    problems = [(((line[0]+'?')*k)[:-1], list(map(int, line[1].split(',')))*k) for line in lines]
    #print([(''.join(row), nums) for row, nums in problems])
    #rowx, numsx = problems[1]
    rowx, numsx = ('??#?????#??#', [1, 1, 7])
    saved = {}
    count = solve(rowx, numsx, saved)
    incorrect = 0
    for i, problem in enumerate(problems):
        rowsy, numsy = problem
        saved = {}
        guess = solve(rowsy, numsy, saved)
        correct = num_sols(list(rowsy), numsy)
        if guess != correct:
            incorrect += 1
            print(f"On problem {i}: {problem}, guessed {guess}, correct was {correct}")
    print(f"{incorrect} problems incorrect!")
    #return count
    #print(list_sols(list(rowx), numsx))
    #return num_sols(list(rowx), numsx)
    #return sum([num_sols(row, nums) for row, nums in problems])

print(part1('input'))
print(part2('input'))
