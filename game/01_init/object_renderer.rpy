init python:

    class ObjectRenderer():
        
        def __init__(self, game):
            self.game = game
            self.wall_textures = self.load_wall_textures()


        def draw(self, render):
            self.draw_objects(render)
        

        def draw_objects(self, render):
            objects_to_render = self.game.raycaster.objects_to_render

            for depth, image, pos in objects_to_render:
                render.blit(image, pos)


        @staticmethod
        def load_texture(path, res=(FpsSettings.TEXTURE_SIZE, FpsSettings.TEXTURE_SIZE)):
            texture = pygame.image.load(path).convert_alpha()
            return pygame.transform.scale(texture, res)


        def load_wall_textures(self):
            return {
                255: self.load_texture(f"{config.gamedir}/images/textures/WallSurface9_img.jpg"),
            }