init -1 python:
    class CellBase(ABC):
        def __init__(self, coord):
            self.type = None
            self.coord = coord
            self._cached_aabb = None
        

        @property
        def coord_x(self):
            return self.coord[0]


        @property
        def coord_y(self):
            return self.coord[1]


        @property
        def is_npc_walkable(self):
            return False
        

        def is_interactable(self, side):
            return False
        

        def get_aabb(self):
            if (self._cached_aabb):
                return self._cached_aabb

            min_x = self.coord_x
            min_y = self.coord_y
            max_x = self.coord_x + 1
            max_y = self.coord_y + 1

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
            

