init -2 python:
    class SpriteObject:
        def __init__(self, game, sprite_anim, pos=(11.5, 9.5), scale=1.0, height_shift=0.0, is_solid=False, radius=0.25, has_shadow=True, shadow_scale=1.0):
            self.game = game
            self.player = game.player
            self.sprite_anim = sprite_anim
            self.pos = Vector2(*pos)
            self.scale = scale
            self.height_shift = height_shift
            self._is_solid = is_solid
            self.radius = radius
            
            self.has_shadow = has_shadow
            self.shadow_scale = shadow_scale
            self.shadow_image = Transform(ImageReference("shadow"), alpha=0.25)
            self.shadow_width, self.shadow_height = get_image_size(self.shadow_image)

            self.sprite_width, self.sprite_height = get_image_size(sprite_anim.image)
            self.half_image_width = self.sprite_width // 2

            self.image_ratio = self.sprite_width / self.sprite_height

            self.at = 0

            self._min_render_depth = 0.1

        @property
        def coord(self):
            return Vector2(int(self.pos.x), int(self.pos.y))

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
            dx = self.pos.x - self.player.pos.x
            dy = self.pos.y - self.player.pos.y

            ## calculate angle from world x to direction of above
            ## note atan2 takes y first and x second
            theta = math.atan2(dy, dx)

            ## calculate angle between player view direction and theta
            da = theta - self.player.angle
            da = (da + math.pi) % math.tau - math.pi

            ## figure out how many rays the sprite spans
            ray_count = da / FpsSettings.DELTA_ANGLE

            ## calculate screen position
            screen_x = (FpsSettings.HALF_RAY_COUNT + ray_count) * FpsSettings.PROJECTION_SCALE

            ## calculate depth
            depth = math.hypot(dx, dy) * math.cos(da)

            ## return early if the object is not on screen
            if (depth < self._min_render_depth
                or screen_x < -self.half_image_width
                or screen_x > self.half_image_width + FpsSettings.SCREEN_WIDTH):
                return None

            ## calculate projection scale
            projection = FpsSettings.PROJECTION_DISTANCE / max(depth, 0.0001)

            ## calculate ground position
            ground_y = (FpsSettings.HALF_SCREEN_HEIGHT + FpsSettings.PROJECTION_DISTANCE / max(depth, 0.0001) * 0.5)

            return (depth, screen_x, projection, ground_y)


        def get_sprite_projection(self):
            
            projection_data = self.get_projection()

            if projection_data is None:
                return None

            depth, screen_x, projection, ground_y = projection_data

            projection *= self.scale

            ## calculate projected sprite dimensions
            projection_width = int(projection * self.image_ratio)
            projection_height = int(projection)

            half_projection_width = projection_width // 2

            ## apply optional height shift
            height_shift = projection_height * self.height_shift

            ## calculate position
            pos = Vector2(screen_x - half_projection_width, ground_y - projection_height + height_shift)

            ## make sure animation time stays within duration
            at = min(self.sprite_anim.duration - 0.0001 if self.sprite_anim.duration else 0, self.at)

            return ProjectionResult(
                depth,
                depth,
                self.sprite_anim.image,
                Rect(0, 0, self.sprite_width, self.sprite_height),
                Vector2(projection_width, projection_height),
                pos,
                at,
                None,
                None
            )


        def get_shadow_projection(self):
            
            if (not self.has_shadow):
                return

            projection_data = self.get_projection()

            if projection_data is None:
                return None

            depth, screen_x, projection, ground_y = projection_data

            projection *= self.shadow_scale * 0.002 ## adjust shadow scale, since it is way to bit for some reason

            ## calculate shadow dimensions
            shadow_width = int(projection * self.shadow_width)
            shadow_height = int(projection * self.shadow_height)

            ## calculate position
            pos = Vector2(screen_x - shadow_width // 2, ground_y - shadow_height // 2)

            return ProjectionResult(
                FpsSettings.MAX_DEPTH, ## we always want to draw the shadow behind other things no matter how far or close they are
                depth,
                self.shadow_image,
                Rect(0, 0, self.shadow_width, self.shadow_height),
                Vector2(shadow_width, shadow_height),
                pos,
                0,
                None,
                None
            )