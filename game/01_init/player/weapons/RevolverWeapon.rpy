define revolver_idle_anim = AnimationData("revolver_idle", None)
define revolver_shoot_anim = AnimationData("revolver_shoot", 0.8)
define revolver_reload_anim = AnimationData("revolver_reload", 1.2)

image revolver_idle:
    "revolver_idle_01"

image revolver_shoot = Animation(
    "revolver_shoot_01", 0.1,
    "revolver_shoot_05", 0.2,
    "revolver_shoot_04", 0.2,
    "revolver_shoot_03", 0.2,
    "revolver_shoot_02", 0.1,
) # 0.8 seconds

image revolver_reload = Animation(
    "revolver_reload_01", 0.05,
    "revolver_reload_02", 0.05,
    "revolver_reload_03", 0.05,
    "revolver_reload_04", 0.05,
    "revolver_reload_05", 0.05,
    "revolver_reload_06", 0.05,
    "revolver_reload_07", 0.05,
    "revolver_reload_08", 0.05,
    "revolver_reload_09", 0.05,
    "revolver_reload_10", 0.05,
    "revolver_reload_11", 0.05,
    "revolver_reload_12", 0.05,
    "revolver_reload_13", 0.05,
    "revolver_reload_14", 0.05,
    "revolver_reload_15", 0.05,
    "revolver_reload_16", 0.05,
    "revolver_reload_17", 0.05,
    "revolver_reload_18", 0.05,
    "revolver_reload_19", 0.05,
    "revolver_reload_20", 0.05,
    "revolver_reload_05", 0.05,
    "revolver_reload_04", 0.05,
    "revolver_reload_03", 0.05,
    "revolver_reload_02", 0.05,
    "revolver_reload_01", 0.05,
) ## 1.2 seconds

init python:
    class RevolverWeapon(Weapon):
        NAME = ".44 magnum"
        def __init__(self, player):
            super().__init__(player, scale=3.0)

        def initialize(self):

            ## animations
            self.idle_anim = revolver_idle_anim
            self.attack_anim = revolver_shoot_anim
            self.reload_anim = revolver_reload_anim

            ## audio
            self.attack_audio = "audio/fps/weapons/revolver_shoot.ogg"
            self.equip_audio = "audio/fps/weapons/revolver_equip.ogg"
            self.reload_audio = "audio/fps/weapons/revolver_reload.ogg"
            self.no_ammo_audio = "audio/fps/weapons/no_ammo_click.ogg"
            
            ## stats
            self.damage = 100
            self.attack_delay = 1.2
            self.penetration = 10
            self.ammo_type = RevolverAmmoType()
            self.magazine_size = 6
            self.magazine_ammo = 6
            self.reload_duration = 1.5

            ## ui
            self.name = RevolverWeapon.NAME
            self.icon = "revolver_icon"
