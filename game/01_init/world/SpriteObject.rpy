init -2 python:
    class SpriteObject:
        def __init__(self, game, sprite_anim, pos=(11.5, 9.5), scale=1.0, height_shift=0.0):
            self.game = game
            self.player = game.player
            self.sprite_anim = sprite_anim
            self.pos_x, self.pos_y = pos
            self.scale = scale
            self.height_shift = height_shift

            self.sprite_width, self.sprite_height = get_image_size(sprite_anim.image)
            self.half_image_width = self.sprite_width // 2

            self.image_ratio = self.sprite_width / self.sprite_height

            self.delta_x, self.delta_y = 0, 0
            self.theta = 0
            self.screen_x = 0
            self.dist = 0
            self.norm_dist = 1
            self.sprite_half_width = 0

            self.at = 0

        @property
        def position(self):
            return (self.pos_x, self.pos_y)

        def update(self, delta_time):
            if (self.sprite_anim.duration > 0):
                self.animation_just_ended = False

                if (self.at >= self.sprite_anim.duration):
                    if (self.sprite_anim.loop):
                        self.at = 0
                    self.on_animation_end(self.sprite_anim)
                else:
                    self.at += delta_time

            self.get_sprite()


        def on_animation_end(self, animation):
            pass


        def get_sprite_projection(self):
                
            proj = FpsSettings.PROJECTION_DISTANCE / max(self.norm_dist, 0.0001) * self.scale
            proj_width, proj_height = int(proj * self.image_ratio), int(proj)

            self.sprite_half_width = proj_width // 2
            
            height_shift = proj_height * self.height_shift
            pos = self.screen_x - self.sprite_half_width, FpsSettings.HALF_SCREEN_HEIGHT - proj_height // 2 + height_shift

            self.game.object_renderer.objects_to_render.append(
                (self.norm_dist,
                self.sprite_anim.image, 
                (0, 0, self.sprite_width, self.sprite_height), 
                (proj_width, proj_height), 
                pos,
                min(self.sprite_anim.duration - 0.0001, self.at))
            )


        def get_sprite(self):

            delta_x = self.pos_x - self.player.pos_x
            delta_y = self.pos_y - self.player.pos_y 
            self.delta_x, self.delta_y = delta_x, delta_y
            self.theta = math.atan2(delta_y, delta_x)

            delta = self.theta - self.player.angle
            delta = (delta + math.pi) % math.tau - math.pi

            delta_rays = delta / FpsSettings.DELTA_ANGLE
            self.screen_x = (FpsSettings.HALF_RAY_COUNT + delta_rays) * FpsSettings.PROJECTION_SCALE

            self.dist = math.hypot(delta_x, delta_y)
            self.norm_dist = self.dist * math.cos(delta)

            if (-self.half_image_width < self.screen_x < (FpsSettings.SCREEN_WIDTH + self.half_image_width) and self.norm_dist > 0.5):
                self.get_sprite_projection()
