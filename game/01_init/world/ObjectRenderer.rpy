init python:
    class ObjectRenderer():
        def __init__(self, game, player, map):
            self.game = game
            self.player = player

            self.is_inside = map.is_inside
            self.floor_image = map.floor_image
            self.sky_image = map.sky_image
            self.sky_offset = 0

            self.objects_to_render = []

#region Public methods

        def update(self, delta_time):
            self.objects_to_render = []

            self._prepare_cells()

            self._prepare_sprite_objects()


        def draw(self, screen, st):
            offset = elementwise_add_tuple(self.player.sway_offset, (FpsSettings.X_OFFSET, FpsSettings.Y_OFFSET))

            self._draw_sky(screen, offset)
            self._draw_floor(screen, offset)

            self._draw_objects(screen, offset, st)

#endregion

#region Private methods

        def _prepare_cells(self):
            raycast_hits = self.game.raycaster.cast_rays_dda()
            self.depth_buffer = [float("inf") for _ in range(FpsSettings.RAY_COUNT)]

            for ray_index, hits in enumerate(raycast_hits):
                for hit in hits:
                    if (hit.cell.type == ECellType.Empty):
                        continue

                    texture, texture_size_ratio = hit.cell.get_texture(hit.side)

                    crop_x = int(hit.offset * (FpsSettings.TEXTURE_SIZE * texture_size_ratio - 1))
                    crop_y = 0
                    crop_width = 1
                    crop_height = FpsSettings.TEXTURE_SIZE

                    projection_height = FpsSettings.PROJECTION_DISTANCE / (hit.near_depth + 0.0001)
                    height = int(projection_height)

                    pos_x = ray_index * FpsSettings.PROJECTION_SCALE
                    pos_y = FpsSettings.HALF_SCREEN_HEIGHT - projection_height // 2

                    if (hit.cell.type is ECellType.VerticalDoor):
                        height = int(projection_height * (1.0 - hit.cell.open_amount))
                        y_offset = int(projection_height - height)
                        crop_height = int(crop_height * (1.0 - hit.cell.open_amount))

                        if (hit.cell.open_direction is EDirection.Down):
                            pos_y += y_offset
                        elif (hit.cell.open_direction is EDirection.Up):
                            crop_y = int(FpsSettings.TEXTURE_SIZE * hit.cell.open_amount)

                    projection_result = ProjectionResult(
                        hit.near_depth,
                        hit.far_depth,
                        texture,
                        (crop_x, crop_y, crop_width, crop_height),
                        (FpsSettings.PROJECTION_SCALE, height),
                        (pos_x, pos_y),
                        0,
                        hit.cell,
                        hit.side
                    )

                    self.objects_to_render.append(projection_result)


        def _prepare_sprite_objects(self):

            for sprite_object in self.game.sprite_objects + self.game.npcs:
                projection_result = sprite_object.get_sprite_projection()
                
                if (projection_result):

                    self.objects_to_render.append(projection_result)

                    shadow_projection = sprite_object.get_shadow_projection()
                    
                    if (shadow_projection):
                        self.objects_to_render.append(shadow_projection)


        def _draw_objects(self, screen, offset, st):
            """
            Draws objects to the screen. Objects inclued walls, NPCs, static objets, etc.
            """
            offset_x, offset_y = offset
            
            ## sort the list by depth to make sure we draw element in the correct order
            self.objects_to_render = sorted(self.objects_to_render, reverse=True)
            
            for near_depth, far_depth, texture, crop, projection_size, pos, at, cell, hit_direction in self.objects_to_render:
                
                if (cell is not None and cell.type == ECellType.VerticalDoor):
                    self._draw_vertical_door_horizontal_side(screen, offset, near_depth, far_depth, crop, pos, cell, st, at)

                pixel_slice = Transform(
                    texture,
                    crop=crop,
                    size=projection_size,
                    matrixcolor=BrightnessMatrix(-(near_depth / FpsSettings.MAX_DEPTH))
                )
                
                slice_render = renpy.render(pixel_slice, FpsSettings.PROJECTION_SCALE, int(projection_size[1]), st, at)

                screen.blit(slice_render, (pos[0] + offset_x, pos[1] + offset_y))


        def _draw_vertical_door_horizontal_side(self, screen, offset, near_depth, far_depth, crop, pos, cell, st, at):
            
            offset_x, offset_y = offset

            z = cell.get_horizontal_side_z()
            
            camera_z = 0.5

            near_y = (FpsSettings.HALF_SCREEN_HEIGHT + (camera_z - z) * FpsSettings.PROJECTION_DISTANCE / near_depth)
            far_y = (FpsSettings.HALF_SCREEN_HEIGHT + (camera_z - z) * FpsSettings.PROJECTION_DISTANCE / far_depth)

            top = int(min(near_y, far_y))
            bottom = int(max(near_y, far_y))

            height = bottom - top

            if height <= 0:
                return

            pixel_slice = Transform(
                cell.plane_texture,
                crop=crop,
                size=(FpsSettings.PROJECTION_SCALE, height),
                matrixcolor=BrightnessMatrix(-(near_depth / FpsSettings.MAX_DEPTH))
            )

            slice_render = renpy.render(pixel_slice, FpsSettings.PROJECTION_SCALE, height, st, at)

            screen.blit(slice_render, (pos[0] + offset_x, top + offset_y))


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