import math
import random
import time
import matplotlib.pyplot as pyplot
from matplotlib.pyplot import Figure, subplot
from smallestenclosingcircle import make_circle

K = 0
C = 0

positions = []

def search(Positions, k, c):
    global K
    global C
    K = k
    C = c

    global positions
    positions = Positions

    frontier = set()
    frontier.add(State({}, Positions))
    current = None
    
    while frontier:
        current = min(frontier, key=lambda x: x.cost(K,C)) 
        if current.is_solution():
            break
        
        frontier = frontier.union(current.childs())
        frontier.remove(current)
        
    return current


def dist_squared(pos1, pos2):
    return (pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2


class State:
    antennas = tuple()
    remaining_positions = tuple()

    def __init__(self, antennas, remaining_positions):
        self.antennas = tuple(antennas)
        self.remaining_positions = tuple(remaining_positions)

    def cost(self, K, C):
        return sum([K + C * antenna[2]**2 for antenna in self.antennas])

    def verify_cover(self, position, antenna):
        return dist_squared(position, (antenna[0], antenna[1])) <= antenna[2] ** 2

    def add_antenna(self, antenna):
        self.antennas = self.antennas + (antenna, )
        self.remaining_positions = tuple([pos for pos in self.remaining_positions if not self.verify_cover(pos, antenna)])

    def is_solution(self):
        return not self.remaining_positions

    def childs(self):
        children = []
        if not self.antennas:
            for pos in positions:
                child = State(self.antennas, self.remaining_positions)
                child.add_antenna((pos[0], pos[1], 1))
                child.remaining_positions = tuple([p for p in child.remaining_positions if p != pos])
                children.append(child)
        else:
            child = State(self.antennas, self.remaining_positions)
            pos = min(self.remaining_positions, key=lambda p : dist_squared(p, self.antennas[-1]))
            closest_antenna = min(child.antennas, key=lambda x : dist_squared(pos, (x[0],x[1])))
            #les points couvert par l'antenne
            covered_points = [p for p in positions if child.verify_cover(p, closest_antenna)]
            covered_points.append(pos)
            new_antenna = make_circle(covered_points)
            if((K+C*new_antenna[2]**2) > (K+C*closest_antenna[2]**2 + K)):
               new_antenna = (pos[0], pos[1], 1)
            else:
                child.antennas = tuple([ant for ant in child.antennas if ant != closest_antenna])
            child.add_antenna(new_antenna)
            #child.remaining_positions = tuple([p for p in child.remaining_positions if p != pos])
            children.append(child)
        return children

    def __eq__(self, other):
        return other and sorted(self.antennas) == sorted(other.antennas)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self, **kwargs):
        return hash(self.antennas)

    def __str__(self):
        return str(self.antennas)

def main():
    #points = [(30, 0), (10, 10), (25,20),(20, 30), (30, 40), (40, 50), (30, 99)];
    #points = [(30, 0), (10, 10), (20,20), (30, 40),(50,40)];
    points = random_pos(20, 100)
    fig=pyplot.figure(1)
    ax = fig.add_subplot(1,1,1)
    pyplot.scatter(*zip(*points),marker='x' )
    before = time.clock()
    result = search(points, 200, 1)
    temp = time.clock() - before
    print("Temps: " + str(temp))
    print("Cout: " + str(result.cost(K,C)))
    for antenna in result.antennas:
        circle = pyplot.Circle((antenna[0],antenna[1]), antenna[2], color='g', fill=False)
        ax.add_patch(circle)

    limx = pyplot.xlim()
    limy = pyplot.ylim()
    pyplot.xlim(0, max(limy[1], limx[1]))
    pyplot.ylim(0, max(limy[1], limx[1]))
    ax.set_aspect(1);

    pyplot.show()

def random_pos(numPos, max):
    points = []
    random.seed()
    for _ in range(0, numPos):
        points.append((random.randrange(0, max), random.randrange(0, max)))
    return points

if __name__ == "__main__":
    for _ in range(0, 10):
        main()


