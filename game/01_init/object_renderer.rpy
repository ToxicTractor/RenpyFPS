init python:

    class ObjectRenderer():
        
        def __init__(self, game):
            self.game = game
            self.wall_textures = self.load_wall_textures()

            self.floor_image = Solid("#333") ## floor is a solid color for now
            
            self.is_inside = False
            self.sky_offset = 0
            if (self.is_inside):
                self.sky_image = Solid("#555")
            else:
                self.sky_image = Transform(
                    Image("images/fps/textures/skies/sky_sunset.png"), 
                    size=(FpsSettings.HALF_SCREEN_WIDTH, FpsSettings.HALF_SCREEN_HEIGHT)
            )

            self.objects_to_render = []


        def get_walls_to_render(self):
            self.objects_to_render = []

            for i, values in enumerate(self.game.raycaster.ray_cast_result):
                depth, projection_height, texture, offset = values
                
                ## if texture is 0 we dont want to render anything
                if (texture == 0):
                    continue

                crop_x = int(offset * (FpsSettings.TEXTURE_SIZE - 1))

                wall_pos = (i * FpsSettings.PROJECTION_SCALE, FpsSettings.HALF_SCREEN_HEIGHT - projection_height // 2)

                self.objects_to_render.append(
                    (depth,
                    self.wall_textures[texture],
                    (crop_x, 0, 1, FpsSettings.TEXTURE_SIZE),
                    (FpsSettings.PROJECTION_SCALE, int(projection_height)),
                    wall_pos,
                    0)
                )


        def update(self):
            self.get_walls_to_render()


        def draw(self, screen, st):
            sway_offset = self.game.player.calculate_sway_offset(st)

            self.draw_sky(screen, sway_offset)
            self.draw_floor(screen, sway_offset)
            self.draw_objects(screen, sway_offset, st)


        def draw_objects(self, screen, offset, st):
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


        def draw_floor(self, screen, offset):
            offset_x, offset_y = offset

            ## we simply draw a box on the lower half of the screen for the floor
            floor_render = renpy.render(self.floor_image, FpsSettings.SCREEN_WIDTH, FpsSettings.HALF_SCREEN_HEIGHT, 0, 0)
            
            screen.blit(floor_render, (0 + offset_x, FpsSettings.HALF_SCREEN_HEIGHT + offset_y))
        

        def draw_sky(self, screen, offset):
            offset_x, offset_y = offset

            ## if we are inside we just draw a box for the roof
            if (self.is_inside):

                ceiling_render = renpy.render(self.sky_image, FpsSettings.SCREEN_WIDTH, FpsSettings.HALF_SCREEN_HEIGHT, 0, 0)

                screen.blit(ceiling_render, (0 + offset_x, 0 + offset_y))

            ## if we are outside we draw a scrolling texture that repeat to simulate the sky
            else:

                self.sky_offset = (self.game.player.angle / (2 * math.pi) * FpsSettings.SCREEN_WIDTH) % FpsSettings.SCREEN_WIDTH
                
                sky_render = renpy.render(self.sky_image, FpsSettings.SCREEN_WIDTH, FpsSettings.HALF_SCREEN_HEIGHT, 0, 0)
                
                for i in range(-1, 4):
                    screen.blit(sky_render, ((i * FpsSettings.HALF_SCREEN_WIDTH - self.sky_offset) + offset_x, 0 + offset_y))


        def load_wall_textures(self):
            return {
                1: Image("images/fps/textures/walls/stone_wall_01.jpg", oversample=4),
                2: Image("images/fps/textures/walls/stone_wall_02.png", oversample=1.875),
                3: Image("images/fps/textures/walls/stone_wall_03.png", oversample=1.875),
                4: Image("images/fps/textures/walls/stone_wall_04.png", oversample=1.875),
                5: Image("images/fps/textures/walls/wood_wall_01.png", oversample=1.875),
                6: Image("images/fps/textures/walls/stone_wall_05.png", oversample=1.875),
            }
        
