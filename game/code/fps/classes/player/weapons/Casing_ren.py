import renpy
from renpy.display.transform import Transform
from game.code.fps.classes.settings.FpsSettings_ren import FpsSettings
from game.code.fps.other.helper_functions_ren import get_image_size
from game.code.fps.other.named_tuples_ren import Vector2

"""renpy
init python:
"""

class Casing():

    def __init__(self, animation, start_position, lifetime=None, scale=1.0):

        self.animation = animation
        self.start_pos = Vector2(*start_position)
        self.pos = Vector2(*start_position)
        self.scale = scale
        self.lifetime = self.animation.duration if lifetime is None else lifetime
        self.at = 0

        self.width, self.height = get_image_size(self.animation.image)

    @property
    def is_expired(self):
        return self.at >= self.lifetime


    def draw(self, screen, st):

        scaled_width = int(self.width * self.scale)
        scaled_height = int(self.height * self.scale)

        displayable = Transform(self.animation.image, size=(scaled_width, scaled_height))

        render = renpy.render(displayable, FpsSettings.SCREEN_WIDTH, FpsSettings.SCREEN_HEIGHT, st, min(self.animation.duration - 0.0001, self.at))

        screen.blit(render, (self.pos.x, self.pos.y))


    def update(self, delta_time):

        if (self.at < self.lifetime):
            self.at += delta_time

        self.pos = self.calculate_current_position()


    def reset(self):

        self.pos = self.start_pos
        self.at = 0


    def calculate_current_position(self):
        if (self.animation.duration == 0):
            return self.start_pos

        x = int((2000*self.at) + self.start_pos.x)

        a = 8000
        b = -1800
        c = 0

        y = int((a * self.at ** 2 + b * self.at + c) + self.start_pos.y)

        return Vector2(x, y)
