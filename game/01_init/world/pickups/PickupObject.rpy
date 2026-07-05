init -1 python:
    class PickupObject(ABC, SpriteObject):
        def __init__(self, game, sprite_anim, pos, scale=1.0, height_shift=0.0):
            super().__init__(game, sprite_anim, pos, scale, height_shift)
            
            self.pickup_distance = 0
            self.pickup_audio = None

            self.initialize()

            self._player = game.player
            self._sqr_pickup_distance = self.pickup_distance ** 2


        def initialize(self):
            pass


        def update(self, delta_time):
            super().update(delta_time)

            sqr_dist_to_player = sqr_dist(self.position, self._player.pos)

            if (sqr_dist_to_player > self._sqr_pickup_distance):
                return

            self._pickup()


        def _pickup(self):
            ## play the pickup audio if its not none
            if (self.pickup_audio is not None):
                renpy.play(self.pickup_audio)

            ## execute the effect of the pickup
            self._effect()

            ## remove the pickup from the objects in the map
            if (self in self.game.sprite_objects):
                self.game.sprite_objects.remove(self)   

            del self


        @abstractmethod
        def _effect(self):
            pass
