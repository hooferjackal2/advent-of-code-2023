import re

def part1(filename):
    scoresum = 0
    with open(filename) as inputlines:
        for line in inputlines:
            score = 0
            strsides = line.split(':')[1].split('|')
            winnums = [int(num) for num in re.split('\s+', strsides[0].strip())]
            mynums = [int(num) for num in re.split('\s+', strsides[1].strip())]
            winnums.sort()
            mynums.sort()
            i1 = 0
            for i2 in range(len(mynums)):
                while i1 < len(winnums) and winnums[i1] < mynums[i2]:
                    i1 += 1
                if i1 >= len(winnums): break
                if winnums[i1] == mynums[i2]:
                    score = 1 if score == 0 else 2*score
            scoresum += score
    return scoresum


def part2(filename):
    with open(filename) as inputfile:
        inputlines = inputfile.readlines()
        numcards = [1]*len(inputlines)
        for line_idx in range(len(inputlines)):
            line = inputlines[line_idx]
            matches = 0
            strsides = line.split(':')[1].split('|')
            winnums = [int(num) for num in re.split('\s+', strsides[0].strip())]
            mynums = [int(num) for num in re.split('\s+', strsides[1].strip())]
            winnums.sort()
            mynums.sort()
            i1 = 0
            for i2 in range(len(mynums)):
                while i1 < len(winnums) and winnums[i1] < mynums[i2]:
                    i1 += 1
                if i1 >= len(winnums): break
                if winnums[i1] == mynums[i2]:
                    matches += 1
            for i in range(line_idx + 1, line_idx + matches + 1):
                try:
                    numcards[i] += numcards[line_idx]
                except IndexError: pass
    return sum(numcards)


print(part1('input'))
print(part2('input'))
