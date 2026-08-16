from game.code.fps.classes.AnimationData_ren import AnimationData
from game.code.fps.classes.player.ammo.AmmoType_ren import ShotgunAmmoType
from game.code.fps.classes.world.pickups.PickupObject_ren import PickupObject

"""renpy
init python:
"""

shotgun_ammo_pickup_anim = AnimationData("shotgun_ammo", None)

class ShotgunAmmoPickup(PickupObject):
    def __init__(self, game, pos):
        super().__init__(game, shotgun_ammo_pickup_anim, pos, scale=0.2)

        self.ammo_type = ShotgunAmmoType()
        self.ammo_amount = 10


    def initialize(self):
        self.pickup_audio = "audio/fps/pickups/ammo_pickup.ogg"


    def _effect(self):

        self.game.player.ammo[self.ammo_type.name].add(self.ammo_amount)

        self.game.notification.show(f"{self.ammo_amount} {self.ammo_type.name} ammo was picked up!", type=ENotificationType.Positive)


    def _can_pick_up(self):

        return (self.game.player.has_ammo_type(self.ammo_type) and 
                not self.game.player.is_ammo_full(self.ammo_type))
