init python:
    class ObjectRenderer():
        OCCLUSION_EPSILON = 0.05 ## avoids flicker when a sprite sits right at a wall's depth

        def __init__(self, game, player, map):
            self.game = game
            self.player = player

            self.is_inside = map.is_inside
            self.floor_image = map.floor_image
            self.sky_image = map.sky_image
            self.sky_offset = 0

            self.objects_to_render = []
            self.depth_buffer = [float("inf") for _ in range(FpsSettings.RAY_COUNT)]
            self.raycast_hits = []

            self.dda_renderer = RaycastingDDARenderer(self)
            self.matrix_renderer = Matrix3DRenderer(self)

#region Public methods

        def update(self, delta_time):
            self.objects_to_render = []
            self.raycast_hits = raycast_hits = self.game.raycaster.cast_rays_dda()

            self._build_depth_buffer(raycast_hits)

            if (FpsSettings.USE_DDA_RENDERING):
                self.dda_renderer.prepare_cells(raycast_hits)

            self._prepare_sprite_objects()


        def draw(self, screen, st):
            offset = elementwise_add_tuple(self.player.sway_offset, (FpsSettings.X_OFFSET, FpsSettings.Y_OFFSET))

            self._draw_sky(screen, offset)
            self._draw_floor(screen, offset)

            if (FpsSettings.USE_DDA_RENDERING):
                self.dda_renderer.draw(screen, offset, st)
            else:
                self.matrix_renderer.draw(screen, offset, st)

#endregion

#region Private methods

        def _build_depth_buffer(self, raycast_hits):
            self.depth_buffer = [float("inf") for _ in range(FpsSettings.RAY_COUNT)]

            for ray_index, hits in enumerate(raycast_hits):
                if hits:
                    self.depth_buffer[ray_index] = hits[0].near_depth


        def _prepare_sprite_objects(self):

            for sprite_object in self.game.sprite_objects + self.game.npcs:
                projection_result = sprite_object.get_sprite_projection()

                if (projection_result):

                    if (self._is_sprite_occluded(projection_result)):
                        continue

                    self.objects_to_render.append(projection_result)

                    shadow_projection = sprite_object.get_shadow_projection()

                    if (shadow_projection):
                        self.objects_to_render.append(shadow_projection)


        def _is_sprite_occluded(self, projection_result):
            """
            Returns True if every screen column the sprite covers has a nearer wall in front of it.
            """
            left = projection_result.position.x
            right = left + projection_result.size.x

            if (FpsSettings.USE_DDA_RENDERING):
                start_ray = max(int(left // FpsSettings.PROJECTION_SCALE), 0)
                end_ray = min(int(right // FpsSettings.PROJECTION_SCALE), FpsSettings.RAY_COUNT - 1)
            else:
                start_ray = max(int(screen_x_to_ray_index(left)), 0)
                end_ray = min(int(screen_x_to_ray_index(right)), FpsSettings.RAY_COUNT - 1)

            if start_ray > end_ray:
                return False

            sprite_depth = projection_result.near_depth

            for ray_index in range(start_ray, end_ray + 1):
                if sprite_depth <= self.depth_buffer[ray_index] + self.OCCLUSION_EPSILON:
                    return False

            return True


        def _draw_floor(self, screen, offset):
            """
            Draws the floor to the screen.
            """
            offset_x, offset_y = offset

            ## we simply draw a box on the lower half of the screen for the floor
            floor_render = renpy.render(self.floor_image, FpsSettings.SCREEN_WIDTH, FpsSettings.HALF_SCREEN_HEIGHT, 0, 0)

            screen.blit(floor_render, (0 + offset_x, FpsSettings.HALF_SCREEN_HEIGHT + offset_y))


        def _draw_sky(self, screen, offset):
            """
            Draws the sky or ceiling to the screen.
            """
            offset_x, offset_y = offset

            ## if we are inside we just draw a box for the roof
            if (self.is_inside):

                ceiling_render = renpy.render(self.sky_image, FpsSettings.SCREEN_WIDTH, FpsSettings.HALF_SCREEN_HEIGHT, 0, 0)

                screen.blit(ceiling_render, (0 + offset_x, 0 + offset_y))

            ## if we are outside we draw a scrolling texture that repeat to simulate the sky
            else:

                sky_render = renpy.render(self.sky_image, FpsSettings.SCREEN_WIDTH, FpsSettings.SCREEN_HEIGHT, 0, 0)

                tile_width = FpsSettings.SCREEN_WIDTH
                sky_offset = (self.player.angle / (2 * math.pi) * tile_width) % tile_width

                x = -sky_offset + offset_x

                screen.blit(sky_render, (x, offset_y))
                screen.blit(sky_render, (x + tile_width, offset_y))

#endregion