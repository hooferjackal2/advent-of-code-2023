import re

def part1(filename):
    gamesum = 0
    gamecount = 0
    with open(filename) as inputlines:
        redre = re.compile("\d*(?= red)")
        greenre = re.compile("\d*(?= green)")
        bluere = re.compile("\d*(?= blue)")
        for line in inputlines:
            gamecount += 1
            valid = True
            pulls = line.split(';')
            for pull in pulls:
                numred = redre.search(pull)
                numgreen = greenre.search(pull)
                numblue = bluere.search(pull)
                if numred and int(numred.group()) > 12:
                    valid = False
                if numgreen and int(numgreen.group()) > 13:
                    valid = False
                if numblue and int(numblue.group()) > 14:
                    valid = False
            if valid:
                gamesum += gamecount
    return gamesum


def part2(filename):
    powersum = 0
    gamecount = 0
    with open(filename) as inputlines:
        redre = re.compile("\d*(?= red)")
        greenre = re.compile("\d*(?= green)")
        bluere = re.compile("\d*(?= blue)")
        for line in inputlines:
            minred = 0
            mingreen = 0
            minblue = 0
            pulls = line.split(';')
            for pull in pulls:
                numred = redre.search(pull)
                numgreen = greenre.search(pull)
                numblue = bluere.search(pull)
                if numred:
                    minred = max(minred, int(numred.group()))
                if numgreen:
                    mingreen = max(mingreen, int(numgreen.group()))
                if numblue:
                    minblue = max(minblue, int(numblue.group()))
            powersum += minred * mingreen * minblue
    return powersum


print(part1("input"))
print(part2("input"))