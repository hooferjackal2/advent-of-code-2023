import re
import random
from numpy.polynomial import Polynomial

class Vec:
    def __init__(self, vals):
        self.x = vals[0]
        self.y = vals[1]
        self.z = 0 if len(vals) < 3 else vals[2]

    def __str__(self):
        return f'x={self.x}, y={self.y},z z={self.z}'

    def __add__(self, other):
        return Vec([self.x+other.x, self.y+other.y, self.z+other.z])

    def __sub__(self, other):
        return Vec([self.x-other.x, self.y-other.y, self.z-other.z])

    def __mul__(self, other):
        return Vec([self.x * other, self.y * other, self.z * other])

    def __truediv__(self, other):
        return Vec([self.x / other, self.y / other, self.z / other])

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def perp(self):
        return Vec([-self.y, self.x])

    def mag(self):
        return self.x ** 2 + self.y ** 2 + self.z ** 2

class Trajectory2D:
    def __init__(self, pos, vel):
        self.pos = Vec(pos)
        self.vel = Vec(vel)

    def __str__(self):
        return f'Vector with position {self.pos} and velocity {self.vel}'

    def d(self):
        return self.pos.y * self.vel.x - self.pos.x * self.vel.y

    def in_front(self, point):
        return (point - self.pos).dot(self.vel) >= 0

    def find_intersection(self, other):
        div = other.vel.perp().dot(self.vel)
        if div == 0:
            return None
        point = Vec([(self.vel.x * other.d() - other.vel.x * self.d()) / div,
                 (self.vel.y * other.d() - other.vel.y * self.d()) / div])
        if self.in_front(point) and other.in_front(point):
            return point
        else:
            return None

class Trajectory3D:
    def __init__(self, pos, vel):
        self.pos = Vec(pos)
        self.vel = Vec(vel)
        #self.t = random.randint(0, 1000000000000)
        self.t = random.randint(0, 10)

    def __str__(self):
        return f'Vector with position {self.pos} and velocity {self.vel}'

    def adjust_time(self, other):
        proj = other.vel - self.vel * (other.vel.dot(other.vel) / self.vel.dot(other.vel))
        self.t = proj.dot(other.pos - self.pos) / proj.dot(self.vel)

def part1(filename):
    with open(filename) as f: lines = f.readlines()
    vecdata = [list(map(float, re.findall('-?\d+', line))) for line in lines]
    trajectories = [Trajectory2D(vec[:2], vec[3:5]) for vec in vecdata]
    total_collisions = 0
    for i, tr1 in enumerate(trajectories):
        for tr2 in trajectories[i + 1:]:
            inter = tr1.find_intersection(tr2)
            if inter and 200000000000000 <= inter.x <= 400000000000000 and 200000000000000 <= inter.y <= 400000000000000:
                total_collisions += 1
    return total_collisions

def part2(filename):
    with open(filename) as f: lines = f.readlines()
    vecdata = [list(map(float, re.findall('-?\d+', line))) for line in lines]
    trajectories = [Trajectory3D(vec[:3], vec[3:]) for vec in vecdata]
    pos_best = [0, 0, 0]
    vel_best = [0, 0, 0]
    for i in range(500):
        #print('iteration', i)
        #print([tr.t for tr in trajectories], [tr.pos.x + tr.t * tr.vel.x for tr in trajectories])
        pos_best[0], vel_best[0] = Polynomial.fit([tr.t for tr in trajectories],
                                                  [tr.pos.x + tr.t * tr.vel.x for tr in trajectories], 1).convert()
        pos_best[1], vel_best[1] = Polynomial.fit([tr.t for tr in trajectories],
                                                  [tr.pos.y + tr.t * tr.vel.y for tr in trajectories], 1).convert()
        pos_best[2], vel_best[2] = Polynomial.fit([tr.t for tr in trajectories],
                                                  [tr.pos.z + tr.t * tr.vel.z for tr in trajectories], 1).convert()
        #print(pos_best, vel_best)
        best_fit = Trajectory3D(pos_best, vel_best)
        for tr in trajectories:
            tr.adjust_time(best_fit)
        #    print(tr.t)
    print(list(map(round, pos_best)))
    return sum(list(map(round, pos_best)))

print(part1('input'))
print(part2('input'))
