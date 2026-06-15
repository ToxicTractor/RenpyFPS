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


        def update(self, delta_time):
            self.move(delta_time)

        def is_wall(self, x, y):
            return (int(x), int(y)) in self.game.map.world_map

        def wall_collision(self, x, y):
            
            return (
                self.is_wall(x + self.size, y + self.size) or
                self.is_wall(x - self.size, y + self.size) or
                self.is_wall(x + self.size, y - self.size) or
                self.is_wall(x - self.size, y - self.size)
            )


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