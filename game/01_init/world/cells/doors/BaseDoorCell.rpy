init -2 python:
    class BaseDoorCell(CellBase, ABC):
        def __init__(self, 
            coord:                      tuple, 
            main_texture:               Image, 
            side_texture:               Image, 
            grid_alignment:             EGridAlignment, 
            open_direction:             EDirection, 
            open_audio:                 str=None, 
            close_audio:                str=None, 
            locked_interact_audio:      str=None, 
            offset:                     float=0.0,
            thickness:                  float=1.0,
            speed:                      float=2.5,
            side_texture_aspect_ratio:  float=1.0,
            start_open:                 bool=False,
            flip_main_texture:          bool=False, 
            is_locked:                  bool=False, 
            can_be_closed:              bool=True):
            super().__init__(coord)

            self.coord = coord
            self.main_texture = main_texture
            self.side_texture = side_texture
            self.grid_alignment = grid_alignment
            self.open_direction = open_direction
            self.open_audio = open_audio
            self.close_audio = close_audio
            self.locked_interact_audio = locked_interact_audio
            self.offset = offset
            self.thickness = thickness
            self.flip_main_texture = flip_main_texture
            self.is_locked = is_locked
            self.can_be_closed = can_be_closed
            self.side_texture_aspect_ratio = side_texture_aspect_ratio
            self.speed = speed
            self.open_amount = 1.0 if start_open else 0.0
            self.is_open_state = start_open
            
        @property
        def is_npc_walkable(self):
            return self.open_amount >= 1.0


        def get_texture(self, side):
            if self.grid_alignment == EGridAlignment.X:
                if side in FpsConstants.VERTICAL_DIRECTIONS:
                    return self.main_texture, 1.0
                else:
                    return self.side_texture, self.side_texture_aspect_ratio

            elif self.grid_alignment == EGridAlignment.Y:
                if side in FpsConstants.HORIZONTAL_DIRECTIONS:
                    return self.main_texture, 1.0
                else:
                    return self.side_texture, self.side_texture_aspect_ratio

            return None, 1.0


        def is_interactable(self, side):

            if (self.is_locked):
                return False

            if (not self.can_be_closed and self.open_amount == 1.0):
                return False

            ## door is only interactable when it is fully open or closed
            return ((self.open_amount == 1.0 and self.is_open_state) or
                    (self.open_amount == 0.0 and not self.is_open_state))


        def interact(self):

            if (self.is_open_state):
                self.close_door()
            else:
                self.open_door()

        
        def open_door(self):

            if (self.is_open_state):
                return

            if (self.open_audio):
                renpy.play(self.open_audio)

            self.is_open_state = True


        def close_door(self):

            if (not self.is_open_state):
                return

            if (self.close_audio):
                renpy.play(self.close_audio)

            self.is_open_state = False

        
        def _calculate_depth(self, player_x, player_y, ray_dx, ray_dy, aabb):

            if ray_dx != 0:
                tx1 = (aabb.min_x - player_x) / ray_dx
                tx2 = (aabb.max_x - player_x) / ray_dx

                tmin = min(tx1, tx2)
                tmax = max(tx1, tx2)
            else:
                if player_x < aabb.min_x or player_x > aabb.max_x:
                    return None, None

                tmin = -float("inf")
                tmax = float("inf")

            if ray_dy != 0:
                ty1 = (aabb.min_y - player_y) / ray_dy
                ty2 = (aabb.max_y - player_y) / ray_dy

                tmin = max(tmin, min(ty1, ty2))
                tmax = min(tmax, max(ty1, ty2))
            else:
                if player_y < aabb.min_y or player_y > aabb.max_y:
                    return None, None

            if tmax < tmin:
                return None, None

            if tmax < 0:
                return None, None

            return tmin, tmax