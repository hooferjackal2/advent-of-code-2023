import re

def part1(filename):
    csum = 0
    with open(filename) as inputlines:
        startre = re.compile("^.*?\d")
        endre = re.compile("\d\D*$")
        for line in inputlines:
            try:
                cval = int(startre.search(line).group()[-1]+endre.search(line).group()[0])
                csum += cval
            except AttributeError:
                continue
    return csum


def substr_list_search(fullstr, substr_list, i):
    for substr in substr_list:
        if i + len(substr) > len(fullstr):
            continue
        if substr == fullstr[i:i+len(substr)]:
            return substr
    return None


def part2(filename):
    csum = 0
    numstrings = {'one': 1, '1': 1,
                  'two': 2, '2': 2,
                  'three': 3, '3': 3,
                  'four': 4, '4': 4,
                  'five': 5, '5': 5,
                  'six': 6, '6': 6,
                  'seven': 7, '7': 7,
                  'eight': 8, '8': 8,
                  'nine': 9, '9': 9,
                  'ten': 10, '10': 10}
    substr_list = numstrings.keys()
    with open(filename) as inputlines:
        for line in inputlines:
            cnum = 0
            for i in range(len(line)):
                result = substr_list_search(line, substr_list, i)
                if result:
                    cnum += 10*numstrings[result]
                    break
            for i in range(len(line), 0, -1):
                result = substr_list_search(line, substr_list, i-1)
                if result:
                    cnum += numstrings[result]
                    break
            csum += cnum
    return csum

print(part1("input"))
print(part2("input"))