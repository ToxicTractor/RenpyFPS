init python:
    import math
    class Player():
        def __init__(self, game, pos=(0, 0), angle=0.0):
            self.game = game
            self.map = game.map
            self.pos_x, self.pos_y = pos
            self.angle = angle * 0.0174532925 # convert angle to radians
            self.speed = 5
            self.angular_speed = 2
            self.size = .33
            self.interact_range = 0.8

            self.raycaster = Raycaster(self, self.map)

            self.input_horizontal = 0
            self.input_vertical = 0
            self.input_angle = 0
            self.input_use = InputKeyHandler(pygame.K_e, on_key_down=self._on_use_down)

            self.sway_offset = (0, 0)
            self.sway_enabled = True
            self.sway_moved_for_duration = 0
            self.sway_change_duration = 0.125
            self.sway_amount = 0
            self.sway_magnitude_x = 5
            self.sway_magnitude_y = 5
            self.sway_phase_x = 0.6
            self.sway_phase_y = 0.3

            self.footstep_last_st = 0
            self.footstep_sounds = [
                "audio/fps/footsteps/footstep_01.ogg",
                "audio/fps/footsteps/footstep_02.ogg",
                "audio/fps/footsteps/footstep_03.ogg",
                "audio/fps/footsteps/footstep_04.ogg",
                "audio/fps/footsteps/footstep_05.ogg"
            ]

            self.weapons = [
                ShotgunWeapon(self)
                ]
            self.equipped_weapon_index = 0
            self.is_attacking = False

            self.health = 100
            self.max_health = 100

            self.hurt_event = GameEvent()
            self.heal_event = GameEvent()
            self.attack_event = GameEvent()

#region Properties

        @property
        def equipped_weapon(self):
            """
            Returns a references to the currently equipped weapon. Can be None if the player has no weapons.
            """
            weapon_count = len(self.weapons)
            
            if (weapon_count == 0):
                return None
            
            return self.weapons[self.equipped_weapon_index]

        @property
        def pos(self):
            """
            A tuple representing the players current position.
            """
            return self.pos_x, self.pos_y

        @property
        def coordinate(self):
            """
            A tuple representing the players current map coordinate.
            """
            return int(self.pos_x), int(self.pos_y)

#endregion

#region Public methods

        def draw(self, screen, st):
            """
            Draw the game to the screen.
            """

            if (self.equipped_weapon is None):
                return

            self.equipped_weapon.draw(screen, st)


        def draw_2d(self, canvas):
            """
            Draws a 2d representation of the player to the screen. Intended for debugging only.
            """
            canvas.line("#ff0", (self.pos_x * self.game.scale, self.pos_y * self.game.scale), 
                (self.pos_x * self.game.scale + config.screen_width * math.cos(self.angle) , self.pos_y  * self.game.scale + config.screen_width * math.sin(self.angle)), 2)

            canvas.circle("#0f0", (self.pos_x * self.game.scale, self.pos_y * self.game.scale), self.size * self.game.scale)


        def handle_input(self, key_pressed):
            """
            Handles player input such as move, look and shoot.
            """
            ## first reset input variables
            self.input_horizontal = 0
            self.input_vertical = 0
            self.input_angle = 0
            self.is_attacking = False

            ## find horizontal and vertical movement axis values
            if (key_pressed[pygame.K_w]):
                self.input_vertical += 1
            if (key_pressed[pygame.K_s]):
                self.input_vertical -= 1    
            if (key_pressed[pygame.K_a]):
                self.input_horizontal -= 1
            if (key_pressed[pygame.K_d]):
                self.input_horizontal += 1
            
            ## find angle input axis values
            if (key_pressed[pygame.K_LEFT]):
                self.input_angle -= 1
            if (key_pressed[pygame.K_RIGHT]):
                self.input_angle += 1

            ## register use key pressed
            self.input_use.handle_input(key_pressed)

            ## trigger an attack with the currently equipped weapon if we have one
            if (key_pressed[pygame.K_SPACE]):
                if (self.equipped_weapon is not None):
                    self.equipped_weapon.attack()


        def update(self, delta_time, st):

            self._move(delta_time)

            self._calculate_sway_offset(st)
            self._footsteps(st)

            if (self.equipped_weapon is not None):
                self.equipped_weapon.update(delta_time)

            if (self.sway_enabled):

                if (abs(self.input_horizontal) > 0 or abs(self.input_vertical) > 0):
                    self.sway_moved_for_duration = clamp(self.sway_moved_for_duration + delta_time, 0, self.sway_change_duration)
                else:
                    self.sway_moved_for_duration = clamp(self.sway_moved_for_duration - delta_time, 0, self.sway_change_duration)

                self.sway_amount = inverse_lerp(0, self.sway_change_duration, self.sway_moved_for_duration)

            self.raycaster.update()

        
        def modify_health(self, amount):

            self.health = clamp(self.health + amount, 0 , self.max_health)

            if (amount > 0): ## values above 0 is healing            
                self.heal_event.invoke()
            else:
                self.hurt_event.invoke()


#endregion


#region Event handlers

        def _on_use_down(self):
            
            cell, cell_side = self.raycaster.center_raycast(self.interact_range)

            if (cell is None):
                return

            if (cell.is_interactable(cell_side)):

                cell.interact()

#endregion


#region Private methods

        def _move(self, delta_time):
            """
            Moves the player according to the current input and checks for collisions along the way.
            """
            ## if delta time is 0, return to avoid dividing by 0
            if delta_time == 0:
                return

            cos_angle = math.cos(self.angle)
            sin_angle = math.sin(self.angle)
            speed = self.speed * delta_time

            speed_cos = speed * cos_angle
            speed_sin = speed * sin_angle

            ## normalize input magnitude to make sure we don't move faster when running diagonally
            vertical, horizontal = normalize(self.input_vertical, self.input_horizontal)

            delta_x = vertical * speed_cos + horizontal * -speed_sin
            delta_y = vertical * speed_sin + horizontal * speed_cos

            new_x = self.pos_x + delta_x
            new_y = self.pos_y + delta_y

            if (not self._collision(new_x, self.pos_y)):
                self.pos_x = new_x
            if (not self._collision(self.pos_x, new_y)):
                self.pos_y = new_y

            delta_angle = self.input_angle * self.angular_speed * delta_time

            self.angle += delta_angle
            self.angle %= math.tau


        def _collision(self, x, y):
            """
            Checks whether or not a given position is blocked.
            """
            return (
                self.map.is_blocking(x + self.size, y + self.size, self.size) or
                self.map.is_blocking(x - self.size, y + self.size, self.size) or
                self.map.is_blocking(x + self.size, y - self.size, self.size) or
                self.map.is_blocking(x - self.size, y - self.size, self.size)
            )


        def _calculate_sway_offset(self, st):
            """
            Calculates the offset caused by movement sway.
            """
            if (self.sway_amount == 0 or not self.sway_enabled):
                return (0, 0)
            
            x = math.sin((st * math.pi * 2) / self.sway_phase_x) * self.sway_magnitude_x * self.sway_amount
            y = math.sin((st * math.pi * 2) / self.sway_phase_y) * self.sway_magnitude_y * self.sway_amount

            self.sway_offset = (x, y)


        def _footsteps(self, st):
            """
            Plays a randomized footstep sound in sync with the sway.
            """
            if (self.sway_moved_for_duration <= 0):
                return

            if (self.footstep_last_st + self.sway_phase_y <= st):
                self.footstep_last_st = st

                renpy.play(self.footstep_sounds[renpy.random.randint(0, len(self.footstep_sounds) - 1)])
            
#endregion
