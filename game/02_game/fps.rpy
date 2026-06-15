init python:
    import pygame
    
    class FpsDisplayable(renpy.Displayable):

        def __init__(self, scale=1):
            super().__init__()
            
            self.old_st = None
            self.delta_time = 0
            self.framerate = 0
            self.scale = scale

            self.background = Solid("#444")
            self.map = Map(self)
            self.player = Player(self, (15, 7))
            self.object_renderer = ObjectRenderer(self)
            self.raycaster = Raycaster(self)

            self.test = FpsSettings.HALF_SCREEN_HEIGHT

            self.modify_renpy_keymaps()

        @staticmethod
        def modify_renpy_keymaps():
            
            config.keymap["screenshot"] = []
            config.keymap["director"] = []

            renpy.clear_keymap_cache()

        @staticmethod
        def restore_keymaps():
            config.keymap["screenshot"] = ['alt_K_s', 'alt_shift_K_s', 'noshift_K_s']
            config.keymap["director"] = ['noshift_K_d']

            renpy.clear_keymap_cache()

        def render(self, width, height, st, at):

            ## update loop for our game
            self.update(st)

            r = renpy.Render(width, height)
            canvas = r.canvas()
            
            self.object_renderer.draw(r)
            # self.map.draw_2d(canvas)
            # self.player.draw_2d(canvas)

            ## redraw for the next frame and return the render
            renpy.redraw(self, 0)
            return r
        

        def update(self, st):
            
            ## update delta time
            self.update_delta_time(st)

            self.player.update(self.delta_time)

            self.raycaster.update()


        def event(self, ev, x, y, st): ## use this for reacting to events
            
            self.player.reset_input()

            if (pygame.key.get_pressed()[pygame.K_w]):
                self.player.input_vertical += 1
            if (pygame.key.get_pressed()[pygame.K_s]):
                self.player.input_vertical -= 1    
            if (pygame.key.get_pressed()[pygame.K_a]):
                self.player.input_horizontal -= 1
            if (pygame.key.get_pressed()[pygame.K_d]):
                self.player.input_horizontal += 1
            
            if (pygame.key.get_pressed()[pygame.K_LEFT]):
                self.player.input_angle -= 1
            if (pygame.key.get_pressed()[pygame.K_RIGHT]):
                self.player.input_angle += 1

            renpy.restart_interaction() ## make the interaction restart so text outside of the displayable can be updated

        
        def draw_background(self, render, width, height, st, at):

            bg = renpy.render(self.background, width, height, st, at)
            
            render.blit(bg, (0, 0))


        ## calculates and sets delta time
        def update_delta_time(self, st):

            if (self.old_st is None):
                self.delta_time = st
                self.old_st = st
            else:
                self.delta_time = st - self.old_st
                self.old_st = st

            self.framerate = self.calculate_framerate()


        def calculate_framerate(self):
            if (self.delta_time <= 0):
                return 0
            else:
                return 1.0 // self.delta_time            


screen FpsScreen():

    modal True

    default fps = FpsDisplayable(30)

    add fps

    label f"Framerate: {fps.framerate}"
