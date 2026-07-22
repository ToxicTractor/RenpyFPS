init python:
    import random
    
    class FpsUI():
        def __init__(self, game):
            self.game = game
            self.ingame_base_ui = Image("images/fps/ui/UI.png")

            self.face = PlayerFace(game.player)

        def draw(self, screen, st, at):

            ui_render = renpy.render(self.ingame_base_ui, config.screen_width, config.screen_height, st, at)
            screen.blit(ui_render, (0, 807))

            self.face.draw(screen)

        def update(self, delta_time):

            self.face.update(delta_time)

