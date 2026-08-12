define health_pickup_anim = AnimationData("health_pack", None, False)

init python:
    class HealthPickup(PickupObject):
        def __init__(self, game, pos):
            super().__init__(game, health_pickup_anim, pos, scale=0.4)

            self.healing_amount = 25


        def initialize(self):
            self.pickup_audio = "audio/fps/pickups/health_pickup.ogg"


        def _effect(self):

            self.game.player.apply_heal(self.healing_amount)

            self.game.notification.show(f"{self.healing_amount} health was restored!", type=ENotificationType.Positive)


        def _can_pick_up(self):
            
            return self.game.player.health < self.game.player.max_health

