from game.code.fps.classes.AnimationData_ren import AnimationData
from game.code.fps.classes.world.pickups.PickupObject_ren import PickupObject
from game.code.fps.enums.ENotificationType_ren import ENotificationType

"""renpy
init python:
"""

armor_pickup_anim = AnimationData("armor", None)

class ArmorPickup(PickupObject):
    def __init__(self, game, pos):
        super().__init__(game, armor_pickup_anim, pos, scale=.5)

        self.armor_amount = 50


    def initialize(self):
        self.pickup_audio = "audio/fps/pickups/armor_pickup.ogg"


    def _effect(self):

        self.game.player.apply_armor(self.armor_amount)

        self.game.notification.show(f"{self.armor_amount} armor was added!", type=ENotificationType.Positive)


    def _can_pick_up(self):

        return self.game.player.armor < self.game.player.max_armor
