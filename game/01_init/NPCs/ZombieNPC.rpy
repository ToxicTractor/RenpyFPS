define zombie_attack_anim = AnimationData("zombie_attack", 0.5)
define zombie_idle_anim = AnimationData("zombie_idle", 0)
define zombie_walk_anim = AnimationData("zombie_walk", 0.8, True)
define zombie_hurt_anim = AnimationData("zombie_hurt", 0.4)
define zombie_death_anim = AnimationData("zombie_death", 0.5)

image zombie_attack = Animation(
    "zombie_shoot_01", 0.1,
    "zombie_shoot_02", 0.1,
    "zombie_shoot_03", 0.3
) # 0.5 seconds

image zombie_idle:
    "zombie_idle_01"

image zombie_walk = Animation(
    "zombie_walk_01", 0.2,
    "zombie_walk_02", 0.2,
    "zombie_walk_03", 0.2,
    "zombie_walk_04", 0.2
) # 0.8 seconds

image zombie_hurt = Animation(
    "zombie_hurt_01", 0.3,
    "zombie_hurt_02", 0.1
) # 0.4 seconds

image zombie_death = Animation(
    "zombie_death_01", 0.1,
    "zombie_death_02", 0.1,
    "zombie_death_03", 0.1,
    "zombie_death_04", 0.1,
    "zombie_death_05", 0.1
) # 0.5 seconds

init python: 
    class ZombieNPC(NPC):
        def __init__(self, game, pos):
            super().__init__(
                game, 
                pos, 
                sprite_anim=zombie_idle_anim, 
                scale=0.7, 
                height_shift=0.35)

            ## animations
            self.attack_anim = zombie_attack_anim
            self.idle_anim = zombie_idle_anim
            self.walk_anim = zombie_walk_anim
            self.hurt_anim = zombie_hurt_anim
            self.death_anim = zombie_death_anim

            ## audio
            self.attack_audio = "audio/fps/npcs/zombie/zombie_shoot.ogg"
            self.hurt_audio = "audio/fps/npcs/zombie/zombie_hurt.ogg"
            self.death_audio = "audio/fps/npcs/zombie/zombie_death_02.ogg"

            ## stats
            self.attack_range = 5
            self.speed = 2
            self.size = .15
            self.health = 100
            self.attack_damage = 10
            self.accuracy = 0.15