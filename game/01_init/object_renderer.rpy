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


        def draw(self, render, st):
            self.draw_sky(render, st)
            self.draw_floor(render, st)
            self.draw_objects(render, st)
        

        def draw_objects(self, render, st):
            objects_to_render = self.game.raycaster.objects_to_render
            offset_x, offset_y = self.game.player.calculate_sway_offset(st)

            for depth, texture, crop_x, projection_height, pos in objects_to_render:
                
                wall_slice = Transform(
                    self.wall_textures[texture],
                    crop=(crop_x, 0, 1, FpsSettings.TEXTURE_SIZE),
                    size=(FpsSettings.PROJECTION_SCALE, int(projection_height)),
                    matrixcolor=BrightnessMatrix(-(depth / FpsSettings.MAX_DEPTH))
                )
                
                wall_render = renpy.render(wall_slice, FpsSettings.PROJECTION_SCALE, int(projection_height), 0, 0)

                render.blit(wall_render, (pos[0] + offset_x, pos[1] + offset_y))


        def draw_floor(self, render, st):

            floor_render = renpy.render(self.floor_image, FpsSettings.SCREEN_WIDTH, FpsSettings.HALF_SCREEN_HEIGHT, 0, 0)
            offset_x, offset_y = self.game.player.calculate_sway_offset(st)
            render.blit(floor_render, (0 + offset_x, FpsSettings.HALF_SCREEN_HEIGHT + offset_y))
        

        def draw_sky(self, render, st):
            offset_x, offset_y = self.game.player.calculate_sway_offset(st)
            if (self.is_inside):

                ceiling_render = renpy.render(self.sky_image, FpsSettings.SCREEN_WIDTH, FpsSettings.HALF_SCREEN_HEIGHT, 0, 0)

                render.blit(ceiling_render, (0 + offset_x, 0 + offset_y))

                return

            self.sky_offset = (self.game.player.angle / (2 * math.pi) * FpsSettings.SCREEN_WIDTH) % FpsSettings.SCREEN_WIDTH
            
            sky_render = renpy.render(self.sky_image, FpsSettings.SCREEN_WIDTH, FpsSettings.HALF_SCREEN_HEIGHT, 0, 0)
            
            for i in range(-1, 4):
                render.blit(sky_render, ((i * FpsSettings.HALF_SCREEN_WIDTH - self.sky_offset) + offset_x, 0 + offset_y))


        def load_wall_textures(self):
            return {
                1: Image("images/fps/textures/walls/stone_wall_01.jpg", oversample=4),
                2: Image("images/fps/textures/walls/stone_wall_02.png", oversample=1.875),
                3: Image("images/fps/textures/walls/stone_wall_03.png", oversample=1.875),
                4: Image("images/fps/textures/walls/stone_wall_04.png", oversample=1.875),
                5: Image("images/fps/textures/walls/wood_wall_01.png", oversample=1.875),
                6: Image("images/fps/textures/walls/stone_wall_05.png", oversample=1.875),
            }
        
