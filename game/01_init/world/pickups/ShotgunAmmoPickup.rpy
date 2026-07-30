define shotgun_ammo_pickup_anim = AnimationData("shotgun_ammo", 0)

init python:
    class ShotgunAmmoPickup(PickupObject):
        def __init__(self, game, pos):
            super().__init__(game, shotgun_ammo_pickup_anim, pos, scale=0.2, height_shift=2.4)

            self.ammo_type = "shotgun"
            self.ammo_amount = 10


        def initialize(self):
            self.pickup_distance = 0.4
            self.pickup_audio = "audio/fps/pickups/ammo_pickup.ogg"


        def _effect(self):
            
            self.game.player.ammo[self.ammo_type].add(self.ammo_amount)


        def _can_pick_up(self):
            
            return (any(weapon.ammo_type == self.ammo_type for weapon in self.game.player.weapons) and
                not self.game.player.ammo[self.ammo_type].full())



