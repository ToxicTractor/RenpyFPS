init python:
    import pygame

    class FpsDisplayable(renpy.Displayable):

        def __init__(self):
            super().__init__()

            self.old_st = None
            self.delta_time = 0

            self.background = Solid("#444")
            self.map = Map()


        def render(self, width, height, st, at):

            r = renpy.Render(width, height)

            ## update delta time
            self.update_delta_time(st)

            ## draw black gray background
            self.draw_background(r, width, height, st, at)

            self.map.draw_2d(r, width, height, st, at)

            ## redraw for the next frame and return the render
            renpy.redraw(self, 0)
            return r


        def events(self, ev, x, y, st): ## use this for reacting to events
            
            pass

        
        def draw_background(self, render, width, height, st, at):

            bg = renpy.render(self.background, width, height, st, at)
            
            render.blit(bg, (0, 0))


        ## calculates and sets delta time
        def update_delta_time(self, st):

            if (self.old_st is None):
                self.old_st = st
                self.delta_time = st

            self.delta_time = st - self.old_st

            self.old_st = st


        def calculate_framerate(self):
            if (self.delta_time <= 0):
                return 0
            else:
                return 1 // self.delta_time            


screen FpsScreen():

    modal True

    default fps = FpsDisplayable()

    add fps

    label f"Framerate: {fps.calculate_framerate()}"