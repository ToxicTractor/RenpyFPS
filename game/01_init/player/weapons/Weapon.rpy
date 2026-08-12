init -1 python:
    class Weapon(ABC): ## abstract class to enforce inheritance for weapon types
        AUTO_RELOAD_ON_EMPTY = True
        def __init__(self, 
            player,
            scale=1.0):

            #region Override variables
            ## animations
            self.idle_anim = None
            self.attack_anim = None
            self.reload_anim = None
            self.equip_duration = 0.25
            self.equip_timer = None
            self.equip_offset = 256

            ## audio
            self.attack_audio = None
            self.reload_audio = None
            self.equip_audio = None
            self.no_ammo_audio = None

            ## casings
            self.casing_pool = None
            self.casing_spawn_delay = 0
            
            ## stats
            self.damage = 0
            self.attack_delay = 0.5
            self.magazine_size = None
            self.magazine_ammo = None
            self.ammo_type = None
            self.dump_remainding_ammo_on_reload = False
            self.range = None ## None means unlimited
            self.penetration = 0
            self.reload_duration = None

            ## ui
            self.name = "Unnamed weapon"
            self.icon = None

            self.initialize()
            #endregion

            ## constructor initialization
            self.player = player
            self.scale = scale

            self.width, self.height = get_image_size(self.idle_anim.image)
            self.scaled_width, self.scaled_height = int(self.width * self.scale), int(self.height * self.scale)
            self.pos = Vector2(FpsSettings.HALF_SCREEN_WIDTH - (self.scaled_width // 2), FpsSettings.SCREEN_HEIGHT - self.scaled_height)

            self.at = 0
            self.current_animation = self.idle_anim

            self.attack_timer = None
            self.reload_timer = None

            self.casing_spawned = False
            self.casings = []

            self.reload_begin_event = GameEvent()
            self.reload_end_event = GameEvent()

        @property
        def formatted_ammo(self):
            return f"{self.magazine_ammo}/{self.spare_ammo}"


        @property
        def spare_ammo(self):
            if (self.ammo_type is None):
                return None

            return self.player.ammo[self.ammo_type.name].current


        @abstractmethod
        def initialize(self):
            pass

        #region Update and Draw methods

        def update(self, delta_time):
            
            ## update and invoke events for reloading
            if (self.reload_timer):
                if (self.reload_timer > 0):
                    self.reload_timer -= delta_time
                else:
                    self.reload_timer = None
                    self.end_reload()

            ## update equip timer
            if (self.equip_timer):
                if (self.equip_timer > 0):
                    self.equip_timer -= delta_time
                else:
                    self.equip_timer = None

            ## update anmiation time if our current animation has a duration
            if (self.current_animation.duration):

                if (self.at >= self.current_animation.duration):
                    self.at = 0
                    self.current_animation = self.idle_anim
                else:
                    self.at += delta_time

            ## if weapon doesn't have a casing pool, just return here
            if (self.casing_pool is None):
                return

            ## spawn casing if appropriate time
            if (self.at >= self.casing_spawn_delay and not self.casing_spawned):
                self.spawn_casing()

            ## loop through our casings and despawn expired casings and update any others
            for casing in self.casings:
                if (casing.is_expired):
                    self.despawn_casing(casing)
                    continue

                casing.update(delta_time)


        ## seperate update method called from the players update for all weapons, not just the equipped one
        def update_attack_timer(self, delta_time):
            
            if (self.attack_timer):
                if (self.attack_timer > 0):
                    self.attack_timer -= delta_time
                else:
                    self.attack_timer = None


        def draw(self, screen, st):

            ## draws the weapon to the screen
            self.draw_weapon(screen, st)

            ## if we dont have a casing pool, just return here
            if (self.casing_pool is None):
                return

            ## draw each casing in our list to the screen
            for casing in self.casings:
                casing.draw(screen, st)


        def draw_weapon(self, screen, st):

            ## calculate the x and y offsets due to sway from movement
            offset_x, offset_y = elementwise_add_tuple(self.player.sway_offset, (FpsSettings.X_OFFSET, FpsSettings.Y_OFFSET))

            if (self.equip_timer and self.equip_duration > 0):
                offset_y += lerp(0, self.equip_offset, self.equip_timer / self.equip_duration)
            
            ## get the weapon image, scaled if appropriate
            weapon_image = self.current_animation.image if self.scale == 1.0 else Transform(self.current_animation.image, size=(self.scaled_width, self.scaled_height))

            ## create a render for the weapon image
            weapon_render = renpy.render(weapon_image, FpsSettings.SCREEN_WIDTH, FpsSettings.SCREEN_HEIGHT, st, min(self.current_animation.duration - 0.0001, self.at) if self.current_animation.duration else self.at) ## make sure dont overshoot duration to avoid wrapping back to start

            ## draw weapon render to the screen
            screen.blit(weapon_render, (self.pos.x + offset_x, self.pos.y + offset_y))
        
        #endregion

        def spawn_casing(self):
            
            ## gets a casing from the pool
            casing = self.casing_pool.get()

            ## if no casing was available, we just return
            if (casing is None):
                return
            
            ## add the casing to our list of casings and set the casing spawned flag to true
            self.casing_spawned = True
            self.casings.append(casing)


        def despawn_casing(self, casing):

            ## if the casing is in our list we remove it from the list
            if (casing in self.casings):
                self.casings.remove(casing)
            
            ## release the casing back to the pool
            self.casing_pool.release(casing)

        
        def get_attack_anim(self):
            return self.attack_anim
        

        def has_ammo_in_magazine(self):
            ## if we dont use ammo, we always return True
            if (not self.ammo_type):
                return True

            if (self.magazine_size):
                return self.magazine_ammo > 0
            else:
                return self.spare_ammo > 0


        def can_be_reloaded(self):
            ## if we dont use ammo, magazine size or reload duration, we always return False
            if (not self.ammo_type or
                not self.magazine_size or
                not self.reload_duration):
                return False

            ## if weapon is not ready, return False
            if (not self.is_ready()):
                return False

            return self.magazine_ammo < self.magazine_size


        def attack(self):
            
            if (not self.has_ammo_in_magazine()):
                
                if (Weapon.AUTO_RELOAD_ON_EMPTY and 
                    self.player.get_ammo_count(self.ammo_type) > 0 and 
                    self.can_be_reloaded()):
                    
                    self.start_reload()
                    return                    

                if (self.no_ammo_audio):
                    renpy.play(self.no_ammo_audio)

                self.attack_timer = 0.5
                return

            if (self.attack_audio):
                renpy.play(self.attack_audio)

            self.attack_timer = self.attack_delay

            ## subtract ammo if we have an ammo type
            if (self.ammo_type):
                if (self.magazine_size and self.magazine_size > 0):
                    self.magazine_ammo = max(self.magazine_ammo - 1, 0)
                else:
                    self.player.ammo[self.ammo_type.name].remove()

            ## set variables to allow animations to play correctly
            self.at = 0
            self.casing_spawned = False
            self.current_animation = self.get_attack_anim()


        def start_reload(self):

            self.reload_timer = self.reload_duration
            
            if (self.reload_audio):
                renpy.play(self.reload_audio)

            self.at = 0
            self.current_animation = self.reload_anim

            self.reload_begin_event.invoke()

        
        def end_reload(self):
            
            available_ammo = min(self.magazine_size, self.player.get_ammo_count(self.ammo_type))
            reloaded_ammo = available_ammo

            if (self.dump_remainding_ammo_on_reload):
                ammo_after_reload = reloaded_ammo
            else:
                reloadable_ammo = self.magazine_size - self.magazine_ammo
                reloaded_ammo = min(available_ammo, reloadable_ammo)
                ammo_after_reload = self.magazine_ammo + reloaded_ammo

            self.magazine_ammo = ammo_after_reload
            self.player.remove_ammo(self.ammo_type, reloaded_ammo)

            self.reload_end_event.invoke()


        def is_ready(self):
            
            if (self.equip_timer):
                return False
            
            if (self.attack_timer):
                return False

            if (self.reload_timer):
                return False

            return True


        def trigger_on_hit_sound_effect(self):
            return


        def equip(self):

            self.equip_timer = self.equip_duration

            if (self.equip_audio):
                renpy.play(self.equip_audio)


        def unequip(self):
            
            self.at = 0
            self.current_animation = self.idle_anim
            self.reload_timer = None

            for casing in self.casings:
                self.despawn_casing(casing)