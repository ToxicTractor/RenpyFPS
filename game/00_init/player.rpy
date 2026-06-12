init python:
    import math

    class Player():

        def __init__(self, game, pos=(0, 0), angle=0.0):
            self.game = game
            self.pos_x, self.pos_y = pos
            self.angle = angle
            self.speed = 200
            self.angular_speed = 2

            self.input_horizontal = 0
            self.input_vertical = 0
            self.input_angle = 0

            self.image = Solid("#ff0", xsize=16, ysize=16)


        def reset_input(self):
            self.input_horizontal = 0
            self.input_vertical = 0
            self.input_angle = 0


        def move(self, delta_time):

            sin_angle = math.sin(self.angle)
            cos_angle = math.cos(self.angle)
            delta_x = 0
            delta_y = 0
            speed = self.speed * delta_time
            speed_sin = speed * sin_angle
            speed_cos = speed * cos_angle

            delta_x = self.input_vertical * speed_cos + self.input_horizontal * -speed_sin
            delta_y = self.input_vertical * speed_sin + self.input_horizontal * speed_cos

            if (not self.wall_collision_x(delta_x)):
                self.pos_x += delta_x
            if (not self.wall_collision_y(delta_y)):
                self.pos_y += delta_y

            delta_angle = self.input_angle * self.angular_speed * delta_time

            self.angle += delta_angle
            self.angle %= math.tau


        def update(self, delta_time):
            self.move(delta_time)

        def to_coord(self, x, y):
            return self.game.map.pos_to_coord(x, y)

        def is_wall(self, x, y):
            return self.to_coord(x, y) in self.game.map.world_map

        def wall_collision_x(self, delta_x):
            return self.is_wall(self.pos_x + delta_x, self.pos_y)

        def wall_collision_y(self, delta_y):
            return self.is_wall(self.pos_x, self.pos_y + delta_y)


        def draw_2d(self, canvas):

            canvas.line("#ff0", (self.pos_x, self.pos_y), (self.pos_x + config.screen_width * math.cos(self.angle), self.pos_y + config.screen_width * math.sin(self.angle)), 2)
            canvas.circle("#0f0", (self.pos_x, self.pos_y), 10)


        @property
        def pos(self):
            return self.pos_x, self.pos_y


        def coord(self):
            return int(self.pos_x), int(self.pos_y)