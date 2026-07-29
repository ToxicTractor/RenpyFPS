define armor_pickup_anim = AnimationData("armor", 0)

init python:
    class ArmorPickup(PickupObject):
        def __init__(self, game, pos):
            super().__init__(game, armor_pickup_anim, pos, scale=.3, height_shift=1.5)

            self.armor_amount = 50


        def initialize(self):
            self.pickup_distance = 0.4
            self.pickup_audio = "audio/fps/pickups/armor_pickup.ogg"


        def _effect(self):

            self.game.player.modify_armor(self.armor_amount)


        def _can_pick_up(self):
            
            return self.game.player.armor < self.game.player.max_armor

