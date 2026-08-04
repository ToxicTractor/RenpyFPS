define armor_pickup_anim = AnimationData("armor", None)

init python:
    class ArmorPickup(PickupObject):
        def __init__(self, game, pos):
            super().__init__(game, armor_pickup_anim, pos, scale=.3, height_shift=1.5)

            self.armor_amount = 50


        def initialize(self):
            self.pickup_audio = "audio/fps/pickups/armor_pickup.ogg"


        def _effect(self):

            self.game.player.apply_armor(self.armor_amount)

            self.game.notification.show(f"{self.armor_amount} armor was added!", notification_type=ENotificationType.Pickup)


        def _can_pick_up(self):
            
            return self.game.player.armor < self.game.player.max_armor

