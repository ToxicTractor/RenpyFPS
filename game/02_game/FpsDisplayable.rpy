init python:
    import pygame
    class FpsDisplayable(renpy.Displayable):

        def __init__(self, scale=1):
            super().__init__()
            
            self.old_st = None
            self.delta_time = 0
            self.framerate = 0
            self.scale = scale

            self.map = Map01(scale)
            self.map.world_map[(7,8)] = DoorCell((7,8), FPS_DOOR_TEXTURES[0], FPS_DOOR_TEXTURES[1000], orientation="horizontal")
            self.map.world_map[(7,14)] = DoorCell((7,14), FPS_DOOR_TEXTURES[1], FPS_DOOR_TEXTURES[1000], orientation="vertical")
            self.map.world_map[(7,14)].is_locked = True
            self.map.world_map[(7,13)] = ButtonCell((7,13), FPS_WALL_TEXTURES[3], FPS_BUTTON_TEXTURES[0], FPS_BUTTON_TEXTURES[1], sides=["east", "west"])
            self.map.world_map[(7,13)].button_event.add_listener(self.map.world_map[7,14].interact)
            self.jukebox = FpsJukebox(self.map)
            self.player = Player(self, pos=self.map.player_start_pos, angle=230)
            self.raycaster = Raycaster(self.player, self.map)
            self.object_renderer = ObjectRenderer(self, self.player, self.map)
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

            self.player.hurt_event.add_listener(lambda: self.trigger_screen_effect("#f005", 0.1))
            self.player.heal_event.add_listener(lambda: self.trigger_screen_effect("#0f05", 0.1))

            self.fade_to_black_event = GameEvent()
            self.fade_to_clear_event = GameEvent()

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
    default fps_fader = FpsFadeOverlay(fps)
    default fps_ui = FpsUIOverlay(fps)

    add fps
    add fps_ui

    fixed: ## UI BLOCK 1
        pos 6, 818
        xysize 814, 256
        # add Solid("#0ff")
        # text "BLOCK 1":
        #     font "images/fps/ui/fonts/fps_font.ttf"
        #     color "000"
        #     align 0.5, 0.5

        fixed: ## HEALTH
            align 0.5, 0.5
            xysize 200, 100
            # add Solid("#0ff")

            text f"{fps.player.health}%":
                font "images/fps/ui/fonts/fps_font.ttf"
                size 80
                align 0.5, 0.0
                text_align 0.5
                color "#800"
                outlines [(2, "fff", 0, 0)]
            text "HEALTH":
                font "images/fps/ui/fonts/fps_font.ttf"
                size 40
                align 0.5, 1.0
                color "#999"

    fixed: ## UI FACE BLOCK
        pos 832, 818
        xysize 256, 256
        # add Solid("#f0f")
        # text "FACE":
        #     font "images/fps/ui/fonts/fps_font.ttf"
        #     color "fff"
        #     align 0.5, 0.5

    fixed: ## UI BLOCK 2
        pos 1100, 818
        xysize 814, 256
        # add Solid("#ff0")
        # text "BLOCK 2":
        #     font "images/fps/ui/fonts/fps_font.ttf"
        #     color "000"
        #     align 0.5, 0.5
        

    label f"Framerate: {fps.framerate}"

    add fps_fader
