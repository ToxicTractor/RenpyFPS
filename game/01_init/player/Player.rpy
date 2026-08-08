init python:
    class Player():
        MAX_WEAPONS = 10
        def __init__(self, game, pos=(0, 0), angle=0.0):
            self.game = game
            self.map = game.map
            self.pos_x, self.pos_y = pos
            self.angle = deg_to_rad(angle)
            self.speed = 5
            self.angular_speed = 2
            self.radius = .25
            self.interact_range = 5.0

            self.input_horizontal = 0
            self.input_vertical = 0
            self.input_angle = 0

            self.input_move_forward = InputKeyHandler(pygame.K_w, on_key=lambda: self._on_vertical_move_input(+1))
            self.input_move_backward = InputKeyHandler(pygame.K_s, on_key=lambda: self._on_vertical_move_input(-1))
            self.input_move_right = InputKeyHandler(pygame.K_d, on_key=lambda: self._on_horizontal_move_input(+1))
            self.input_move_left = InputKeyHandler(pygame.K_a, on_key=lambda: self._on_horizontal_move_input(-1))

            self.input_look_right = InputKeyHandler(pygame.K_RIGHT, on_key=lambda: self._on_angle_input(+1))
            self.input_look_left = InputKeyHandler(pygame.K_LEFT, on_key=lambda: self._on_angle_input(-1))

            self.input_use = InputKeyHandler(pygame.K_e, on_key_down=self._on_use_key_down)
            self.input_attack = InputKeyHandler(pygame.K_SPACE, on_key=self._on_attack_key)
            self.input_reload = InputKeyHandler(pygame.K_r, on_key_down=self._on_reload_key_down)

            self.input_weapon_1 = InputKeyHandler(pygame.K_1, on_key_down=lambda: self._on_change_weapon_key_down(1))
            self.input_weapon_2 = InputKeyHandler(pygame.K_2, on_key_down=lambda: self._on_change_weapon_key_down(2))
            self.input_weapon_3 = InputKeyHandler(pygame.K_3, on_key_down=lambda: self._on_change_weapon_key_down(3))
            self.input_weapon_4 = InputKeyHandler(pygame.K_4, on_key_down=lambda: self._on_change_weapon_key_down(4))
            self.input_weapon_5 = InputKeyHandler(pygame.K_5, on_key_down=lambda: self._on_change_weapon_key_down(5))
            self.input_weapon_6 = InputKeyHandler(pygame.K_6, on_key_down=lambda: self._on_change_weapon_key_down(6))
            self.input_weapon_7 = InputKeyHandler(pygame.K_7, on_key_down=lambda: self._on_change_weapon_key_down(7))
            self.input_weapon_8 = InputKeyHandler(pygame.K_8, on_key_down=lambda: self._on_change_weapon_key_down(8))
            self.input_weapon_9 = InputKeyHandler(pygame.K_9, on_key_down=lambda: self._on_change_weapon_key_down(9))
            self.input_weapon_0 = InputKeyHandler(pygame.K_0, on_key_down=lambda: self._on_change_weapon_key_down(0))

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
                FistsWeapon(self),
                ShotgunWeapon(self),
                ]
            self.equipped_weapon_index = 0
            self._cached_center_cell_trace = None

            self.ammo = {
                "shotgun": AmmoCount(),
            }

            self.inventory = Inventory()

            self.is_alive = True

            self.health = 100
            self.max_health = 100
            self.armor = 0
            self.max_armor = 100

            self.hurt_event = GameEvent()
            self.heal_event = GameEvent()
            self.gain_armor_event = GameEvent()
            self.attack_event = GameEvent()
            self.death_event = GameEvent()

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
        def coord(self):
            """
            A tuple representing the players current map coord.
            """
            return int(self.pos_x), int(self.pos_y)

        @property
        def coord_x(self):
            return int(self.pos_x)

        @property
        def coord_y(self):
            return int(self.pos_y)
        
        @property
        def center_cell_trace(self):
            if (self._cached_center_cell_trace):
                return self._cached_center_cell_trace
            
            self._cached_center_cell_trace = self.game.raycaster.trace_cells(self.pos, angle=self.angle)
            return self._cached_center_cell_trace

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

            canvas.circle("#0f0", (self.pos_x * self.game.scale, self.pos_y * self.game.scale), self.radius * self.game.scale)


        def handle_input(self, key_pressed):
            """
            Handles player input such as move, look and shoot.
            """
            ## first reset input variables
            self.input_horizontal = 0
            self.input_vertical = 0
            self.input_angle = 0

            ## then process inputs
            self.input_move_forward.handle_input(key_pressed)
            self.input_move_backward.handle_input(key_pressed)
            self.input_move_right.handle_input(key_pressed)
            self.input_move_left.handle_input(key_pressed)

            self.input_look_right.handle_input(key_pressed)
            self.input_look_left.handle_input(key_pressed)

            self.input_use.handle_input(key_pressed)
            self.input_attack.handle_input(key_pressed)
            self.input_reload.handle_input(key_pressed)

            self.input_weapon_1.handle_input(key_pressed)
            self.input_weapon_2.handle_input(key_pressed)
            self.input_weapon_3.handle_input(key_pressed)
            self.input_weapon_4.handle_input(key_pressed)
            self.input_weapon_5.handle_input(key_pressed)
            self.input_weapon_6.handle_input(key_pressed)
            self.input_weapon_7.handle_input(key_pressed)
            self.input_weapon_8.handle_input(key_pressed)
            self.input_weapon_9.handle_input(key_pressed)
            self.input_weapon_0.handle_input(key_pressed)


        def update(self, delta_time, st):
            
            self._move(delta_time)

            self._calculate_sway_offset(st)
            self._footsteps(st)

            for weapon in self.weapons:
                weapon.update_attack_timer(delta_time)

            if (self.equipped_weapon):
                self.equipped_weapon.update(delta_time)

            if (self.sway_enabled):

                if (abs(self.input_horizontal) > 0 or abs(self.input_vertical) > 0):
                    self.sway_moved_for_duration = clamp(self.sway_moved_for_duration + delta_time, 0, self.sway_change_duration)
                else:
                    self.sway_moved_for_duration = clamp(self.sway_moved_for_duration - delta_time, 0, self.sway_change_duration)

                self.sway_amount = inverse_lerp(0, self.sway_change_duration, self.sway_moved_for_duration)
            
            ## clear cached cell trace to force a new one next time we use it
            self._cached_center_cell_trace = None


        def apply_damage(self, amount, ignore_no_damage=True):
            
            ## do nothing if we are dead
            if (not self.is_alive):
                return

            ## if nothing is added, just return
            if (ignore_no_damage and amount <= 0):
                return
            
            ## keep track of damage individually
            health_damage = 0
            armor_damage = 0

            ## if we have more armor than the damage that was dealth, we deal only armor damage
            if (self.armor >= amount):
                health_damage = 0
                armor_damage = amount
            ## if we deal more damage than we have armor, we deal all our armor damage and the rest as health damage
            else:
                armor_damage = self.armor
                health_damage = amount - self.armor
            
            ## apply armor damage if any
            if (armor_damage > 0):
                self.armor -= armor_damage
            ## apply health damage if any
            if (health_damage > 0):
                self.health = max(self.health - health_damage, 0)
            
            ## if health is 0 or lower and we have not yet died, invoke death event
            if (self.health <= 0 and self.is_alive):
                self.is_alive = False
                self.death_event.invoke()
            ## if health is greater than 0, invoke hurt event
            else:
                self.hurt_event.invoke()


        def apply_heal(self, amount):

            ## do nothing if we are dead
            if (not self.is_alive):
                return

            ## if nothing is added, just return
            if (amount <= 0):
                return

            self.health = min(self.health + amount, self.max_health)

            self.heal_event.invoke()


        def apply_armor(self, amount):
            
            ## do nothing if we are dead
            if (not self.is_alive):
                return

            ## if nothing is added, just return
            if (amount <= 0):
                return

            self.armor = min(self.armor + amount, self.max_armor)

            self.gain_armor_event.invoke()


        def has_weapon(self, weapon_name):
            return any(weapon.name == weapon_name for weapon in self.weapons)

        def add_weapon(self, weapon, ammo=0, equip=True):
            weapon_count = len(self.weapons)

            ## ignore the weapon if we already have the max number of weapons
            if (len(self.weapons) >= Player.MAX_WEAPONS):
                return

            self.weapons.append(weapon)

            if (equip):
                self.equipped_weapon.unequip()
                self.equipped_weapon_index = weapon_count
                self.equipped_weapon.equip()
            
            self.add_ammo(weapon.ammo_type, ammo)
        
        def get_ammo_count(self, ammo_type):
            if (not self.has_ammo_type(ammo_type)):
                return 0
            return self.ammo[ammo_type.name].current

        def has_ammo_type(self, ammo_type):
            return ammo_type.name in self.ammo

        def is_ammo_full(self, ammo_type):
            return self.ammo[ammo_type.name].full()

        def add_ammo(self, ammo_type, amount):
            if (ammo_type.name not in self.ammo):
                self.ammo[ammo_type.name] = AmmoCount(amount, ammo_type.max)
            else:
                self.ammo[ammo_type.name].add(amount)

        def remove_ammo(self, ammo_type, amount=1):
            self.ammo[ammo_type.name].remove(amount)

        

#endregion


#region Event handlers

        def _on_change_weapon_key_down(self, weapon_key):
            
            if weapon_key == 0:
                weapon_key = 10
            
            index = weapon_key - 1

            ## only change weapon if the index is lower than the number of weapons
            if (len(self.weapons) > index):

                if (self.equipped_weapon_index == index):
                    return

                # if (not self.equipped_weapon.is_ready()):
                #     return
                self.equipped_weapon.unequip()
                self.equipped_weapon_index = index
                self.equipped_weapon.equip()


        def _on_use_key_down(self):
            
            cells, first_hit_distance = self.center_cell_trace

            if (first_hit_distance > self.interact_range):
                return

            ## for each cell, starting with the closest, we check if we can interact
            for trace in cells:

                ## if interaction is possible we trigger interact and then return to avoid triggering anything behind the first thing
                if (trace.cell.is_interactable(trace.cell_side)):
                    trace.cell.interact(self.game)
                    return


        def _on_attack_key(self):
            
            if (self.equipped_weapon and
                self.equipped_weapon.is_ready()):

                self.equipped_weapon.attack()

                if (self.equipped_weapon.has_ammo_in_magazine()):
                    self.attack_event.invoke()
                else:
                    return

                pen_count = 0
                weapon_pen = self.equipped_weapon.penetration
                weapon_range = self.equipped_weapon.range
                weapon_hit_sfx_played = False

                cells, block_distance = self.center_cell_trace

                for cell, depth, _ in cells:
                    
                    ## if we hit a cell that is not empty or an open door, we stop
                    if (cell.type != ECellType.Empty and 
                        not (cell.type == ECellType.HorizontalDoor and cell.open_amount >= 1.0)):
                        block_distance = depth ## we overwrite this since the first hit could have been an open door
                        break

                dx = math.cos(self.angle)
                dy = math.sin(self.angle)

                ## see if any npcs are in the traversed cell
                for npc in self.game.npcs:
                    
                    ## if npc is already dead, continue to next npc
                    if (not npc.is_alive):
                        continue

                    vx = npc.pos_x - self.pos_x
                    vy = npc.pos_y - self.pos_y

                    t = vx * dx + vy * dy

                    ## if behind us, we continue
                    if t < 0:
                        continue

                    ## the shot was blocked by a wall or a closed door
                    if t > block_distance:
                        continue

                    if weapon_range and t > weapon_range:
                        continue

                    closest_x = self.pos_x + dx * t
                    closest_y = self.pos_y + dy * t

                    dist_sq = (npc.pos_x - closest_x)**2 + (npc.pos_y - closest_y)**2

                    if (dist_sq <= npc.hit_size**2):

                        ## damage the npc
                        npc.modify_health(-self.equipped_weapon.damage)

                        if (not weapon_hit_sfx_played):
                            self.equipped_weapon.trigger_on_hit_sound_effect()
                            weapon_hit_sfx_played = True

                        ## if our weapon has no pen, return after the first enemy was hit
                        if (weapon_pen <= 0):
                            return
                        
                        ## if our weapon has pen, count up one pen and continue to the next npc
                        if (pen_count < weapon_pen):
                            pen_count += 1
                        else:
                            return

        
        def _on_reload_key_down(self):
            weapon = self.equipped_weapon
            ammo_type = weapon.ammo_type

            ## if our current weapon cannot reload, just return
            if (not weapon.can_be_reloaded()):
                return

            if (self.get_ammo_count(ammo_type) > 0):
                ## trigger reload
                weapon.start_reload()
            else:
                self.game.notification.show("No more ammo!", notification_type=ENotificationType.WeaponAction)


        def _on_horizontal_move_input(self, value):
            self.input_horizontal += value


        def _on_vertical_move_input(self, value):
            self.input_vertical += value


        def _on_angle_input(self, value):
            self.input_angle += value

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
            
            ## move the player
            self.pos_x = new_x
            self.pos_y = new_y

            ## correct the players position by doing a collision pass
            self.pos_x, self.pos_y = CollisionSystem.collision_pass(self.game, self)

            delta_angle = self.input_angle * self.angular_speed * delta_time

            self.angle += delta_angle
            self.angle %= math.tau


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
