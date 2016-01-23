import itertools
from smallestenclosingcircle import make_circle

def partition(collection):
    if len(collection) == 1:
        yield [ collection ]
        return

    first = collection[0]
    for smaller in partition(collection[1:]):
        # insert `first` in each of the subpartition's subsets
        for n, subset in enumerate(smaller):
            yield smaller[:n] + [[ first ] + subset]  + smaller[n+1:]
        # put `first` in its own subset 
        yield [ [ first ] ] + smaller

def find_solution(groups):
    antennas = [];
    for positions in groups:
        ant = make_circle(positions);
        antennas.append(ant)
    return antennas

def cost(antennas):
    return sum([200 + 1 * antenna[2] for antenna in antennas])

def search(Positions, K, C):
    solution = []
    for c in partition(Positions):
        sol = find_solution(c)
        solution.append(sol)
        print(len(sol))
        print(str(sol) + ": " + str(cost(sol)))
    return min(solution, key=lambda x : cost(x))

def main():
    #search([1,2,3, 4],200,1)
    cost([(20,0,14), (10,10,10)])
    solution = search([(30, 0), (10, 10), (20, 30), (30, 40), (50, 40)], 200, 1)
    print(solution)
    print(cost(solution))

if __name__ == "__main__":
    main()