import math
import random
import time
import matplotlib.pyplot as pyplot
from matplotlib.pyplot import Figure, subplot
from smallestenclosingcircle import make_circle


min_x = 0
min_y = 0
max_x = 0
max_y = 0
max_r = 0

x_step = 0
y_step = 0
r_step = 0

positions = []

def search(Positions, K, C):
    global min_x
    global max_x
    global min_y
    global max_y
    min_x = min([position[0] for position in Positions])
    max_x = max([position[0] for position in Positions])
    min_y = min([position[1] for position in Positions])
    max_y = max([position[1] for position in Positions])

    global x_step 
    global y_step 
    x_step = (max_x - min_x) / 10 
    y_step = (max_y - min_y) / 10

    global positions
    global max_r
    global r_step
    max_r =  min(math.ceil(math.sqrt((max_x - min_x) ** 2 + (max_y - min_y) ** 2) / 2), K/C)
    r_step = max_r / 10
    positions = Positions

    frontier = set()
    frontier.add(State({}, Positions))
    current = None

#    print(min_x)
#    print(max_x)
#    print(min_y)
#    print(max_y)
#    print(x_step)
#    print(y_step)
#    print(r_step)

    
    while frontier:
        current = min(frontier, key=lambda x: x.cost(K,C) + heuristic(x))
        if current.is_solution():
            print(current)
            break
        
        childs = current.childs()
        frontier = frontier.union(childs)
        frontier.remove(current)
        
    return current


def max_radius(K, C):
    return K/C;

def heuristic(state):
    return 0;

def childs(state):
    children = set()
    for i in range(min_x, max_x, int(x_step)):
        for j in range(min_y, max_y, int(y_step)):
            for k in range(1, int(max_r), int(r_step)):
                if is_useful((i,j,k), state.remaining_positions):
                    child = State(state.antennas, state.remaining_positions)
                    child.add_antenna((i,j,k))
                    children.add(child)
    
    return children
    

def is_useful(antenna, remaining_positions):
    return any([dist_squared(position, (antenna[0], antenna[1])) <= antenna[2] ** 2
               for position in remaining_positions])


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
        #self.remaining_positions = tuple([pos for pos in self.remaining_positions if not self.verify_cover(pos, antenna)])

    def dist_squared(self, pos1, pos2):
        return (pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2

    def is_solution(self):
        return not self.remaining_positions

    def childs(self):
        children = []
        child = State(self.antennas, self.remaining_positions)
        if not self.antennas:
            pos = child.remaining_positions[0]
            child.add_antenna((pos[0], pos[1], 1))
            child.remaining_positions = tuple([p for p in child.remaining_positions if p != pos])
        else:
            pos = min(self.remaining_positions, key=lambda p : dist_squared(p, self.antennas[-1]))
            closest_antenna = min(child.antennas, key=lambda x : dist_squared(pos, (x[0],x[1])))
            #les points couvert par l'antenne
            covered_points = [p for p in positions if child.verify_cover(p, closest_antenna)]
            covered_points.append(pos)
            new_antenna = make_circle(covered_points)
            if((200+1*new_antenna[2]**2) > (200+1*closest_antenna[2]**2 + 200)):
               new_antenna = (pos[0], pos[1], 1)
            else:
                child.antennas = tuple([ant for ant in child.antennas if ant != closest_antenna])
            child.add_antenna(new_antenna)
            child.remaining_positions = tuple([p for p in child.remaining_positions if p != pos])
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
    print(points)
    fig=pyplot.figure(1)
    ax = fig.add_subplot(1,1,1)
    pyplot.scatter(*zip(*points))
    before = time.clock()
    result = search(points, 200, 1)
    temp = time.clock() - before
    print("Temps: " + str(temp))
    print("Cout: " + str(result.cost(200,1)))
    for antenna in result.antennas:
        circle = pyplot.Circle((antenna[0],antenna[1]), antenna[2], color='g', fill=False)
        ax.add_patch(circle)

    limx = pyplot.xlim()
    limy = pyplot.ylim()
    pyplot.xlim(0, max(limy[1], limx[1]))
    pyplot.ylim(0, max(limy[1], limx[1]))


    pyplot.show()

def random_pos(numPos, max):
    points = []
    random.seed()
    for _ in range(0, numPos):
        points.append((random.randrange(0, max), random.randrange(0, max)))
    return points

if __name__ == "__main__":
    main()


