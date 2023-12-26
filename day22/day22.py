import re
import copy

class Brick:
    def __init__(self, xcoords, ycoords, zcoords):
        self.xcoords = xcoords
        self.ycoords = ycoords
        self.zcoords = zcoords
        self.supported = False
        self.supported_by = []
        self.dependencies = []
        self.is_important = False

    def __lt__(self, other):
        return self.zcoords[0] < other.zcoords[0]

    def __str__(self):
        return f'Brick with coords x={self.xcoords}, y={self.ycoords}, z={self.zcoords}'

    def update_supported(self, other_bricks):
        self.supported = False
        self.supported_by = []
        if self.zcoords[0] == 1:
            self.supported = True
        for other in other_bricks:
            if (other.zcoords[1] == self.zcoords[0] - 1 and self.xcoords[1] >= other.xcoords[0]
            and other.xcoords[1] >= self.xcoords[0] and self.ycoords[1] >= other.ycoords[0]
            and other.ycoords[1] >= self.ycoords[0]):
                self.supported_by.append(other)
                self.supported = True

    def get_below(self, other_bricks):
        below = []
        if self.zcoords[0] == 1:
            return below
        for other in other_bricks:
            if (other.zcoords[1] < self.zcoords[0] and self.xcoords[1] >= other.xcoords[0]
            and other.xcoords[1] >= self.xcoords[0] and self.ycoords[1] >= other.ycoords[0]
            and other.ycoords[1] >= self.ycoords[0]):
                below.append(other)
        return below

    def fall(self, other_bricks):
        self.update_supported(other_bricks)
        if self.supported:
            return
        below = self.get_below(other_bricks)
        if not below:
            dist = self.zcoords[0] - 1
        else:
            target = max(below, key=lambda brick: brick.zcoords[1])
            dist = self.zcoords[0] - target.zcoords[1] - 1
        self.zcoords = [coord - dist for coord in self.zcoords]
        self.update_supported(other_bricks)

def brick_setup(rawbricks):
    bricks = []
    for rawbrick in rawbricks:
        c = [int(coord) for coord in re.findall('\d+', rawbrick)]
        bricks.append(Brick([c[0], c[3]],[c[1], c[4]],[c[2], c[5]]))
    bricks.sort()
    for brick in bricks:
        brick.fall(bricks)
    bricks.sort()
    return bricks

def part1(filename):
    with open(filename) as f: rawbricks = f.readlines()
    bricks = brick_setup(rawbricks)
    for brick in bricks:
        if len(brick.supported_by) == 1:
            brick.supported_by[0].is_important = True
    return sum(not brick.is_important for brick in bricks)

def part2(filename):
    with open(filename) as f: rawbricks = f.readlines()
    bricks = brick_setup(rawbricks)
    for brick in bricks:
        if len(brick.supported_by) == 1:
            brick.supported_by[0].is_important = True
        for support in brick.supported_by: support.dependencies.append(brick)
    chain_sum = 0
    for brick in bricks:
        # Simulate a chain collapse
        frontier = brick.dependencies
        collapsed = [brick]
        while frontier:
            nextbrick = frontier.pop(0)
            if nextbrick in collapsed: continue
            allcollapsed = True
            for support in nextbrick.supported_by:
                if support not in collapsed: allcollapsed = False
            if allcollapsed:
                collapsed.append(nextbrick)
                frontier += nextbrick.dependencies
        chain_sum += len(collapsed) - 1
    return chain_sum

print(part1('input'))
print(part2('input'))
