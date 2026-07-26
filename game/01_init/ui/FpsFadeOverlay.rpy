init python:
    class FpsFadeOverlay(renpy.Displayable):
        def __init__(self, game):
            super().__init__()

            self.game = game

            self.current_alpha = 1.0
            self.initial_alpha = 1.0
            self.target_alpha = 1.0
            self.current_time = 0
            self.duration = 0

            self.old_st = 0
            self.black = Solid("#000")

            game.fade_to_black_event.add_listener(self.on_fade_to_black)
            game.fade_to_clear_event.add_listener(self.on_fade_to_clear)

            ## trigger fade to clear at the beginning to fade at the very start of the game
            self.on_fade_to_clear(0.5)

        def render(self, width, height, st, at):
            r = renpy.Render(width, height)
            
            delta_time = st - self.old_st
            self.update(delta_time)
            self.old_st = st

            if (self.current_alpha != 0.0):
                fade_displayable = Transform(self.black, alpha=self.current_alpha)
                fade_render = renpy.render(fade_displayable, config.screen_width, config.screen_height, 0, 0)
                r.blit(fade_render, (0, 0))
            
            ## redraw for the next frame and return the render
            renpy.redraw(self, 0)
            return r
        

        def update(self, delta_time):

            if (self.current_alpha == self.target_alpha):
                return

            if (self.duration == 0 and self.current_alpha != self.target_alpha):
                self.current_alpha = self.target_alpha
                return

            if (self.current_time < self.duration):
                self.current_time += delta_time

            t = inverse_lerp(0, self.duration, self.current_time)
            self.current_alpha = lerp(self.initial_alpha, self.target_alpha, t)
            

        def on_fade_to_black(self, duration):
            self.initial_alpha = self.current_alpha
            self.target_alpha = 1.0
            self.current_time = 0
            self.duration = duration


        def on_fade_to_clear(self, duration):
            self.initial_alpha = self.current_alpha
            self.target_alpha = 0.0
            self.current_time = 0
            self.duration = duration
