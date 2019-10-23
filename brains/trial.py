import heapq


class SquareGrid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.walls = []

    def in_bounds(self, loc):
        (x, y) = loc
        return 0 <= x < self.width and 0 <= y < self.height

    def passable(self, loc):
        return loc not in self.walls

    def neighbors(self, loc):
        (x, y) = loc
        results = [(x+1, y), (x, y-1), (x-1, y), (x, y+1)]
        results = filter(self.in_bounds, results)
        results = filter(self.passable, results)
        return list(results)


class GridWithWeights(SquareGrid):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.weights = {}

    def cost(self, from_node, to_node):
        return self.weights.get(to_node, 1)


class PriorityQueue:
    def __init__(self):
        self.elements = []

    @property
    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]


def reconstruct_path(came_from, start, goal):
    current = goal
    path = []
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)  # optional
    path.reverse()  # optional
    return path


def heuristic(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)


def a_star_search(graph, start, goal):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty:
        current = frontier.get()

        if current == goal:
            break

        for next in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, next)
            if new_cost < cost_so_far.get(next, float('inf')):
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(goal, next)
                frontier.put(next, priority)
                came_from[next] = current

    return came_from, cost_so_far


def scan_map(game):
    game_map = []
    walls = []
    weighted = []
    for y in range(8):
        row = []
        for x in range(10):
            tile = game.radar(x, y)
            if tile[0] in game.UNSAFE_TILES or tile[1] in (game.ROCK, game.TREE):
                walls.append((x, y))
            if tile[0] == game.DIRT:
                weighted.append((x, y))
            row.append(tile)
        game_map.append(row)
    return game_map, walls, weighted


def think(game):
    game_map, walls, weighted = scan_map(game)

    diag = GridWithWeights(10, 8)
    diag.walls = walls
    diag.weights = {loc: 2 for loc in weighted}

    current_loc = game.position
    enemy_loc = game.tank_positions[0]
    came_from, cost_so_far = a_star_search(diag, current_loc, enemy_loc)
    path = reconstruct_path(came_from, current_loc, enemy_loc)
    print('PATH:', path)
