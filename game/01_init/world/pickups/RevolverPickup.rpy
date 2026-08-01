define revolver_pickup_anim = AnimationData("revolver", None)

init python:
    class RevolverPickup(PickupObject):
        def __init__(self, game, pos):
            super().__init__(game, revolver_pickup_anim, pos, scale=0.2, height_shift=2.4)

            self.weapon = RevolverWeapon(self.game.player)
            self.ammo_amount = 20

        @property
        def ammo_type(self):
            return self.weapon.ammo_type

        def initialize(self):
            self.pickup_audio = "audio/fps/pickups/weapon_pickup.ogg"


        def _effect(self):

            ## if player doesnt have revolver yet, give them one
            if (not self.game.player.has_weapon(self.weapon.name)):
                
                self.game.player.add_weapon(self.weapon, ammo=self.ammo_amount)

            ## otherwise we just give them the ammo
            else:
            
                self.game.player.add_ammo(self.ammo_type, self.ammo_amount)


        def _can_pick_up(self):

            ## if we dont have the weapon we can always pick it up            
            if (not self.game.player.has_weapon(self.weapon.name)):
                return True
            
            ## if we already have the weapon only pick it up if we dont have full ammo
            return (self.game.player.has_ammo_type(self.ammo_type) and 
                    not self.game.player.is_ammo_full(self.ammo_type))
