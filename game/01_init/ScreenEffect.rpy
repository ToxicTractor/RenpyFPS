init python:
    class ScreenEffect():
        def __init__(self):
            self.at = 0
            self.duration = 0
            self.image = None
        

        def trigger(self, color, duration):

            self.at = 0
            self.duration = duration
            self.image = Solid(color)            


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
            