init -1 python:
    from abc import ABC, abstractmethod
    class Weapon(ABC): ## abstract class to enforce inheritance for weapon types
        def __init__(self, 
            player,
            scale=1.0):

            #region Override variables
            ## animations
            self.idle_anim = None
            self.attack_anim = None
            self.reload_anim = None

            ## audio
            self.attack_audio = None
            self.reload_audio = None

            ## casings
            self.casing_pool = None
            self.casing_spawn_delay = 0
            
            ## stats
            self.damage = 0
            self.magazine_size = 0
            self.range = 0 ## 0 means no range limit

            self.initialize()
            #endregion

            ## constructor initialization
            self.player = player
            self.scale = scale

            self.width, self.height = get_image_size(self.idle_anim.image)
            self.scaled_width, self.scaled_height = int(self.width * self.scale), int(self.height * self.scale)
            self.pos_x = FpsSettings.HALF_SCREEN_WIDTH - (self.scaled_width // 2)
            self.pos_y = FpsSettings.SCREEN_HEIGHT - self.scaled_height

            self.at = 0
            self.current_animation = self.idle_anim

            self.casing_spawned = False
            self.casings = []


        @abstractmethod
        def initialize(self):
            pass

        #region Update and Draw methods

        def update(self, delta_time):

            ## update anmiation time if our current animation has a duration
            if (self.current_animation.duration > 0):

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
            offset_x, offset_y = self.player.sway_offset

            ## get the weapon image, scaled if appropriate
            weapon_image = self.current_animation.image if self.scale == 1.0 else Transform(self.current_animation.image, size=(self.scaled_width, self.scaled_height))

            ## create a render for the weapon image
            weapon_render = renpy.render(weapon_image, FpsSettings.SCREEN_WIDTH, FpsSettings.SCREEN_HEIGHT, st, min(self.current_animation.duration - 0.0001, self.at)) ## make sure dont overshoot duration to avoid wrapping back to start

            ## draw weapon render to the screen
            screen.blit(weapon_render, (self.pos_x + offset_x, self.pos_y + offset_y))
        
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


        def attack(self):

            ## ignore attack input if we are not ready toattackt
            if (self.current_animation != self.idle_anim):
                return
            
            if (self.attack_audio is not None):
                renpy.play(self.attack_audio)

            ## set variables to allow animations to play correctly
            self.at = 0
            self.casing_spawned = False
            self.current_animation = self.attack_anim
            self.player.is_attacking = True
