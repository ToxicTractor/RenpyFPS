import random
from game.code.fps.classes.AnimationData_ren import AnimationData
from game.code.fps.classes.player.weapons.Weapon_ren import Weapon

"""renpy
image fists_idle:
    "fists_idle_01"

image fists_attack_left = Animation(
    "fists_attack_l_01", 0.1,
    "fists_attack_l_02", 0.2,
    "fists_idle_01", 0.1,
) ## 0.4 seconds

image fists_attack_right = Animation(
    "fists_attack_r_01", 0.1,
    "fists_attack_r_02", 0.2,
    "fists_idle_01", 0.1,
) ## 0.4 seconds

init python:
"""

fists_idle_anim = AnimationData("fists_idle", None)
fists_attack_r_anim = AnimationData("fists_attack_left", 0.4)
fists_attack_l_anim = AnimationData("fists_attack_right", 0.4)

class FistsWeapon(Weapon):
    NAME = "fists"
    def __init__(self, player):
        super().__init__(player)

        self.last_attack_anim = None

        self.on_hit_sound_effects = [
            "audio/fps/weapons/punch_hit_01.ogg",
            "audio/fps/weapons/punch_hit_02.ogg",
            "audio/fps/weapons/punch_hit_03.ogg"
        ]


    def initialize(self):

        ## animations
        self.idle_anim = fists_idle_anim

        ## audio
        self.attack_audio = "audio/fps/weapons/punch_swing_01.ogg"
        self.equip_audio = "audio/fps/weapons/punch_swing_01.ogg"

        ## stats
        self.damage = 75
        self.range = 1.5
        self.penetration = 0

        ## ui
        self.name = FistsWeapon.NAME
        self.icon = "fist_icon"

    @property
    def formatted_ammo(self):
        return "n/a"

    def get_attack_anim(self):

        if (self.last_attack_anim is None or 
            self.last_attack_anim == fists_attack_l_anim):
            self.last_attack_anim = fists_attack_r_anim
        else:
            self.last_attack_anim = fists_attack_l_anim

        return self.last_attack_anim


    def trigger_on_hit_sound_effect(self):
        renpy.play(random.choice(self.on_hit_sound_effects))
