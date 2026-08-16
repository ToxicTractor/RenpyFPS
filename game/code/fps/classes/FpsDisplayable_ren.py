import renpy
from renpy import config
from game.code.fps.classes.FpsItem_ren import FpsItem
from game.code.fps.classes.FpsJukebox_ren import FpsJukebox
from game.code.fps.classes.GameEvent_ren import GameEvent
from game.code.fps.classes.Raycaster_ren import Raycaster
from game.code.fps.classes.ScreenEffect_ren import ScreenEffect
from game.code.fps.classes.npcs.ZombieNPC_ren import ZombieNPC
from game.code.fps.classes.player.Player_ren import Player
from game.code.fps.classes.rendering.ObjectRenderer_ren import ObjectRenderer
from game.code.fps.classes.ui.Notification_ren import Notification
from game.code.fps.classes.world.SpriteObject_ren import SpriteObject
from game.code.fps.classes.world.Trigger_ren import Trigger
from game.code.fps.classes.world.cells.ButtonCell_ren import ButtonCell
from game.code.fps.classes.world.cells.doors.HorizontalDoorCell_ren import HorizontalDoorCell
from game.code.fps.classes.world.cells.doors.VerticalDoorCell_ren import VerticalDoorCell
from game.code.fps.classes.world.maps.Map01_ren import Map01
from game.code.fps.classes.world.pickups.ArmorPickup_ren import ArmorPickup
from game.code.fps.classes.world.pickups.HealthPickup_ren import HealthPickup
from game.code.fps.classes.world.pickups.KeyPickup_ren import KeyPickup
from game.code.fps.classes.world.pickups.RevolverPickup_ren import RevolverPickup
from game.code.fps.classes.world.pickups.ShotgunAmmoPickup_ren import ShotgunAmmoPickup
from game.code.fps.enums.EDirection_ren import EDirection
from game.code.fps.enums.EGridAlignment_ren import EGridAlignment
from game.code.fps.enums.ETriggerType_ren import ETriggerType
from game.code.fps.other.named_tuples_ren import Vector2

"""renpy
init python:
"""

class FpsDisplayable(renpy.Displayable):
    def __init__(self, scale=1):
        super().__init__()

        self.old_st = None
        self.delta_time = 0
        self.show_framerate = True
        self.framerate = 0
        self.framerate_avg = 0
        self.framerate_buffer = []
        self.framerate_avg_time = 5
        self.scale = scale
        self.is_won = False

        self.notification = Notification()
        self.map = Map01(scale)
        self.map.world_map[(7, 8)] = HorizontalDoorCell((7, 8), FPS_DOOR_TEXTURES[0], FPS_DOOR_TEXTURES[1000], EGridAlignment.X, EDirection.Right, flip_main_texture=True, is_locked=True, unlocked_by_item=FpsItem.RED_KEYCARD)
        self.map.world_map[(7, 14)] = HorizontalDoorCell((7, 14), FPS_DOOR_TEXTURES[1], FPS_DOOR_TEXTURES[1000], EGridAlignment.Y, EDirection.Left, allow_interaction=False)
        self.map.world_map[(7, 14)].is_locked = True
        self.map.world_map[(7, 13)] = ButtonCell((7, 13), FPS_WALL_TEXTURES[3], FPS_BUTTON_TEXTURES[0], FPS_BUTTON_TEXTURES[1], sides=[EDirection.Right, EDirection.Left])
        self.map.world_map[(7, 16)] = ButtonCell((7, 16), FPS_WALL_TEXTURES[3], FPS_BUTTON_TEXTURES[2], FPS_BUTTON_TEXTURES[3], sides=[EDirection.Right], can_be_closed=False, is_locked=True, unlocked_by_item=FpsItem.BLUE_KEYCARD, consumed_on_unlock_count=1)
        self.map.world_map[(7, 13)].button_event.add_listener(self.map.world_map[7,14].toggle_door_state)
        self.map.world_map[(2, 25)] = HorizontalDoorCell((2, 25), FPS_DOOR_TEXTURES[1], FPS_DOOR_TEXTURES[1000], EGridAlignment.X, EDirection.Left, is_locked=True, unlocked_by_item=FpsItem.BLUE_KEY, consumed_on_unlock_count=1)
        self.map.world_map[(0, 14)]._overlay_images = self.map.world_map[(0, 14)]._construct_overlay_images_dict({ EDirection.Right: FPS_WALL_OVERLAY_TEXTURES[0] })

        self.map.world_map[(11, 21)] = VerticalDoorCell((11, 21), FPS_DOOR_TEXTURES[1], FPS_DOOR_TEXTURES[1000], EGridAlignment.X, EDirection.Up, can_be_closed=False)
        self.map.world_map[(14, 18)] = VerticalDoorCell((14, 18), FPS_DOOR_TEXTURES[1], FPS_DOOR_TEXTURES[1000], EGridAlignment.Y, EDirection.Down, allow_interaction=False)

        self.jukebox = FpsJukebox(self.map)
        self.player = Player(self, pos=self.map.player_start_pos, angle=0)
        self.player.pos = Vector2(1.5, 10.5)
        self.raycaster = Raycaster(self.player, self.map)
        self.object_renderer = ObjectRenderer(self, self.player, self.map)

        self.sprite_objects = [
            SpriteObject(self, candlestick_anim, scale=0.7, is_solid=True),
            SpriteObject(self, torch_anim, pos=(14.5, 15.5), shadow_scale=0.5),
            HealthPickup(self, (2.5, 14.5)),
            ArmorPickup(self, (3.5, 14.5)),
            ShotgunAmmoPickup(self, (2.5, 15.5)),
            RevolverPickup(self, (7.5, 4.5)),
            KeyPickup(self, (1.5, 18.5), red_keycard_pickup_anim, FpsItem.RED_KEYCARD, scale=0.25),
            KeyPickup(self, (1.5, 19.5), yellow_keycard_pickup_anim, FpsItem.YELLOW_KEYCARD, scale=0.25),
            KeyPickup(self, (1.5, 20.5), blue_keycard_pickup_anim, FpsItem.BLUE_KEYCARD, scale=0.25),
            KeyPickup(self, (1.5, 21.5), red_key_pickup_anim, FpsItem.RED_KEY),
            KeyPickup(self, (1.5, 22.5), yellow_key_pickup_anim, FpsItem.YELLOW_KEY),
            KeyPickup(self, (1.5, 23.5), blue_key_pickup_anim, FpsItem.BLUE_KEY),
        ]

        self.npcs = [
            #ZombieNPC(self, pos=(2.5, 5.5)),
            ZombieNPC(self, pos=(13.5, 6.5)),
            ZombieNPC(self, pos=(8.5, 23.5)),
            ZombieNPC(self, pos=(9.5, 26.5)),
            ZombieNPC(self, pos=(16.5, 22.5)),
            ZombieNPC(self, pos=(21.5, 28.5)),
            ZombieNPC(self, pos=(28.5, 22.5)),
            ZombieNPC(self, pos=(17.5, 8.5)),
            ZombieNPC(self, pos=(26.5, 4.5)),
            ZombieNPC(self, pos=(27.5, 4.5))
        ]

        self.triggers = {
            "door_1_trigger": Trigger(self, (12, 16), (5, 5), trigger_type=ETriggerType.Any),
            "win_trigger": Trigger(self, (4, 4), (7, 4), once_only=True)
        }
        ## link trigger to door cell
        self.triggers["door_1_trigger"].enter_event.add_listener(self.map.world_map[(14, 18)].open_door)
        self.triggers["door_1_trigger"].exit_event.add_listener(self.map.world_map[(14, 18)].close_door) 

        ## set up the win trigger
        self.triggers["win_trigger"].enter_event.add_listener(self.win)

        self.screen_effect = ScreenEffect()

        self.modify_renpy_keymaps()
        self.jukebox.play()

        self.player.hurt_event.add_listener(self.screen_effect.trigger_hurt)
        self.player.heal_event.add_listener(self.screen_effect.trigger_heal)
        self.player.gain_armor_event.add_listener(self.screen_effect.trigger_armor_pickup)

        self.won_event = GameEvent()

        ## fade from black at the beginning of the game
        fps_fader.fade_to_clear()


    @staticmethod
    def modify_renpy_keymaps(): # TODO: Move this method to settings file

        config.keymap["screenshot"] = []
        config.keymap["director"] = []

        renpy.clear_keymap_cache()


    @staticmethod
    def restore_keymaps(): # TODO: Move this method to settings file
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

        self.notification.update(self.delta_time)

        ## stop the game if the player dies
        if (not self.player.is_alive or self.is_won):
            return

        self.player.update(self.delta_time, st)
        self.map.update(self.delta_time)

        for obj in self.sprite_objects:
            obj.update(self.delta_time)

        for npc in self.npcs:
            npc.update(self.delta_time)

        for trigger in self.triggers.values():
            trigger.update(self.delta_time)

        self.object_renderer.update(self.delta_time)

        self.screen_effect.update(self.delta_time)


    def event(self, ev, x, y, st): ## use this for reacting to events

        self.player.handle_input()


    ## calculates and sets delta time
    def update_delta_time(self, st):

        if (self.old_st is None):
            self.delta_time = st
            self.old_st = st
        else:
            self.delta_time = st - self.old_st
            self.old_st = st

        if (self.show_framerate):
            self.calculate_framerate(st)


    def calculate_framerate(self, st):

        self.framerate = 0 if self.delta_time <= 0 else int(1 // self.delta_time)

        self.framerate_buffer.append((st, self.framerate))

        ## remove too old entries
        self.framerate_buffer = [item for item in self.framerate_buffer if st - item[0] < self.framerate_avg_time]

        ## find avg framerate
        self.framerate_avg = int(sum([item[1] for item in self.framerate_buffer]) // len(self.framerate_buffer))


    def trigger_screen_effect(self, color, duration):
        self.screen_effect.trigger(color, duration)


    def win(self):
        self.is_won = True
        self.won_event.invoke()
