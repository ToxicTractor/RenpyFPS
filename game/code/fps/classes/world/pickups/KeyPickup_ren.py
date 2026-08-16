from game.code.fps.classes.AnimationData_ren import AnimationData
from game.code.fps.classes.world.pickups.PickupObject_ren import PickupObject
from game.code.fps.enums.ENotificationType_ren import ENotificationType
from game.code.fps.other.named_tuples_ren import InventoryItem
from game.code.fps.other.named_tuples_ren import Position

"""renpy
init python:
"""

red_keycard_pickup_anim = AnimationData("red_keycard", None)
red_key_pickup_anim = AnimationData("red_key", None)
yellow_keycard_pickup_anim = AnimationData("yellow_keycard", None)
yellow_key_pickup_anim = AnimationData("yellow_key", None)
blue_keycard_pickup_anim = AnimationData("blue_keycard", None)
blue_key_pickup_anim = AnimationData("blue_key", None)

class KeyPickup(PickupObject):
    def __init__(self, 
            game, 
            pos:                    Position, 
            animation:              AnimationData, 
            item:                   InventoryItem,
            scale:                  float=0.4, 
            height_shift:           float=0.0, 
            pickup_audio:           str=None, 
            trigger_notification:   bool=True):
        super().__init__(
            game, 
            animation, 
            pos, 
            scale=scale, 
            height_shift=height_shift)

        self.player = game.player
        self.item = item
        self.pickup_audio = pickup_audio
        self.trigger_notification = trigger_notification


    def _effect(self):

        self.player.inventory.add_item(self.item, 1)

        if (self.trigger_notification):
            self.game.notification.show(f"{self.item.name} was picked up!", type=ENotificationType.Positive)


    def _can_pick_up(self):
        return True
