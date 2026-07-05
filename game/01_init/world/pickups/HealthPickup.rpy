define health_pickup_anim = AnimationData("health_pack", 0)

init python:
    class HealthPickup(PickupObject):
        def __init__(self, game, pos):
            super().__init__(game, health_pickup_anim, pos, scale=0.1, height_shift=5)

            self.healing_amount = 25


        def initialize(self):
            self.pickup_distance = 0.25
            self.pickup_audio = "audio/fps/pickups/health_pickup.ogg"


        def _effect(self):

            print(f"Health pack picked up. Healed player for {self.healing_amount} HP.")

            
            