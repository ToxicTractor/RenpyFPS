init python:
    from copy import deepcopy
    class Casing():

        def __init__(self, animation, start_position, lifetime=None, scale=1.0):

            self.animation = animation
            self.start_x, self.start_y = start_position
            self.pos_x, self.pos_y = start_position
            self.scale = scale
            self.lifetime = self.animation.duration if lifetime is None else lifetime
            self.at = 0

            self.width, self.height = get_image_size(self.animation.image)


        def is_expired(self):
            print(f"AT: {self.at} | Lifetime: {self.lifetime}")
            return self.at >= self.lifetime


        def draw(self, screen, st):

            scaled_width = int(self.width * self.scale)
            scaled_height = int(self.height * self.scale)

            displayable = Transform(self.animation.image, size=(scaled_width, scaled_height))

            render = renpy.render(displayable, FpsSettings.SCREEN_WIDTH, FpsSettings.SCREEN_HEIGHT, st, min(self.animation.duration - 0.0001, self.at))

            screen.blit(render, (self.pos_x, self.pos_y))


        def update(self, delta_time):

            if (self.at < self.lifetime):
                self.at += delta_time

            self.pos_x, self.pos_y = self.calculate_current_position()


        def reset(self):

            self.pos_x = self.start_x
            self.pos_y = self.start_y
            self.at = 0


        def calculate_current_position(self):
            if (self.animation.duration == 0):
                return self.start_x, self.start_y
            
            x = int((3000*self.at) + self.start_x)
            y = int((110 * (self.at - 0.06)) ** 2 + self.start_y)

            return x, y
