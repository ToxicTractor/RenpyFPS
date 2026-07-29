define fists_idle_anim = AnimationData("fists_idle", 0)
define fists_attack_r_anim = AnimationData("fists_attack_left", 0.4)
define fists_attack_l_anim = AnimationData("fists_attack_right", 0.4)

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
    class FistsWeapon(Weapon):
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
            self.icon = "fist_icon"


        def get_attack_anim(self):

            if (self.last_attack_anim is None or 
                self.last_attack_anim == fists_attack_l_anim):
                self.last_attack_anim = fists_attack_r_anim
            else:
                self.last_attack_anim = fists_attack_l_anim

            return self.last_attack_anim


        def trigger_on_hit_sound_effect(self):
            renpy.play(random.choice(self.on_hit_sound_effects))

