init python:

    class ObjectRenderer():
        
        def __init__(self, game):
            self.game = game
            self.wall_textures = self.load_wall_textures()
            self.wall_slice_cache = {}

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


        def draw(self, render):
            self.draw_sky(render)
            self.draw_floor(render)
            self.draw_objects(render)
        

        def get_wall_slice(self, texture_id, crop_x, height):
            key = (texture_id, crop_x, int(height))

            cached_slice = self.wall_slice_cache.get(key)

            if (cached_slice):
                return cached_slice

            else:
                slice = Transform(
                    self.wall_textures[texture_id],
                    crop=(crop_x, 0, 1, FpsSettings.TEXTURE_SIZE),
                    size=(FpsSettings.PROJECTION_SCALE, int(height))
                )
                
                self.wall_slice_cache[key] = slice

                return slice


        def draw_objects(self, render):
            objects_to_render = self.game.raycaster.objects_to_render
            
            for depth, texture, crop_x, projection_height, pos in objects_to_render:
                
                #wall_slice = self.get_wall_slice(texture, crop_x, projection_height)
                wall_slice = Transform(
                    self.wall_textures[texture],
                    crop=(crop_x, 0, 1, FpsSettings.TEXTURE_SIZE),
                    size=(FpsSettings.PROJECTION_SCALE, int(projection_height)),
                    matrixcolor=BrightnessMatrix(-(depth / FpsSettings.MAX_DEPTH))
                    #matrixcolor=OpacityMatrix((1 - (depth / FpsSettings.MAX_DEPTH)))
                )

                wall_render = renpy.render(wall_slice, FpsSettings.PROJECTION_SCALE, int(projection_height), 0, 0)

                render.blit(wall_render, pos)

        def draw_floor(self, render):

            floor_render = renpy.render(self.floor_image, FpsSettings.SCREEN_WIDTH, FpsSettings.HALF_SCREEN_HEIGHT, 0, 0)

            render.blit(floor_render, (0, FpsSettings.HALF_SCREEN_HEIGHT))


        def draw_sky(self, render):
            
            if (self.is_inside):

                ceiling_render = renpy.render(self.sky_image, FpsSettings.SCREEN_WIDTH, FpsSettings.HALF_SCREEN_HEIGHT, 0, 0)

                render.blit(ceiling_render, (0, 0))

                return

            self.sky_offset = (self.game.player.angle / (2 * math.pi) * FpsSettings.SCREEN_WIDTH) % FpsSettings.SCREEN_WIDTH
            
            sky_render = renpy.render(self.sky_image, FpsSettings.SCREEN_WIDTH, FpsSettings.HALF_SCREEN_HEIGHT, 0, 0)
            
            for i in range(-1, 4):
                render.blit(sky_render, ((i * FpsSettings.HALF_SCREEN_WIDTH - self.sky_offset), 0))


        def load_wall_textures(self):
            return {
                1: Image("images/fps/textures/walls/stone_wall_01.jpg", oversample=4),
                2: Image("images/fps/textures/walls/stone_wall_02.png", oversample=1.875),
                3: Image("images/fps/textures/walls/stone_wall_03.png", oversample=1.875),
                4: Image("images/fps/textures/walls/stone_wall_04.png", oversample=1.875),
                5: Image("images/fps/textures/walls/wood_wall_01.png", oversample=1.875),
                6: Image("images/fps/textures/walls/stone_wall_05.png", oversample=1.875),
            }
        
