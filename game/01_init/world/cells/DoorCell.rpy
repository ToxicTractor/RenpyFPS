init python:
    class DoorCell(CellBase):
        def __init__(self, coordinate, texture_id, offset=0.5, orientation="horizontal"):
            super().__init__(coordinate)

            self.type = "door"
            self.texture_id = texture_id
            self.offset = offset
            self.orientation = orientation
            self.open_amount = 0.5
            self.thickness = 0.1
        
        def intersect(self, player_x, player_y, ray_dx, ray_dy):
            
            cell_x, cell_y = self.coordinate

            if (self.orientation == "horizontal"):
                min_x = cell_x + self.open_amount
                max_x = cell_x + 1
                min_y = cell_y + self.offset - self.thickness / 2
                max_y = cell_y + self.offset + self.thickness / 2
            elif (self.orientation == "vertical"):
                min_x = cell_x + self.offset - self.thickness / 2
                max_x = cell_x + self.offset + self.thickness / 2
                min_y = cell_y + self.open_amount
                max_y = cell_y + 1.0
                
            depth = self._aabb_test(player_x, player_y, ray_dx, ray_dy, min_x, max_x, min_y, max_y)

            if (depth is None or depth <= 0):
                return None

            hit_x = player_x + depth * ray_dx
            hit_y = player_y + depth * ray_dy

            EPSILON = 1e-6

            if abs(hit_x - min_x) < EPSILON:
                face = "left"
            elif abs(hit_x - max_x) < EPSILON:
                face = "right"
            elif abs(hit_y - min_y) < EPSILON:
                face = "top"
            else:
                face = "bottom"

            if (face == "left" or face == "right"):
                offset = hit_y - math.floor(hit_y)
            else:
                offset = hit_x - math.floor(hit_x)

            return depth, offset


        def _aabb_test(self, player_x, player_y, ray_dx, ray_dy, min_x, max_x, min_y, max_y):

            if ray_dx != 0:
                tx1 = (min_x - player_x) / ray_dx
                tx2 = (max_x - player_x) / ray_dx

                tmin = min(tx1, tx2)
                tmax = max(tx1, tx2)
            else:
                if player_x < min_x or player_x > max_x:
                    return None

                tmin = -float("inf")
                tmax = float("inf")

            if ray_dy != 0:
                ty1 = (min_y - player_y) / ray_dy
                ty2 = (max_y - player_y) / ray_dy

                tmin = max(tmin, min(ty1, ty2))
                tmax = min(tmax, max(ty1, ty2))
            else:
                if player_y < min_y or player_y > max_y:
                    return None

            if tmax < tmin:
                return None

            if tmax < 0:
                return None

            return tmin
        

define FPS_DOOR_TEXTURES = {
    0: Image("images/fps/textures/doors/metal_door.png", oversample=1),
    1: Image("images/fps/textures/doors/blue_door.png", oversample=1)
}