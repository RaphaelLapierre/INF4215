import math

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
    max_r =  math.ceil(math.sqrt((max_x - min_x) ** 2 + (max_y - min_y) ** 2) / 2)
    r_step = max_r / 10
    positions = Positions

    frontier = set()
    frontier.add(State([], Positions))
    current = None

    print(min_x)
    print(max_x)
    print(min_y)
    print(max_y)
    print(x_step)
    print(y_step)
    print(r_step)
    
    while frontier:
        current = min(frontier, key=lambda x: x.cost(K,C) + heuristic(x))

        if current.is_solution():
            print(current)
            break
        
        frontier = frontier.union(childs(current))
        frontier.remove(current)


def heuristic(state):
    return 0;

def childs(state):
    children = set()
    for i in range(min_x, max_x, x_step):
        for j in range(min_y, max_y, y_step):
            for k in range(1, int(max_r), int(r_step)):
                if is_useful((i,j,k), state.remaining_positions) and len(children) < 10:
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
    antennas = []
    remaining_positions = []

    def __init__(self, antennas, remaining_positions):
        self.antennas = list(antennas)
        self.remaining_positions = list(remaining_positions)

    def cost(self, K, C):
        return sum([K + C * antenna[2] for antenna in self.antennas])

    def verify_cover(self, position, antenna):
        return dist_squared(position, (antenna[0], antenna[1])) <= antenna[2] ** 2

    def add_antenna(self, antenna):
        self.antennas.append(antenna)
        self.remaining_positions = [pos for pos in self.remaining_positions if not self.verify_cover(pos, antenna)]

    def dist_squared(self, pos1, pos2):
        return (pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2

    def is_solution(self):
        return not self.remaining_positions

    def __str__(self):
        return str(self.antennas)

def main():
    search([(30, 0), (10, 10), (20, 30), (30, 40), (50, 40)], 200, 1)

if __name__ == "__main__":
    main()


