init python:
    
    class Raycaster():

        def __init__(self, game):
            self.game = game
            self.ray_cast_result = []
            self.objects_to_render = []
            self.textures = self.game.object_renderer.wall_textures


        def get_objects_to_draw(self):
            self.objects_to_render = []

            for i, values in enumerate(self.ray_cast_result):
                depth, projection_height, texture, offset = values

                wall_column = self.textures[texture].subsurface(
                    offset * (FpsSettings.TEXTURE_SIZE - FpsSettings.PROJECTION_SCALE), 0, FpsSettings.PROJECTION_SCALE, FpsSettings.TEXTURE_SIZE
                )

                wall_column = pygame.transform.scale(wall_column, (FpsSettings.PROJECTION_SCALE, projection_height))
                wall_pos = (i * FpsSettings.PROJECTION_SCALE, FpsSettings.HALF_SCREEN_HEIGHT - projection_height // 2)

                self.objects_to_render.append((depth, wall_column, wall_pos))


        def cast_rays(self):
            self.ray_cast_result = []

            player_x = self.game.player.pos_x
            player_y = self.game.player.pos_y
            map_x, map_y = self.game.player.coordinate
            
            texture_vertical, texture_horizontal = [255], [255]

            ray_angle = self.game.player.angle - FpsSettings.HALF_FOV + 0.0001
            
            for i in range(FpsSettings.RAY_COUNT):
                
                sin_angle = math.sin(ray_angle)
                cos_angle = math.cos(ray_angle)

                ## calculate the horizontal depth
                y = map_y + 1 if sin_angle > 0 else map_y - 1e-6
                delta_y = 1 if sin_angle > 0 else -1

                horizontal_depth = (y - player_y) / sin_angle
                x = player_x + horizontal_depth * cos_angle

                delta_depth = delta_y / sin_angle
                delta_x = delta_depth * cos_angle

                for i in range(FpsSettings.MAX_DEPTH):
                    cell = int(x), int(y)
                    
                    ## check if we hit a wall and break if we do
                    if (cell in self.game.map.world_map):

                        ## the texture is passed in as a list to allow us to change it by reference
                        texture_horizontal = self.game.map.world_map[cell]
                        break
                    
                    y += delta_y
                    x += delta_x
                    horizontal_depth += delta_depth
                
                ## calculate the vertical depth
                x = map_x + 1 if cos_angle > 0 else map_x - 1e-6
                delta_x = 1 if cos_angle > 0 else -1

                vertical_depth = (x - player_x) / cos_angle
                y = player_y + vertical_depth * sin_angle

                delta_depth = delta_x / cos_angle
                delta_y = delta_depth * sin_angle

                for i in range(FpsSettings.MAX_DEPTH):
                    cell = int(x), int(y)
                    
                    ## check if we hit a wall and break if we do
                    if (cell in self.game.map.world_map):

                        ## the texture is passed in as a list to allow us to change it by reference
                        texture_vertical = self.game.map.world_map[cell]
                        break
                    
                    x += delta_x
                    y += delta_y
                    vertical_depth += delta_depth

                ## the depth we need is the smaller of the 2 calculated depth values
                if (vertical_depth < horizontal_depth):
                    depth = vertical_depth
                    texture = texture_vertical
                    y %= 1
                    offset = y if cos_angle > 0 else (1 - y)
                else:
                    depth = horizontal_depth
                    texture = texture_horizontal
                    x %= 1
                    offset = x if sin_angle < 0 else (1 - x)

                ## eliminate 'fish lense' effect
                depth *= math.cos(self.game.player.angle - ray_angle)

                ## draw 3d projection
                projection_height = FpsSettings.PROJECTION_DISTANCE / (depth + 0.0001)

                self.ray_cast_result.append((depth, projection_height, texture, offset))

                ray_angle += FpsSettings.DELTA_ANGLE


        def update(self):
            self.cast_rays()
            self.get_objects_to_draw()