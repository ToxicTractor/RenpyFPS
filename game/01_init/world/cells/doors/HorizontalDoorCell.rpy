define FPS_DOOR_TEXTURES = {
    0: Image("images/fps/textures/doors/metal_door.png", oversample=0.25),
    1: Image("images/fps/textures/doors/blue_door.png", oversample=0.25),
    1000: Image("images/fps/textures/doors/door_slim_side.png", oversample=0.25)
}

init python:
    class HorizontalDoorCell(BaseDoorCell):
        def __init__(self,            
            coord:                      tuple, 
            main_texture:               Image, 
            side_texture:               Image,
            grid_alignment:             EGridAlignment, 
            open_direction:             EDirection, 
            open_audio:                 str=None, 
            close_audio:                str=None, 
            unlock_audio:               str=None, 
            locked_interact_audio:      str=None, 
            offset:                     float=0.0,
            thickness:                  float=0.125,
            speed:                      float=2.5,
            side_texture_aspect_ratio:  float=0.125,
            start_open:                 bool=False,
            flip_main_texture:          bool=False, 
            allow_interaction:          bool=True,
            can_be_closed:              bool=True,
            is_locked:                  bool=False, 
            unlocked_by_item:           str=None,
            consumed_on_unlock_count:   int=0,
            locked_notification:        str=FpsConstants.LOCKED_DOOR_NOTIFICATION):
            super().__init__(
                coord, 
                main_texture, 
                side_texture, 
                grid_alignment, 
                open_direction, 
                open_audio, 
                close_audio, 
                unlock_audio,
                locked_interact_audio, 
                offset, 
                thickness, 
                speed, 
                side_texture_aspect_ratio, 
                start_open, 
                flip_main_texture, 
                allow_interaction,
                can_be_closed,
                is_locked,
                unlocked_by_item,
                consumed_on_unlock_count,
                locked_notification)

            self.type = ECellType.HorizontalDoor

            if (self.flip_main_texture):
                self.main_texture = Transform(main_texture, xzoom=-1)


        def update(self, delta_time):
            
            if (self.is_open_state):
                if (self.open_amount < 1.0):
                    self.open_amount = clamp01(self.open_amount + self.speed * delta_time)
                    self._cached_aabb = None ## clear cached aabb to make sure we recalculate it next time we use it
            else:
                if (self.open_amount > 0.0):
                    self.open_amount = clamp01(self.open_amount - self.speed * delta_time)
                    self._cached_aabb = None


        def ray_intersect(self, origin_x, origin_y, ray_dx, ray_dy):
            
            aabb = self.get_aabb()
            near_depth, far_depth = self._calculate_depth(origin_x, origin_y, ray_dx, ray_dy, aabb)

            if (near_depth is None or near_depth <= 0):
                return None

            hit_x = origin_x + near_depth * ray_dx
            hit_y = origin_y + near_depth * ray_dy

            EPSILON = 1e-6

            if abs(hit_x - aabb.min_x) < EPSILON:
                face = EDirection.Left
            elif abs(hit_x - aabb.max_x) < EPSILON:
                face = EDirection.Right
            elif abs(hit_y - aabb.min_y) < EPSILON:
                face = EDirection.Up
            else:
                face = EDirection.Down
            
            if self.grid_alignment == EGridAlignment.X:
                if face in FpsConstants.VERTICAL_DIRECTIONS:
                    # Large faces
                    if (self.open_direction == EDirection.Right):
                        offset = hit_x - (self.coord_x + 1 - self.open_amount)
                    else:
                        offset = hit_x - (self.coord_x + self.open_amount)
                else:
                    # Thin ends
                    offset = (hit_y - aabb.min_y) / self.thickness

            elif  self.grid_alignment == EGridAlignment.Y:
                if face in FpsConstants.HORIZONTAL_DIRECTIONS:
                    # Large faces
                    if (self.open_direction == EDirection.Right):
                        offset = hit_y - (self.coord_y + 1 - self.open_amount)
                    else:
                        offset = hit_y - (self.coord_y + self.open_amount)
                else:
                    # Thin ends
                    offset = (hit_x - aabb.min_x) / self.thickness

            ## convert to texture offset by removing coord part of the offset
            offset %= 1.0

            return near_depth, far_depth, offset, face


        def get_aabb(self):

            if (self._cached_aabb):
                return self._cached_aabb

            cell_x, cell_y = self.coord
        
            if (self.grid_alignment == EGridAlignment.X):
                if (self.open_direction == EDirection.Right):
                    min_x = cell_x
                    max_x = cell_x + 1 - self.open_amount
                else:
                    min_x = cell_x + self.open_amount
                    max_x = cell_x + 1
                min_y = cell_y + 0.5 + self.offset - self.thickness / 2
                max_y = cell_y + 0.5 + self.offset + self.thickness / 2
            elif (self.grid_alignment == EGridAlignment.Y):
                min_x = cell_x + 0.5 + self.offset - self.thickness / 2
                max_x = cell_x + 0.5 + self.offset + self.thickness / 2
                if (self.open_direction == EDirection.Right):
                    min_y = cell_y
                    max_y = cell_y + 1 - self.open_amount
                else:
                    min_y = cell_y + self.open_amount
                    max_y = cell_y + 1
            
            self._cached_aabb = AABB(min_x, min_y, max_x, max_y)

            return self._cached_aabb

