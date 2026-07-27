init python:
    class FpsUIOverlay(renpy.Displayable):
        def __init__(self, game):
            super().__init__()

            self.game = game
            self.old_st = 0

            self.base_ui_image = Image("images/fps/ui/UI.png")

            self.face = PlayerFace(game.player)


        def render(self, width, height, st, at):

            ## calculate delta_time and call update
            delta_time = st - self.old_st
            self.update(delta_time)
            self.old_st = st

            ## create screen
            screen = renpy.Render(width, height)

            self.draw(screen, st, at)

            ## schedule screen redraw
            renpy.redraw(self, 0)
            return screen
        

        def draw(self, screen, st, at):
            
            ## draw UI background
            ui_render = renpy.render(self.base_ui_image, config.screen_width, config.screen_height, st, at)
            screen.blit(ui_render, (0, 807))

            ## draw player face
            self.face.draw(screen)


        def update(self, delta_time):

            self.face.update(delta_time)