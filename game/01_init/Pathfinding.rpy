init python:
    import heapq
    ## A* pathfinding
    class Pathfinding():

        DIRECTIONS = (
                (1, 0),
                (-1, 0),
                (0, 1),
                (0, -1),
            )

        ## 0 - walkable
        ## 1 - not-walkable
        def __init__(self, grid):
            self.grid = grid
            self.height = len(grid)
            self.width = len(grid[0]) if self.height else 0


        def in_bounds(self, x, y):
            return (
                0 <= x < self.width and
                0 <= y < self.height
            )


        def is_walkable(self, x, y):
            return self.grid[y][x] == 0


        def heuristic(self, a, b):
            # Manhattan distance
            return abs(a[0] - b[0]) + abs(a[1] - b[1])


        def get_neighbors(self, x, y):
            
            neighbors = []

            for dx, dy in Pathfinding.DIRECTIONS:
                nx = x + dx
                ny = y + dy

                if self.in_bounds(nx, ny) and self.is_walkable(nx, ny):
                    neighbors.append((nx, ny))

            return neighbors


        def reconstruct_path(self, came_from, current):
            path = [current]

            while current in came_from:
                current = came_from[current]
                path.append(current)

            path.reverse()
            return path


        def find_path(self, start, goal):
            if not self.is_walkable(*start):
                return None

            if not self.is_walkable(*goal):
                return None

            open_heap = []
            heapq.heappush(open_heap, (0, start))

            came_from = {}

            g_score = {start: 0}
            f_score = {start: self.heuristic(start, goal)}

            closed_set = set()

            while open_heap:

                _, current = heapq.heappop(open_heap)

                if current == goal:
                    return self.reconstruct_path(
                        came_from,
                        current
                    )

                if current in closed_set:
                    continue

                closed_set.add(current)

                for neighbor in self.get_neighbors(*current):

                    tentative_g = g_score[current] + 1

                    if (
                        neighbor not in g_score or
                        tentative_g < g_score[neighbor]
                    ):

                        came_from[neighbor] = current

                        g_score[neighbor] = tentative_g

                        f = tentative_g + self.heuristic(
                            neighbor,
                            goal
                        )

                        f_score[neighbor] = f

                        heapq.heappush(
                            open_heap,
                            (f, neighbor)
                        )

            return None