init python:
    import pygame
    class FpsDisplayable(renpy.Displayable):

        def __init__(self, scale=1):
            super().__init__()
            
            self.old_st = None
            self.delta_time = 0
            self.framerate = 0
            self.scale = scale
            self.ui = FpsUI()

            self.map = Map01(scale)
            self.map.world_map[(7,8)] = DoorCell((7,8), FPS_DOOR_TEXTURES[0], FPS_DOOR_TEXTURES[1000], orientation="horizontal")
            self.map.world_map[(7,14)] = DoorCell((7,14), FPS_DOOR_TEXTURES[1], FPS_DOOR_TEXTURES[1000], orientation="vertical")
            self.map.world_map[(7,14)].is_locked = True
            self.map.world_map[(7,13)] = ButtonCell((7,13), FPS_WALL_TEXTURES[3], FPS_BUTTON_TEXTURES[0], FPS_BUTTON_TEXTURES[1], sides=["east", "west"])
            self.map.world_map[(7,13)].button_event.add_listener(self.map.world_map[7,14].interact)
            self.jukebox = FpsJukebox(self.map)
            self.player = Player(self, pos=self.map.player_start_pos, angle=230)
            self.object_renderer = ObjectRenderer(self.player, self.map)
            self.sprite_objects = []

            self.sprite_objects.append(SpriteObject(self, candlestick_anim, scale=0.7, height_shift=0.27))
            self.sprite_objects.append(SpriteObject(self, torch_anim, pos=(14.5, 15.5), height_shift=0.05))
            
            self.sprite_objects.append(HealthPickup(self, (2.5, 14.5)))

            self.npcs = [
                ZombieNPC(self, pos=(2.5, 5.5)),
                ZombieNPC(self, pos=(13.5, 6.5)),
                ZombieNPC(self, pos=(8.5, 23.5)),
                ZombieNPC(self, pos=(9.5, 26.5)),
                ZombieNPC(self, pos=(16.5, 22.5)),
                ZombieNPC(self, pos=(21.5, 28.5)),
                ZombieNPC(self, pos=(28.5, 22.5)),
                ZombieNPC(self, pos=(27.5, 14.5)),
                ZombieNPC(self, pos=(17.5, 8.5)),
                ZombieNPC(self, pos=(26.5, 4.5)),
                ZombieNPC(self, pos=(27.5, 4.5))
            ]

            self.screen_effect = ScreenEffect()

            self.modify_renpy_keymaps()
            self.jukebox.play()

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
            
            self.object_renderer.draw(r, st)
            self.player.draw(r, st)

            # self.map.draw_2d(canvas)
            # self.player.draw_2d(canvas)
            # for npc in self.npcs:
            #     npc.draw_2d(canvas)
            
            self.screen_effect.draw(r)

            self.ui.draw(r, st, at)

            ## redraw for the next frame and return the render
            renpy.redraw(self, 0)
            return r
        

        def update(self, st):
            
            ## update delta time
            self.update_delta_time(st)

            self.player.update(self.delta_time, st)
            self.map.update(self.delta_time)

            self.object_renderer.update()
            
            for obj in self.sprite_objects:
                obj.update(self.delta_time)

            for npc in self.npcs:
                npc.update(self.delta_time)

            self.screen_effect.update(self.delta_time)


        def event(self, ev, x, y, st): ## use this for reacting to events
            key_pressed = pygame.key.get_pressed()
            
            self.player.handle_input(key_pressed)

            renpy.restart_interaction() ## make the interaction restart so text outside of the displayable can be updated


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

        def trigger_screen_effect(self, color, duration):
            self.screen_effect.trigger(color, duration) 


screen FpsScreen():

    modal True

    default fps = FpsDisplayable(scale=30)

    add fps

    label f"Framerate: {fps.framerate}"
