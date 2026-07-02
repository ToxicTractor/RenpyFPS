init python:
    class ObjectRenderer():
        def __init__(self, player, map):

            self.player = player

            self.is_inside = map.is_inside
            self.floor_image = map.floor_image
            self.sky_image = map.sky_image
            self.sky_offset = 0

            self.objects_to_render = []

#region Public methods

        def update(self):
            self.objects_to_render = []

            for i, values in enumerate(self.player.raycaster.ray_cast_results):
                depth, projection_height, cell, offset = values
                
                if (cell.type == "empty"):
                    continue

                texture = cell.image

                crop_x = int(offset * (FpsSettings.TEXTURE_SIZE - 1))

                wall_pos = (i * FpsSettings.PROJECTION_SCALE, FpsSettings.HALF_SCREEN_HEIGHT - projection_height // 2)
            
                self.objects_to_render.append(
                    (depth,
                    texture,
                    (crop_x, 0, 1, FpsSettings.TEXTURE_SIZE),
                    (FpsSettings.PROJECTION_SCALE, int(projection_height)),
                    wall_pos,
                    0)
                )


        def draw(self, screen, st):
            sway_offset = self.player.sway_offset

            self._draw_sky(screen, sway_offset)
            self._draw_floor(screen, sway_offset)

            self._draw_objects(screen, sway_offset, st)

#endregion

#region Private methods

        def _draw_objects(self, screen, offset, st):
            """
            Draws objects to the screen. Objects inclued walls, NPCs, static objets, etc.
            """
            offset_x, offset_y = offset
            
            ## sort the list by depth to make sure we draw element in the correct order
            self.objects_to_render = sorted(self.objects_to_render, reverse=True)
            
            for depth, texture, crop, projection_size, pos, at in self.objects_to_render:
                
                wall_slice = Transform(
                    texture,
                    crop=crop,
                    size=projection_size,
                    matrixcolor=BrightnessMatrix(-(depth / FpsSettings.MAX_DEPTH))
                )
                
                wall_render = renpy.render(wall_slice, FpsSettings.PROJECTION_SCALE, int(projection_size[1]), st, at)

                screen.blit(wall_render, (pos[0] + offset_x, pos[1] + offset_y))


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

                self.sky_offset = (self.player.angle / (2 * math.pi) * FpsSettings.SCREEN_WIDTH) % FpsSettings.SCREEN_WIDTH
                
                sky_render = renpy.render(self.sky_image, FpsSettings.SCREEN_WIDTH, FpsSettings.HALF_SCREEN_HEIGHT, 0, 0)
                
                for i in range(-1, 4):
                    screen.blit(sky_render, ((i * FpsSettings.HALF_SCREEN_WIDTH - self.sky_offset) + offset_x, 0 + offset_y))  

#endregion