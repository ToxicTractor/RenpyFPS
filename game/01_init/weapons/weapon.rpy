init python:

    class Weapon():

        def __init__(self, idle_image, shoot_image, reload_image=None, casing_image=None, scale=1.0):

            self.idle_image = ImageReference(idle_image) if idle_image is not None else None
            self.shoot_image = ImageReference(shoot_image) if shoot_image is not None else None
            self.reload_image = ImageReference(reload_image) if reload_image is not None else None
            self.casing_image = ImageReference(casing_image) if casing_image is not None else None
            
            self.idle_anim = shotgun_idle_anim
            self.shoot_anim = shotgun_shoot_anim
            self.reload_anim = None
            self.casing_anim = shotgun_shell_anim

            self.scale = scale
            self.width, self.height = get_image_size(self.idle_image)
            self.casing_width, self.casing_height = get_image_size(self.casing_anim.image) if self.casing_anim is not None else (None, None)

            self.at = 0
            self.current_animation = self.idle_anim

            self.spawn_casing_theshold = 0.3
            self.casing_spawn_offset = (FpsSettings.HALF_SCREEN_WIDTH, FpsSettings.SCREEN_HEIGHT - 150)

            self.casing_pool = ObjectPool(Casing(self.casing_anim, self.casing_spawn_offset, scale=self.scale), 2) if self.casing_anim is not None else None
            self.casing_spawned = False
            self.casings = []

        
        def update(self, delta_time):

            if (self.current_animation.duration > 0):

                if (self.at >= self.current_animation.duration):
                    self.at = 0
                    self.current_animation = self.idle_anim
                else:
                    self.at += delta_time

            if (self.at >= self.spawn_casing_theshold and not self.casing_spawned):
                self.spawn_casing()

            for casing in self.casings:
                if (casing.is_expired()):
                    self.despawn_casing(casing)
                    continue

                casing.update(delta_time)

        def spawn_casing(self):

            casing = self.casing_pool.get()

            if (casing is None):
                return

            self.casing_spawned = True
            self.casings.append(casing)


        def despawn_casing(self, casing):

            if (casing in self.casings):
                self.casings.remove(casing)
            
            self.casing_pool.release(casing)


        def draw(self, render, st):

            self.draw_weapon(render, st)

            for casing in self.casings:
                casing.draw(render, st)


        def draw_weapon(self, render, st):

            scaled_width = int(self.width * self.scale)
            scaled_height = int(self.height * self.scale)

            render_image = self.current_animation.image

            if (self.scale != 1.0):
                render_image = Transform(render_image, size=(scaled_width, scaled_height))

            weapon_render = renpy.render(render_image, scaled_width, scaled_height, st, min(self.current_animation.duration - 0.0001, self.at)) ## make sure dont overshoot duration to avoid wrapping back to start

            x = FpsSettings.HALF_SCREEN_WIDTH - (scaled_width // 2)
            y = FpsSettings.SCREEN_HEIGHT - scaled_height

            render.blit(weapon_render, (x, y))


        def shoot(self):

            ## ignore shoot input if we are not ready to shoot
            if (self.current_animation != self.idle_anim):
                return

            self.at = 0
            self.casing_spawned = False
            self.current_animation = self.shoot_anim


define shotgun_idle_anim = AnimationData("shotgun_idle", 0)
define shotgun_shoot_anim = AnimationData("shotgun_shoot", 0.8)
define shotgun_shell_anim = AnimationData("shotgun_shell", 0.2)

image shotgun_idle:
    "shotgun_idle_01"

image shotgun_shoot = Animation(
    "shotgun_shoot_01", 0.05,
    "shotgun_shoot_02", 0.05,
    "shotgun_reload_01", 0.1,
    "shotgun_reload_02", 0.1,
    "shotgun_reload_03", 0.2,
    "shotgun_reload_02", 0.2,
    "shotgun_reload_01", 0.1,
) 

image shotgun_shell = Animation(
    "shotgun_shell_01", 0.1,
    "shotgun_shell_02", 0.1
) ## 0.2 seconds
    