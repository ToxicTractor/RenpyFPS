import math
from abc import ABC, abstractmethod
from game.code.fps.enums.ECellType_ren import ECellType
from game.code.fps.other.helper_functions_ren import clamp
from game.code.fps.other.named_tuples_ren import Vector2
from game.code.fps.other.named_tuples_ren import AABB

"""renpy
init -3 python:
"""

class CellBase(ABC):
    def __init__(self, coord):
        self.type = ECellType.Empty
        self.coord = Vector2(*coord)
        self._cached_aabb = None

    @property
    def is_npc_walkable(self):
        return False


    @abstractmethod
    def get_texture(self, side):
        pass

    def update(self, delta_time):
        pass

    def is_interactable(self, side):
        return False


    def get_aabb(self):
        if (self._cached_aabb):
            return self._cached_aabb

        min_x = self.coord.x
        min_y = self.coord.y
        max_x = self.coord.x + 1
        max_y = self.coord.y + 1

        self._cached_aabb = AABB(min_x, min_y, max_x, max_y)

        return self._cached_aabb


    def check_collision(self, x, y, radius):

        min_x, min_y, max_x, max_y = self.get_aabb()

        closest_x = clamp(x, min_x, max_x)
        closest_y = clamp(y, min_y, max_y)

        dx = x - closest_x
        dy = y - closest_y

        collides = dx ** 2 + dy ** 2 < radius ** 2

        ## we dont need to calculate distance and penetration if we dont collide
        if (not collides):
            return collides, None, None, None, None

        distance = math.sqrt(dx ** 2 + dy ** 2)
        penetration = radius - distance

        return collides, dx, dy, distance, penetration
