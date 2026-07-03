init python:
    class DoorCell(CellBase):
        def __init__(self, coordinate, image, slim_side_image, offset=0.5, orientation="horizontal"):
            super().__init__(coordinate)

            self.type = "door"
            self.images = [image, slim_side_image]
            self.image_ratios = [1, 0.125]
            self.offset = offset
            self.orientation = orientation
            self.open_amount = 0.0
            self.thickness = 0.125
            self.speed = 2.5
            self.is_open_state = False

            self.open_audio = "audio/fps/map/doors/door_open.ogg"
            self.close_audio = "audio/fps/map/doors/door_close.ogg"
        

        def intersect(self, player_x, player_y, ray_dx, ray_dy):
            
            min_x, max_x, min_y, max_y = self.get_aabb()

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
            
            texture_index = 0

            if self.orientation == "horizontal":
                if face in ("top", "bottom"):
                    # Large faces
                    offset = hit_x - (self.coord_x + self.open_amount)
                else:
                    # Thin ends
                    offset = (hit_y - min_y) / self.thickness
                    texture_index = 1

            else:
                if face in ("left", "right"):
                    # Large faces
                    offset = hit_y - (self.coord_y + self.open_amount)
                else:
                    # Thin ends
                    offset = (hit_x - min_x) / self.thickness
                    texture_index = 1

            return depth, offset, texture_index
        

        @property
        def interactable(self):

            ## door is only interactable when it is fully open or closed
            return ((self.open_amount == 1.0 and self.is_open_state) or
                    (self.open_amount == 0.0 and not self.is_open_state))


        def interact(self):

            if (not self.is_open_state and self.open_audio is not None):
                renpy.play(self.open_audio)

            if (self.is_open_state and self.close_audio is not None):
                renpy.play(self.close_audio)

            self.is_open_state = not self.is_open_state


        def update(self, delta_time):

            if (self.is_open_state):
                if (self.open_amount < 1.0):
                    self.open_amount = clamp01(self.open_amount + self.speed * delta_time)
            else:
                if (self.open_amount > 0.0):
                    self.open_amount = clamp01(self.open_amount - self.speed * delta_time)


        def get_aabb(self):

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
            
            return min_x, max_x, min_y, max_y


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
        

        def blocks_movement(self, x, y, radius):

            if (self.open_amount >= 1.0):
                return False

            min_x, max_x, min_y, max_y = self.get_aabb()

            closest_x = clamp(x, min_x, max_x)
            closest_y = clamp(y, min_y, max_y)
            
            dx = x - closest_x
            dy = y - closest_y

            return dx ** 2 + dy ** 2 < radius ** 2

            return (min_x <= x <= max_x and
                    min_y <= y <= max_y)


define FPS_DOOR_TEXTURES = {
    0: Image("images/fps/textures/doors/metal_door.png", oversample=0.25),
    1: Image("images/fps/textures/doors/blue_door.png", oversample=0.25),
    1000: Image("images/fps/textures/doors/door_slim_side.png", oversample=0.25)
}