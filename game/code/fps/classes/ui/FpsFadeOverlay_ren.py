from game.code.fps.classes.settings.FpsSettings_ren import FpsSettings
from game.code.fps.other.helper_functions_ren import inverse_lerp, lerp

"""renpy
init -1 python:
"""

class FpsFadeOverlay(renpy.Displayable):
    def __init__(self):
        super().__init__()

        self.current_alpha = 1.0
        self.initial_alpha = 1.0
        self.target_alpha = 1.0
        self.current_time = 0
        self.duration = 0
        self.complete_action = None
        self.complete_action_args = ()

        self.old_st = 0
        self.black = Solid("#000")


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
            if (self.complete_action):
                if (len(self.complete_action_args) > 0):
                    self.complete_action(*self.complete_action_args)
                else:
                    self.complete_action()
                self.complete_action = None
                self.complete_action_args = ()
            return

        if (self.duration == 0 and self.current_alpha != self.target_alpha):
            self.current_alpha = self.target_alpha
            return

        if (self.current_time < self.duration):
            self.current_time += delta_time

        t = inverse_lerp(0, self.duration, self.current_time)
        self.current_alpha = lerp(self.initial_alpha, self.target_alpha, t)


    def fade_to_black(self, duration=FpsSettings.DEFAULT_FADE_DURATION, complete_action=None, *complete_action_args):
        self.initial_alpha = self.current_alpha
        self.target_alpha = 1.0
        self.current_time = 0
        self.duration = duration
        self.complete_action = complete_action
        self.complete_action_args = complete_action_args


    def fade_to_clear(self, duration=FpsSettings.DEFAULT_FADE_DURATION, complete_action=None, *complete_action_args):
        self.initial_alpha = self.current_alpha
        self.target_alpha = 0.0
        self.current_time = 0
        self.duration = duration
        self.complete_action = complete_action
        self.complete_action_args = complete_action_args


    ## function used for screen buttons to fade out, jump to a label and then fade in again
    def fade_out_jump_in(self, label_name):
        self.fade_to_black(FpsSettings.DEFAULT_FADE_DURATION, self._fade_jump_in, label_name)

    def _fade_jump_in(self, label_name):
        renpy.jump(label_name)
        self.fade_to_clear()
