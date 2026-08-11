init -2 python:
    class SpriteObject:
        def __init__(self, game, sprite_anim, pos=(11.5, 9.5), scale=1.0, height_shift=0.0, is_solid=False, radius=0.25):
            self.game = game
            self.player = game.player
            self.sprite_anim = sprite_anim
            self.pos_x, self.pos_y = pos
            self.scale = scale
            self.height_shift = height_shift
            self._is_solid = is_solid
            self.radius = radius

            self.sprite_width, self.sprite_height = get_image_size(sprite_anim.image)
            self.half_image_width = self.sprite_width // 2

            self.image_ratio = self.sprite_width / self.sprite_height

            self.at = 0

            self._min_render_depth = 0.1

        @property
        def pos(self):
            return (self.pos_x, self.pos_y)

        @property
        def coord(self):
            return (int(self.pos_x), int(self.pos_y))

        @property
        def coord_x(self):
            return int(self.pos_x)

        @property
        def coord_y(self):
            return int(self.pos_y)
        
        @property
        def is_solid(self):
            return self._is_solid

        def update(self, delta_time):
            if (self.sprite_anim.duration and self.sprite_anim.duration > 0):
                self.animation_just_ended = False

                if (self.at >= self.sprite_anim.duration):
                    if (self.sprite_anim.loop):
                        self.at = 0
                    self.on_animation_end(self.sprite_anim)
                else:
                    self.at += delta_time


        def on_animation_end(self, animation):
            pass


        def get_projection(self):
            
            ## find dx and dy to the player
            dx = self.pos_x - self.player.pos_x
            dy = self.pos_y - self.player.pos_y

            ## calculate angle from world x to direction of above
            ## note atan2 takes y first and x second
            theta = math.atan2(dy, dx)

            ## calculate angle between player view direction and theta
            da = theta - self.player.angle
            da = (da + math.pi) % math.tau - math.pi ## make sure the angle wraps around, keeping the range between -pi and +pi

            ## figure out how many rays the sprite spans
            ray_count = da / FpsSettings.DELTA_ANGLE

            ## calculate screen position of the sprite
            screen_x = (FpsSettings.HALF_RAY_COUNT + ray_count) * FpsSettings.PROJECTION_SCALE

            ## calculate depth
            depth = math.hypot(dx, dy) * math.cos(da)

            ## return early if the sprite is not on screen
            if (depth < self._min_render_depth or
                screen_x < -self.half_image_width or
                screen_x > self.half_image_width + FpsSettings.SCREEN_WIDTH):
                return None

            projection = FpsSettings.PROJECTION_DISTANCE / max(depth, 0.0001) * self.scale
            projection_width = int(projection * self.image_ratio) ## projection with is multiplied by ratio since we can have non-square sprites
            projection_height = int(projection)

            half_projection_width = projection_width // 2

            ground_y = (FpsSettings.HALF_SCREEN_HEIGHT + FpsSettings.PROJECTION_DISTANCE / depth * 0.5)
            
            height_shift = projection_height * self.height_shift

            ## calculate position
            pos_x = screen_x - half_projection_width
            pos_y = ground_y - projection_height + height_shift

            ## make sure animation time stays within duration to avoid the animation looping back to the start
            at = min(self.sprite_anim.duration - 0.0001 if self.sprite_anim.duration else 0, self.at)

            ## retun projection result
            return (depth, 
                    depth, 
                    self.sprite_anim.image, 
                    Rect(0, 0, self.sprite_width, self.sprite_height),
                    Vector2(projection_width, projection_height),
                    Vector2(pos_x, pos_y),
                    at,
                    None,
                    None)