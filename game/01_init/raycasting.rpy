init python:
    
    class RayCaster():

        def __init__(self, game):
            self.game = game


        def cast_rays(self, canvas=None):
            player_x = self.game.player.pos_x
            player_y = self.game.player.pos_y
            map_x, map_y = self.game.player.coordinate
            
            ray_angle = self.game.player.angle - FpsSettings.HALF_FOV + 0.0001
            
            for i in range(FpsSettings.RAY_COUNT):
                
                sin_angle = math.sin(ray_angle)
                cos_angle = math.cos(ray_angle)

                ## calculate the horizontal and vertical depth
                horizontal_depth = self.calculate_depth(player_x, player_y, map_x, map_y, sin_angle, cos_angle, True)
                vertical_depth = self.calculate_depth(player_x, player_y, map_x, map_y, sin_angle, cos_angle, False)

                ## the depth we need is the smaller of the 2 calculated depth values
                depth = horizontal_depth if horizontal_depth < vertical_depth else vertical_depth

                ## eliminate 'fish lense' effect
                depth *= math.cos(self.game.player.angle - ray_angle)

                ## draw 3d projection
                projection_height = FpsSettings.PROJECTION_DISTANCE / (depth + 0.0001)

                if (canvas is not None):
                    color = [255 / (1 + depth ** 5 * 0.00002)] * 3
                    canvas.rect(color, (i * FpsSettings.PROJECTION_SCALE, FpsSettings.HALF_SCREEN_HEIGHT - projection_height // 2, FpsSettings.PROJECTION_SCALE, projection_height))

                # ## draw rays for 2d debugging
                # if (canvas is not None):
                    
                #     canvas.line("#ff0", (player_x * self.game.scale, player_y * self.game.scale), 
                #         (player_x * self.game.scale + depth * cos_angle * self.game.scale, player_y  * self.game.scale + depth * sin_angle * self.game.scale), 2)

                ray_angle += FpsSettings.DELTA_ANGLE


        ## calculates either vertical or horizontal depth
        def calculate_depth(self, player_x, player_y, map_x, map_y, sin_angle, cos_angle, horizontal):
            
            if (horizontal):
                player_primary = player_y
                player_secondary = player_x
                trig_primary = sin_angle
                trig_secondary = cos_angle
                map_coordinate_component = map_y
            else:
                player_primary = player_x
                player_secondary = player_y
                trig_primary = cos_angle
                trig_secondary = sin_angle
                map_coordinate_component = map_x

            primary = map_coordinate_component + 1 if trig_primary > 0 else map_coordinate_component - 1e-6
            delta_primary = 1 if trig_primary > 0 else -1

            depth = (primary - player_primary) / trig_primary
            secondary = player_secondary + depth * trig_secondary

            delta_depth = delta_primary / trig_primary
            delta_secondary = delta_depth * trig_secondary

            for i in range(FpsSettings.MAX_DEPTH):
                cell = (int(secondary), int(primary)) if horizontal else (int(primary), int(secondary))
                
                ## check if we hit a wall and break if we do
                if (cell in self.game.map.world_map):
                    break
                
                primary += delta_primary
                secondary += delta_secondary
                depth += delta_depth

            return depth


        def update(self):
            self.cast_rays()