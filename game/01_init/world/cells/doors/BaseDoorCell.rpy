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
            unlock_audio:               str=None, 
            locked_interact_audio:      str=None,
            offset:                     float=0.0,
            thickness:                  float=1.0,
            speed:                      float=2.5,
            side_texture_aspect_ratio:  float=1.0,
            start_open:                 bool=False,
            flip_main_texture:          bool=False, 
            allow_interaction:          bool=True,
            can_be_closed:              bool=True,
            is_locked:                  bool=False, 
            unlocked_by_item:           str=None,
            consumed_on_unlock_count:   int=0,
            locked_notification:        str=FpsConstants.LOCKED_DOOR_NOTIFICATION):
            super().__init__(coord)

            self.coord = coord
            self.main_texture = main_texture
            self.side_texture = side_texture
            self.grid_alignment = grid_alignment
            self.open_direction = open_direction
            self.open_audio = open_audio
            self.close_audio = close_audio
            self.unlock_audio = unlock_audio
            self.locked_interact_audio = locked_interact_audio
            self.offset = offset
            self.speed = speed
            self.thickness = thickness
            self.side_texture_aspect_ratio = side_texture_aspect_ratio
            self.is_open_state = start_open
            self.flip_main_texture = flip_main_texture
            self.allow_interaction = allow_interaction
            self.can_be_closed = can_be_closed
            self.is_locked = is_locked
            self.unlocked_by_item = unlocked_by_item
            self.consumed_on_unlock_count = consumed_on_unlock_count
            self.locked_notification = locked_notification
            
            self.open_amount = 1.0 if start_open else 0.0

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


        def is_interactable(self, side) -> bool:

            if (not self.allow_interaction):
                return False

            if (not self.can_be_closed and self.open_amount == 1.0):
                return False

            ## door is only interactable when it is fully open or closed
            return ((self.open_amount == 1.0 and self.is_open_state) or
                    (self.open_amount == 0.0 and not self.is_open_state))


        def interact(self, game):
            
            ## if we were unable to unlock the door, just return
            if (not self._try_unlock_door(game)):
                return

            self.toggle_door_state()


        def toggle_door_state(self):

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


        def _try_unlock_door(self, game) -> bool: ## returns true if the door is not locked or was unlocked

            ## if the door wasnt locked, we just return true
            if (not self.is_locked):
                return True

            ## if the door is not unlocked by an item, we cant open it so we show a generic notification
            if (self.unlocked_by_item is None):
                
                if (self.locked_interact_audio):
                    renpy.play(self.locked_interact_audio)

                game.notification.show(self.locked_notification, ENotificationType.Negative)
                return False
            
            ## ----------------------------
            ## door consumes item on unlock
            ## ----------------------------
            if (self.consumed_on_unlock_count > 0):

                ## if the player has enough of the required item we unlock the door and remove the items from the player inventory
                if (game.player.inventory.has_item(self.unlocked_by_item, self.consumed_on_unlock_count)):
                    self.is_locked = False
                    
                    if (self.unlock_audio):
                        renpy.play(self.unlock_audio)

                    game.player.inventory.remove_item(self.unlocked_by_item, self.consumed_on_unlock_count)
                    game.notification.show(f"{self.consumed_on_unlock_count} x {self.unlocked_by_item.name} was removed.")

                    return True
                
                ## if the player doesn't have enough of the required item we just show a notification
                if (self.locked_interact_audio):
                    renpy.play(self.locked_interact_audio)

                game.notification.show(f"Requires {self.consumed_on_unlock_count} x {self.unlocked_by_item.name}.", type=ENotificationType.Negative)
                return False
            
            ## -----------------------------------
            ## door doesn't consume item on unlock
            ## -----------------------------------
            
            ## if the player has the item we unlock the door
            if (game.player.inventory.has_item(self.unlocked_by_item)):
                self.is_locked = False
                
                if (self.unlock_audio):
                    renpy.play(self.unlock_audio)

                return True
            
            ## if the player doesn't have the item we show a notification
            if (self.locked_interact_audio):
                renpy.play(self.locked_interact_audio)

            game.notification.show(f"Requires {self.unlocked_by_item.name}.", type=ENotificationType.Negative)

            return False


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