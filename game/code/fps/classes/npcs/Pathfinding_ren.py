import heapq

"""renpy
init python:
"""

## A* pathfinding
class Pathfinding():

    DIRECTIONS = (
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1),
        )

    def __init__(self, _actor):
        self._actor = _actor

    @property
    def world_map(self):
        return self._actor.game.map.world_map


    #region Public methods

    def find_path(self, start, goal):

        if not self._is_walkable(*start):
            return None

        if not self._is_walkable(*goal):
            return None

        open_heap = []
        heapq.heappush(open_heap, (0, start))

        came_from = {}

        g_score = {start: 0}
        f_score = {start: self._heuristic(start, goal)}

        closed_set = set()

        while open_heap:

            _, current = heapq.heappop(open_heap)

            if current == goal:
                return self._reconstruct_path(
                    came_from,
                    current
                )

            if current in closed_set:
                continue

            closed_set.add(current)

            for neighbor in self._get_neighbors(*current):

                tentative_g = g_score[current] + 1

                if (
                    neighbor not in g_score or
                    tentative_g < g_score[neighbor]
                ):

                    came_from[neighbor] = current

                    g_score[neighbor] = tentative_g

                    f = tentative_g + self._heuristic(
                        neighbor,
                        goal
                    )

                    f_score[neighbor] = f

                    heapq.heappush(
                        open_heap,
                        (f, neighbor)
                    )

        return None

    #endregion

    #region Private methods

    def _is_walkable(self, x, y):
        cell = self.world_map.get((x, y))

        return cell is not None and cell.is_npc_walkable


    def _heuristic(self, a, b):
        # Manhattan distance
        return abs(a[0] - b[0]) + abs(a[1] - b[1])


    def _get_neighbors(self, x, y):

        neighbors = []

        for dx, dy in Pathfinding.DIRECTIONS:
            nx = x + dx
            ny = y + dy

            if (self._is_walkable(nx, ny)):
                neighbors.append((nx, ny))

        return neighbors


    def _reconstruct_path(self, came_from, current):
        path = [current]

        while current in came_from:
            current = came_from[current]
            path.append(current)

        path.reverse()
        return path

    #endregion
