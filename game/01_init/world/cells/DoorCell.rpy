init python:
    class DoorCell(CellBase):
        def __init__(self, coord, image, slim_side_image, offset=0.0, orientation=EOrientation.Horizontal):
            super().__init__(coord)

            self.type = ECellType.Door
            self.images = [image, slim_side_image]
            self.image_ratios = [1, 0.125]
            self.offset = offset
            self.orientation = orientation
            self.open_amount = 0.0
            self.thickness = 0.125
            self.speed = 2.5
            self.is_open_state = False
            self.is_locked = False

            self.open_audio = "audio/fps/map/doors/door_open.ogg"
            self.close_audio = "audio/fps/map/doors/door_close.ogg"
        
        @property
        def is_npc_walkable(self):
            return self.open_amount >= 1.0

        
        def get_texture(self, side):
            if self.orientation == EOrientation.Horizontal:
                if side in (EDirection.North, EDirection.South):
                    return self.images[0], self.image_ratios[0]
                else:
                    return self.images[1], self.image_ratios[1]
            elif self.orientation == EOrientation.Vertical:
                if side in (EDirection.West, EDirection.East):
                    return self.images[0], self.image_ratios[0]
                else:
                    return self.images[1], self.image_ratios[1]

            return None, 1.0


        def ray_intersect(self, origin_x, origin_y, ray_dx, ray_dy):
            
            aabb = self.get_aabb()
            depth = self._calculate_depth(origin_x, origin_y, ray_dx, ray_dy, aabb)

            if (depth is None or depth <= 0):
                return None

            hit_x = origin_x + depth * ray_dx
            hit_y = origin_y + depth * ray_dy

            EPSILON = 1e-6

            if abs(hit_x - aabb.min_x) < EPSILON:
                face = EDirection.West
            elif abs(hit_x - aabb.max_x) < EPSILON:
                face = EDirection.East
            elif abs(hit_y - aabb.min_y) < EPSILON:
                face = EDirection.North
            else:
                face = EDirection.South
            
            if self.orientation == EOrientation.Horizontal:
                if face in (EDirection.North, EDirection.South):
                    # Large faces
                    offset = hit_x - (self.coord_x + self.open_amount)
                else:
                    # Thin ends
                    offset = (hit_y - aabb.min_y) / self.thickness

            elif  self.orientation == EOrientation.Vertical:
                if face in (EDirection.West, EDirection.East):
                    # Large faces
                    offset = hit_y - (self.coord_y + self.open_amount)
                else:
                    # Thin ends
                    offset = (hit_x - aabb.min_x) / self.thickness

            return depth, offset, face
        

        def is_interactable(self, side):

            if (self.is_locked):
                return False

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
                    self._cached_aabb = None ## clear cached aabb to make sure we recalculate it next time we use it
            else:
                if (self.open_amount > 0.0):
                    self.open_amount = clamp01(self.open_amount - self.speed * delta_time)
                    self._cached_aabb = None


        def get_aabb(self):

            if (self._cached_aabb):
                return self._cached_aabb

            cell_x, cell_y = self.coord
        
            if (self.orientation == EOrientation.Horizontal):
                min_x = cell_x + self.open_amount
                max_x = cell_x + 1
                min_y = cell_y + 0.5 + self.offset - self.thickness / 2
                max_y = cell_y + 0.5 + self.offset + self.thickness / 2
            elif (self.orientation == EOrientation.Vertical):
                min_x = cell_x + 0.5 + self.offset - self.thickness / 2
                max_x = cell_x + 0.5 + self.offset + self.thickness / 2
                min_y = cell_y + self.open_amount
                max_y = cell_y + 1
            
            self._cached_aabb = AABB(min_x, min_y, max_x, max_y)

            return self._cached_aabb


        def _calculate_depth(self, player_x, player_y, ray_dx, ray_dy, aabb):

            if ray_dx != 0:
                tx1 = (aabb.min_x - player_x) / ray_dx
                tx2 = (aabb.max_x - player_x) / ray_dx

                tmin = min(tx1, tx2)
                tmax = max(tx1, tx2)
            else:
                if player_x < aabb.min_x or player_x > aabb.max_x:
                    return None

                tmin = -float("inf")
                tmax = float("inf")

            if ray_dy != 0:
                ty1 = (aabb.min_y - player_y) / ray_dy
                ty2 = (aabb.max_y - player_y) / ray_dy

                tmin = max(tmin, min(ty1, ty2))
                tmax = min(tmax, max(ty1, ty2))
            else:
                if player_y < aabb.min_y or player_y > aabb.max_y:
                    return None

            if tmax < tmin:
                return None

            if tmax < 0:
                return None

            return tmin


define FPS_DOOR_TEXTURES = {
    0: Image("images/fps/textures/doors/metal_door.png", oversample=0.25),
    1: Image("images/fps/textures/doors/blue_door.png", oversample=0.25),
    1000: Image("images/fps/textures/doors/door_slim_side.png", oversample=0.25)
}