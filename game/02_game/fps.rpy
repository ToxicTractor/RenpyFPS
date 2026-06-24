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
            self.jukebox = FpsJukebox()
            self.player = Player(self, self.map.player_start_pos)
            self.object_renderer = ObjectRenderer(self)
            self.raycaster = Raycaster(self)
            self.weapon = Weapon(
                self,
                "shotgun_idle", 
                "shotgun_shoot", 
                shoot_sound="audio/fps/weapons/shotgun_shoot.ogg",
                casing_pool=ObjectPool(
                    Casing(
                        shotgun_shell_anim, 
                        (FpsSettings.HALF_SCREEN_WIDTH - 40, FpsSettings.SCREEN_HEIGHT - 80), 
                        lifetime=0.3, 
                        scale=4.0
                    ), 
                    2
                ),
                casing_spawn_delay=0.3,
                scale=4.0
            )
            self.sprite_obj1 = SpriteObject(self, candlestick_anim, scale=0.7, height_shift=0.27)
            self.sprite_obj2 = SpriteObject(self, torch_anim, pos=(14.5, 15.5), height_shift=0.05)
            
            self.npcs = [
                ZombieNPC(self, pos=(13.5, 15.5)),
                ZombieNPC(self, pos=(9.5, 9.5))
            ]

            self.modify_renpy_keymaps()
            #self.jukebox.play()

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
            
            # self.map.draw_2d(canvas)
            # self.player.draw_2d(canvas)
            # for npc in self.npcs:
            #     npc.draw_2d(canvas)

            self.object_renderer.draw(r, st)
            self.weapon.draw(r, st)

            ## redraw for the next frame and return the render
            renpy.redraw(self, 0)
            return r
        

        def update(self, st):
            
            ## update delta time
            self.update_delta_time(st)

            self.player.update(self.delta_time, st)
            self.weapon.update(self.delta_time)

            self.raycaster.update()
            self.object_renderer.update()

            self.sprite_obj1.update(self.delta_time)
            self.sprite_obj2.update(self.delta_time)
  
            #self.npc.update(self.delta_time)

            for npc in self.npcs:
                npc.update(self.delta_time)


        def event(self, ev, x, y, st): ## use this for reacting to events
            key_pressed = pygame.key.get_pressed()
            self.player.reset_input()

            if (key_pressed[pygame.K_w]):
                self.player.input_vertical += 1
            if (key_pressed[pygame.K_s]):
                self.player.input_vertical -= 1    
            if (key_pressed[pygame.K_a]):
                self.player.input_horizontal -= 1
            if (key_pressed[pygame.K_d]):
                self.player.input_horizontal += 1
            
            if (key_pressed[pygame.K_LEFT]):
                self.player.input_angle -= 1
            if (key_pressed[pygame.K_RIGHT]):
                self.player.input_angle += 1

            if (key_pressed[pygame.K_SPACE]):
                self.weapon.shoot()

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
