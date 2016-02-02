import math
import random
import time
import matplotlib.pyplot as pyplot
from matplotlib.pyplot import Figure, subplot
from smallestenclosingcircle import make_circle


def search(Positions, k, c):
    solution = greedy_solution(Positions, k, c)
    print(str(cout(solution, k,c)))
    meilleur = solution
    T = 500.0
    theta = T
    P = 50
    Kmax = 50
    alpha = 0.8;

    for i in range(0, Kmax):
        for j in range(1, P+1):
            voisin = find_neighbour(solution, Positions)
            delta = cout(solution, k, c) - cout(voisin, k, c)
            if CritereMetropolis(delta, theta):
                print("Nouvelle solution: " + str(cout(voisin, k, c)))
                solution = voisin
                if cout(solution, k, c) < cout(meilleur, k , c):
                    meilleur = solution
                    print("Nouveau meilleux: " + str(cout(meilleur, k, c)))
        theta *= alpha


    return meilleur

def find_neighbour(solution, positions):
    if len(solution) <= 1:
        return solution

    antenna = solution[int(random.random() * len(solution))]
    closest_antenna = min([ant for ant in solution if ant != antenna], key=lambda a : dist_squared(a, antenna))
    ant1_coverage = [p for p in positions if verify_cover(p, antenna)]
    ant2_coverage = [p for p in positions if verify_cover(p, closest_antenna)]

    le_point = min(ant2_coverage, key=lambda pos : dist_squared(pos, antenna))
    ant2_coverage = [p for p in ant2_coverage if p != le_point]
    ant1_coverage.append(le_point)

    new_ant1 = make_circle(ant1_coverage);
    new_ant2 = make_circle(ant2_coverage);

    solution = [ant for ant in solution if (ant != antenna and ant != closest_antenna)]
    if new_ant1:
        solution.append(new_ant1)
    if new_ant2:
        solution.append(new_ant2)

    return solution

def cout(solution, K, C):
    return sum([K + C * antenna[2]**2 for antenna in solution])

def greedy_solution(remaining_positions, k, c):
    positions = list(remaining_positions)
    if not remaining_positions:
        return

    antennas = [(remaining_positions[0][0], remaining_positions[0][1], 1)]
    remaining_positions = remaining_positions[1:]

    for pos in remaining_positions:
        closest_antenna = min(antennas, key=lambda x : dist_squared(pos, (x[0],x[1])))
        covered_points = [p for p in positions if verify_cover(p, closest_antenna)]
        covered_points.append(pos)
        new_antenna = make_circle(covered_points)

        if((k+c*new_antenna[2]**2) > (k+c*closest_antenna[2]**2 + k)):
            new_antenna = (pos[0], pos[1], 1)
        else:
            antennas = [ant for ant in antennas if ant != closest_antenna]

        antennas.append(new_antenna)
        remaining_positions = [p for p in remaining_positions if p != pos]
    return antennas

def CritereMetropolis(delta, T):
    if delta > 0:
        return True

    random.seed()
    x = delta/T
    return math.exp(x) >= random.random()

def dist_squared(pos1, pos2):
    return (pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2


def verify_cover(position, antenna):
    return dist_squared(position, (antenna[0], antenna[1])) <= antenna[2] ** 2


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
    for antenna in result:
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
        main()


