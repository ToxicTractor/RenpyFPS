import renpy
from renpy.display.imagelike import Solid
from game.code.fps.classes.settings.FpsSettings_ren import FpsSettings

"""renpy
init python:
"""

class ScreenEffect():
    def __init__(self):
        self.at = 0
        self.duration = 0
        self.image = None


    def trigger(self, color, duration):

        self.at = 0
        self.duration = duration
        self.image = Solid(color)


    def trigger_heal(self):
        self.trigger("#0f05", 0.1)


    def trigger_armor_pickup(self):
        self.trigger("#00f5", 0.1)


    def trigger_hurt(self):
        self.trigger("#f005", 0.1)


    def update(self, delta_time):

        if (self.image is None):
            return

        if (self.at > self.duration):
            self.image = None
            return

        self.at += delta_time


    def draw(self, screen):

        if (self.image is None or self.at > self.duration):
            return

        render = renpy.render(self.image, FpsSettings.SCREEN_WIDTH, FpsSettings.SCREEN_HEIGHT, 0, 0)

        screen.blit(render, (0, 0))
