init -1 python:
    from abc import ABC, abstractmethod
    class NPC(SpriteObject, ABC): ## abstract class to enforce inheritance for enemy types

        def __init__(self, game, pos, sprite_anim=None, scale=1.0, height_shift=0.0):
            super().__init__(game, sprite_anim, pos=pos, scale=scale, height_shift=height_shift)

            #region Override variables
            ## animations
            self.attack_anim = None
            self.idle_anim = None
            self.walk_anim = None
            self.hurt_anim = None
            self.death_anim = None

            ## audio
            self.attack_audio = None
            self.hurt_audio = None
            self.death_audio = None

            ## stats
            self.attack_range = 0
            self.speed = 0
            self.size = 0
            self.health = 0
            self.attack_damage = 0
            self.accuracy = 0
            #endregion

            self.alive = True
            self.hurt = False
            self.attack = False

            self.return_to_start_pos = True
            self.start_coord = self.coordinate

            self.pathfinding = Pathfinding(game.map.nav_map)
            self.path = None
            self.los_grace_period = 2.0
            self.los_grace_timer = 0

            self.has_los_to_player = False
            self.last_player_coord = None
            self.lost_player = False


        @property
        def coordinate(self):
            return int(self.pos_x), int(self.pos_y)


        def update(self, delta_time):
            super().update(delta_time)
            
            if self.alive:
                player_coord = self.game.player.coordinate
                player_coord_x, player_coord_y = player_coord
                self.has_los_to_player = self.is_player_in_sight()
                self.check_was_hit()

                if (self.hurt):
                    self.change_animation(self.hurt_anim, audio=self.hurt_audio)

                elif (self.attack):
                    self.change_animation(self.attack_anim, audio=self.attack_audio)

                elif (self.has_los_to_player):
                    
                    if (self.dist <= self.attack_range):
                        self.attack = True
                        return

                    self.move_towards((player_coord_x + 0.5, player_coord_y + 0.5), delta_time)

                    ## set variables
                    self.path = None
                    self.last_player_coord = player_coord
                    self.lost_player = False
                    self.los_grace_timer = 0

                elif (self.last_player_coord is not None):
                    self.pathfind_to_player(player_coord, delta_time)

                elif (self.return_to_start_pos and self.lost_player):
                    self.pathfind_to_start_pos(delta_time)

                else:
                    self.change_animation(self.idle_anim)

            else:
                self.change_animation(self.death_anim, audio=self.death_audio)


        def change_animation(self, animation, audio=None, override_same=False):

            if (self.sprite_anim == animation and not override_same):
                return
            
            if (audio is not None):
                renpy.play(audio)

            self.sprite_anim = animation
            self.at = 0


        def pathfind_to_start_pos(self, delta_time):

            if (self.path is None):
                self.path = self.pathfinding.find_path(self.coordinate, self.start_coord)
            
            ## if there is no path or we have arrived, return self.lost_player to False
            if (not self.pathfind_along_current_path(delta_time)):
                self.lost_player = False


        def pathfind_to_player(self, player_coord, delta_time):

            ## update the path if we dont have one or if the players position changed and we are still within the LOS grace period
            if (self.los_grace_timer < self.los_grace_period and (self.path is None or self.last_player_coord != player_coord)):
                self.path = self.pathfinding.find_path(self.coordinate, player_coord)
            
            self.last_player_coord = player_coord

            if (self.path is not None and len(self.path) > 1):

                next_tile = self.path[1]

                ## +0.5 to go to the center of the tile
                target_x = next_tile[0] + 0.5
                target_y = next_tile[1] + 0.5

                distance = math.hypot(target_x - self.pos_x, target_y - self.pos_y)

                ## pop the element to use the next step, next time
                if (distance < 0.1):
                    self.path.pop(0)

                self.move_towards((target_x, target_y), delta_time)

            else:

                ## reset variables
                self.path = None
                self.last_player_coord = None
                self.los_grace_timer = 0
                self.lost_player = True
                return

            self.los_grace_timer += delta_time
        

        def pathfind_along_current_path(self, delta_time):

            if (self.path is not None and len(self.path) > 1):

                next_tile = self.path[1]

                ## +0.5 to go to the center of the tile
                target_x = next_tile[0] + 0.5
                target_y = next_tile[1] + 0.5

                distance = math.hypot(target_x - self.pos_x, target_y - self.pos_y)

                ## pop the element to use the next step, next time
                if (distance < 0.1):
                    self.path.pop(0)

                self.move_towards((target_x, target_y), delta_time)
                
                return True
            
            return False


        def move_towards(self, target_coord, delta_time):
            
            self.change_animation(self.walk_anim)

            target_coord_x, target_coord_y = target_coord

            angle = math.atan2(target_coord_y - self.pos_y, target_coord_x - self.pos_x)
            speed = self.speed * delta_time
            
            speed_cos = speed * math.cos(angle)
            speed_sin = speed * math.sin(angle)

            delta_x = speed_cos
            delta_y = speed_sin

            new_x = self.pos_x + delta_x
            new_y = self.pos_y + delta_y

            if (not self.wall_collision(new_x, self.pos_y)):
                self.pos_x = new_x
            if (not self.wall_collision(self.pos_x, new_y)):
                self.pos_y = new_y


        def wall_collision(self, x, y):
            map = self.game.map
            return (
                map.is_wall(x + self.size, y + self.size) or
                map.is_wall(x - self.size, y + self.size) or
                map.is_wall(x + self.size, y - self.size) or
                map.is_wall(x - self.size, y - self.size)
            )


        def on_animation_end(self, animation):

            if (animation == self.hurt_anim):

                self.hurt = False
                self.sprite_anim = self.idle_anim
                self.at = 0

            elif (animation == self.attack_anim):

                self.attack = False
                self.sprite_anim = self.idle_anim
                self.at = 0


        def check_was_hit(self):

            if (self.has_los_to_player and self.game.player.is_attacking):
                
                ## we should probably also check weapon range here
                if (FpsSettings.HALF_SCREEN_WIDTH - self.sprite_half_width < self.screen_x < FpsSettings.HALF_SCREEN_WIDTH + self.sprite_half_width):

                    self.game.player.is_attacking = False ## if weapon is piercing we dont do this
                    self.hurt = True     
                    
                    self.take_damage(self.game.player.equipped_weapon.damage)            


        def take_damage(self, amount):
            self.health -= amount

            if (self.health <= 0 and self.alive):
                self.alive = False


        def is_player_in_sight(self):

            world_map = self.game.map.world_map

            ## if we are in the same cell as an enemy, return true
            if (self.game.player.coordinate == self.coordinate):
                return True

            ## get starting coord
            cell_x, cell_y = self.coordinate

            ## calculate sin and cos
            ray_direction_x = -math.cos(self.theta)
            ray_direction_y = -math.sin(self.theta)

            ## calculate delta distance
            delta_distance_x = float('inf') if ray_direction_x == 0 else abs(1 / ray_direction_x)
            delta_distance_y = float('inf') if ray_direction_y == 0 else abs(1 / ray_direction_y)

            ## determine step direction
            step_x = -1 if ray_direction_x < 0 else 1
            step_y = -1 if ray_direction_y < 0 else 1

            ## calculate initial side distances
            if (ray_direction_x < 0):
                side_distance_x = (self.pos_x - cell_x) * delta_distance_x
            else:
                side_distance_x = (cell_x + 1 - self.pos_x) * delta_distance_x

            if (ray_direction_y < 0):
                side_distance_y = (self.pos_y - cell_y) * delta_distance_y
            else:
                side_distance_y = (cell_y + 1 - self.pos_y) * delta_distance_y

            ## only loop for a max number of steps to avoid an infinite loop 
            for _ in range(FpsSettings.MAX_DEPTH):
                if (side_distance_x < side_distance_y):

                    side_distance_x += delta_distance_x
                    cell_x += step_x
                    side = 0
                
                else:

                    side_distance_y += delta_distance_y
                    cell_y += step_y
                    side = 1

                ## we reached the enemy, thus we have line of sight
                if (cell_x, cell_y) == self.game.player.coordinate:
                    return True

                ## we are blocked by a wall
                if (cell_x, cell_y) in world_map:
                    return False

            return False

        
        ## this method exists purely for 2d debugging
        def draw_2d(self, canvas):
            canvas.circle("#f00", (self.pos_x * self.game.scale, self.pos_y * self.game.scale), self.size * self.game.scale)

            if (not self.alive and not self.is_player_in_sight()):
                return

            canvas.line("#fa0", (self.game.player.pos_x * self.game.scale, self.game.player.pos_y * self.game.scale), 
                (self.pos_x * self.game.scale, self.pos_y * self.game.scale), 2)
