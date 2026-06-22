init python:
    import math

    class Player():

        def __init__(self, game, pos=(0, 0), angle=0.0):
            self.game = game
            self.pos_x, self.pos_y = pos
            self.angle = angle
            self.speed = 5
            self.angular_speed = 2
            self.size = .33
            self.input_horizontal = 0
            self.input_vertical = 0
            self.input_angle = 0

            self.sway_enabled = True
            self.sway_moved_for_duration = 0
            self.sway_change_duration = 0.125
            self.sway_amount = 0
            self.sway_magnitude_x = 5
            self.sway_magnitude_y = 5
            self.sway_phase_x = 0.6
            self.sway_phase_y = 0.3

            self.footstep_played = False
            self.footstep_last_st = 0
            self.footstep_sounds = [
                "audio/fps/footsteps/footstep_01.ogg",
                "audio/fps/footsteps/footstep_02.ogg",
                "audio/fps/footsteps/footstep_03.ogg",
                "audio/fps/footsteps/footstep_04.ogg",
                "audio/fps/footsteps/footstep_05.ogg"
            ]

        def reset_input(self):
            self.input_horizontal = 0
            self.input_vertical = 0
            self.input_angle = 0


        def move(self, delta_time):

            ## if delta time is 0, return to avoid dividing by 0
            if delta_time == 0:
                return

            sin_angle = math.sin(self.angle)
            cos_angle = math.cos(self.angle)
            delta_x = 0
            delta_y = 0
            speed = self.speed * delta_time
            speed_sin = speed * sin_angle
            speed_cos = speed * cos_angle

            delta_x = self.input_vertical * speed_cos + self.input_horizontal * -speed_sin
            delta_y = self.input_vertical * speed_sin + self.input_horizontal * speed_cos

            new_x = self.pos_x + delta_x
            new_y = self.pos_y + delta_y

            if (not self.wall_collision(new_x, self.pos_y)):
                self.pos_x = new_x
            if (not self.wall_collision(self.pos_x, new_y)):
                self.pos_y = new_y

            delta_angle = self.input_angle * self.angular_speed * delta_time

            self.angle += delta_angle
            self.angle %= math.tau


        def update(self, delta_time, st):
            self.move(delta_time)

            self.footsteps(st)

            if (not self.sway_enabled):
                return

            if (abs(self.input_horizontal) > 0 or abs(self.input_vertical) > 0):
                self.sway_moved_for_duration = clamp(self.sway_moved_for_duration + delta_time, 0, self.sway_change_duration)
            else:
                self.sway_moved_for_duration = clamp(self.sway_moved_for_duration - delta_time, 0, self.sway_change_duration)

            self.sway_amount = inverse_lerp(0, self.sway_change_duration, self.sway_moved_for_duration)

        def is_wall(self, x, y):
            return (int(x), int(y)) in self.game.map.world_map

        def wall_collision(self, x, y):
            
            return (
                self.is_wall(x + self.size, y + self.size) or
                self.is_wall(x - self.size, y + self.size) or
                self.is_wall(x + self.size, y - self.size) or
                self.is_wall(x - self.size, y - self.size)
            )


        def calculate_sway_offset(self, st):
            
            if (self.sway_amount == 0):
                return (0, 0)
            
            x = math.sin((st * math.pi * 2) / self.sway_phase_x) * self.sway_magnitude_x * self.sway_amount
            y = math.sin((st * math.pi * 2) / self.sway_phase_y) * self.sway_magnitude_y * self.sway_amount

            return (x, y)

        
        def footsteps(self, st):
            
            if (self.sway_moved_for_duration <= 0):
                return

            if (self.footstep_last_st + self.sway_phase_y <= st):
                self.footstep_last_st = st

                renpy.play(self.footstep_sounds[renpy.random.randint(0, len(self.footstep_sounds) - 1)])
            

        def draw_2d(self, canvas):

            canvas.line("#ff0", (self.pos_x * self.game.scale, self.pos_y * self.game.scale), 
                (self.pos_x * self.game.scale + config.screen_width * math.cos(self.angle) , self.pos_y  * self.game.scale + config.screen_width * math.sin(self.angle)), 2)

            canvas.circle("#0f0", (self.pos_x * self.game.scale, self.pos_y * self.game.scale), self.size * self.game.scale)


        @property
        def pos(self):
            return self.pos_x, self.pos_y

        @property
        def coordinate(self):
            return int(self.pos_x), int(self.pos_y)