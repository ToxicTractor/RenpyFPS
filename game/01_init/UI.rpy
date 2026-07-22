init python:

    class FpsUI():
        def __init__(self):
            self.ingame_base_ui = Image("images/fps/ui/UI.png")


        def draw(self, screen, st, at):

            ui_render = renpy.render(self.ingame_base_ui, config.screen_width, config.screen_height, st, at)

            screen.blit(ui_render, (0, 0))