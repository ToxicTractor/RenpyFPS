define shotgun_idle_anim = AnimationData("shotgun_idle", 0)
define shotgun_shoot_anim = AnimationData("shotgun_shoot", 0.8)
define shotgun_shell_anim = AnimationData("shotgun_shell", 0.3)

image shotgun_idle:
    "shotgun_idle_01"

image shotgun_shoot = Animation(
    "shotgun_shoot_01", 0.05,
    "shotgun_shoot_02", 0.05,
    "shotgun_reload_01", 0.1,
    "shotgun_reload_02", 0.1,
    "shotgun_reload_03", 0.2,
    "shotgun_reload_02", 0.2,
    "shotgun_reload_01", 0.1,
) 

image shotgun_shell = Animation(
    "shotgun_shell_01", 0.1,
    "shotgun_shell_02", 0.1,
    Transform("shotgun_shell_01", xzoom=-1), 0.1
) ## 0.2 seconds

init python:
    class ShotgunWeapon(Weapon):
        def __init__(self, player):
            super().__init__(player, scale=2.0)
            
        def initialize(self):

            ## animations
            self.idle_anim = shotgun_idle_anim
            self.attack_anim = shotgun_shoot_anim

            ## audio
            self.attack_audio = "audio/fps/weapons/shotgun_shoot.ogg"

            ## casings
            self.casing_pool = ObjectPool(
                Casing(
                    shotgun_shell_anim, 
                    (FpsSettings.HALF_SCREEN_WIDTH - 40, FpsSettings.SCREEN_HEIGHT - 80), 
                    lifetime=0.3, 
                    scale=2.0),
                2)
            self.casing_spawn_delay = 0.3
            
            ## stats
            self.damage = 25
