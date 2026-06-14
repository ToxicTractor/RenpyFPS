init python:

    class ObjectRenderer():
        
        def __init__(self, game):
            self.game = game
            self.wall_textures = self.load_wall_textures()
            self.wall_slice_cache = {}
            

        def draw(self, render):
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

                wall_slice = Transform(
                    self.wall_textures[texture],
                    crop=(crop_x, 0, 1, FpsSettings.TEXTURE_SIZE),
                    size=(FpsSettings.PROJECTION_SCALE, int(projection_height))
                )

                wall_render = renpy.render(wall_slice, FpsSettings.PROJECTION_SCALE, int(projection_height), 0, 0)

                render.blit(wall_render, pos)


        def load_wall_textures(self):
            return {
                255: Image("images/textures/WallSurface9_img.jpg", oversample=4),
            }