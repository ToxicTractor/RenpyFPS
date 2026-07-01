init python:
    class Raycaster():
        def __init__(self, player, map):
            self.player = player
            self.world_map = map.world_map
            self.ray_cast_results = []
            self.ray_data = self._calculate_ray_data()

#region Public methods

        def update(self):
            self._cast_rays_dda()

#endregion

#region Private methods

        def _calculate_ray_data(self):
            """
            Precomputes Sin and Cos for each ray.
            """
            ray_data = []

            for i in range(FpsSettings.RAY_COUNT):
                offset = -FpsSettings.HALF_FOV + i * FpsSettings.DELTA_ANGLE

                ray_data.append((math.sin(offset), math.cos(offset)))

            return ray_data


        def _cast_rays_dda(self):
            """
            Casts a bunch of rays using a DDA algorithm and stores the results in self.ray_cast_results.
            """
            self.ray_cast_results = []

            player_x = self.player.pos_x
            player_y = self.player.pos_y
            player_angle = self.player.angle
            player_coord = self.player.coordinate ## coordinate of the grid cell of the player
            
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


                    cell = self.world_map[(cell_x, cell_y)]

                    if (cell.type == "wall"):
                        texture = cell.texture_id
                        break

                    if (cell.type == "door"):
                        texture = cell.texture_id
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

                self.ray_cast_results.append((depth, projection_height, texture, offset))

#endregion