init python:
    
    class RayCaster():

        def __init__(self, game):
            self.game = game

            self.fov = math.pi / 3
            self.half_fov = self.fov / 2
            self.ray_count = config.screen_width // 2
            self.half_ray_count = self.ray_count // 2
            self.delta_angle = self.fov / self.ray_count
            self.max_depth = 20


        def cast_rays(self, canvas=None):
            player_x = self.game.player.pos_x
            player_y = self.game.player.pos_y
            map_x, map_y = self.game.player.coordinate
            
            ray_angle = self.game.player.angle - self.half_fov + 0.0001
            
            for i in range(self.ray_count):
                
                sin_angle = math.sin(ray_angle)
                cos_angle = math.cos(ray_angle)

                ## find horizontal intersections
                # horizontal_y = map_y + 1 if sin_angle > 0 else map_y - 1e-6
                # delta_y = 1 if sin_angle > 0 else -1

                # horizontal_depth = (horizontal_y - player_y) / sin_angle
                # horizontal_x = player_x + horizontal_depth * cos_angle

                # delta_depth = delta_y / sin_angle
                # delta_x = delta_depth * cos_angle

                # for i in range(self.max_depth):

                #     horizontal_tile = int(horizontal_x), int(horizontal_y)
                #     ## check if we hit a wall and break if we do
                #     if (horizontal_tile in self.game.map.world_map):
                #         break
                    
                #     horizontal_x += delta_x
                #     horizontal_y += delta_y
                #     horizontal_depth += delta_depth
                horizontal_depth = self.calculate_horizontal_depth(player_x, player_y, map_y, sin_angle, cos_angle)

                ## find vertical intersections
                # vertical_x = map_x + 1 if cos > 0 else map_x - 1e-6
                # delta_x = 1 if cos > 0 else -1

                # vertical_depth = (vertical_x - player_x) / cos_angle
                # vertical_y = player_y + vertical_depth * sin_angle

                # delta_depth = delta_x / cos_angle
                # delta_y = delta_depth * sin_angle

                # for i in range(self.max_depth):

                #     vertical_tile = int(vertical_x), int(vertical_y)
                #     ## check if we hit a wall and break if we do
                #     if (vertical_tile in self.game.map.world_map):
                #         break
                    
                #     vertical_x += delta_x
                #     vertical_y += delta_y
                #     vertical_depth += delta_depth
                vertical_depth = self.calculate_vertical_depth(player_x, player_y, map_x, sin_angle, cos_angle)

                ## the depth we need is the smaller of the 2 calculated depth values
                depth = horizontal_depth if horizontal_depth < vertical_depth else vertical_depth

                ## draw rays for debugging
                if (canvas is not None):
                    
                    canvas.line("#ff0", (player_x * self.game.scale, player_y * self.game.scale), 
                        (player_x * self.game.scale + depth * cos_angle * self.game.scale, player_y  * self.game.scale + depth * sin_angle * self.game.scale), 2)

                ray_angle += self.delta_angle


                


        def calculate_horizontal_depth(self, player_x, player_y, map_y, sin_angle, cos_angle):
            y = map_y + 1 if sin_angle > 0 else map_y - 1e-6
            delta_y = 1 if sin_angle > 0 else -1

            depth = (y - player_y) / sin_angle
            x = player_x + depth * cos_angle

            delta_depth = delta_y / sin_angle
            delta_x = delta_depth * cos_angle

            for i in range(self.max_depth):
                cell = int(x), int(y)
                
                ## check if we hit a wall and break if we do
                if (cell in self.game.map.world_map):
                    break
                
                x += delta_x
                y += delta_y
                depth += delta_depth

            return depth

        
        def calculate_vertical_depth(self, player_x, player_y, map_x, sin_angle, cos_angle):
            x = map_x + 1 if cos_angle > 0 else map_x - 1e-6
            delta_x = 1 if cos_angle > 0 else -1

            depth = (x - player_x) / cos_angle
            y = player_y + depth * sin_angle

            delta_depth = delta_x / cos_angle
            delta_y = delta_depth * sin_angle

            for i in range(self.max_depth):
                cell = int(x), int(y)

                ## check if we hit a wall and break if we do
                if (cell in self.game.map.world_map):
                    break
                
                x += delta_x
                y += delta_y
                depth += delta_depth

            return depth

        def update(self):
            self.cast_rays()