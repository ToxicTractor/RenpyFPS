init python:
    
    class Raycaster():

        def __init__(self, game):
            self.game = game
            self.ray_cast_result = []
            self.textures = self.game.object_renderer.wall_textures
            self.ray_data = self.calculate_ray_data()


        def update(self):
            self.cast_rays_dda()


        def calculate_ray_data(self):
            ray_data = []

            for i in range(FpsSettings.RAY_COUNT):
                offset = -FpsSettings.HALF_FOV + i * FpsSettings.DELTA_ANGLE

                ray_data.append((math.sin(offset), math.cos(offset)))

            return ray_data


        def cast_rays_dda(self):
            self.ray_cast_result = []

            player_x = self.game.player.pos_x
            player_y = self.game.player.pos_y
            player_angle = self.game.player.angle
            player_coord = self.game.player.coordinate ## coordinate of the grid cell of the player
            world_map = self.game.map.world_map
            
            sin_player_angle = math.sin(player_angle)
            cos_player_angle = math.cos(player_angle)

            for sin_offset, cos_offset in self.ray_data:
                ## fallback texture
                texture = 0

                ## get starting coord
                cell_x, cell_y = player_coord

                ## calculate sin and cos using our precomputed offsets
                ray_direction_x = cos_player_angle * cos_offset - sin_player_angle * sin_offset
                ray_direction_y = sin_player_angle * cos_offset + cos_player_angle * sin_offset

                ## calculate delta distance
                delta_distance_x = float('inf') if ray_direction_x == 0 else abs(1 / ray_direction_x)
                delta_distance_y = float('inf') if ray_direction_y == 0 else abs(1 / ray_direction_y)

                ## determine step direction
                step_x = -1 if ray_direction_x < 0 else 1
                step_y = -1 if ray_direction_y < 0 else 1

                ## calculate initial side distances
                if (ray_direction_x < 0):
                    side_distance_x = (player_x - cell_x) * delta_distance_x
                else:
                    side_distance_x = (cell_x + 1 - player_x) * delta_distance_x

                if (ray_direction_y < 0):
                    side_distance_y = (player_y - cell_y) * delta_distance_y
                else:
                    side_distance_y = (cell_y + 1 - player_y) * delta_distance_y

                ## only loop for a max number of steps to avoid an infinite loop 
                for _ in range(FpsSettings.MAX_DEPTH):
                    if (side_distance_x < side_distance_y):

                        side_distance_x += delta_distance_x
                        cell_x += step_x
                        side = 0
                    
                    else:

                        side_distance_y += delta_distance_y
                        cell_y += step_y
                        side = 1

                    if (cell_x, cell_y) in world_map:
                        texture = world_map[(cell_x, cell_y)]
                        break

                if (side == 0):
                    depth = (cell_x - player_x + (1 - step_x) / 2) / ray_direction_x 
                    offset = player_y + depth * ray_direction_y
                else:
                    depth = (cell_y - player_y + (1 - step_y) / 2) / ray_direction_y
                    offset = player_x + depth * ray_direction_x

                offset -= math.floor(offset)

                ## eliminate fisheye effect
                depth *= cos_offset

                ## calculate projection height
                projection_height = FpsSettings.PROJECTION_DISTANCE / (depth + 0.0001)

                self.ray_cast_result.append((depth, projection_height, texture, offset))