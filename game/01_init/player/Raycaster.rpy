init python:
    class Raycaster():
        def __init__(self, player, map):
            self.player = player
            self.world_map = map.world_map
            self._ray_data = self._calculate_ray_data()


#region Public methods

        def cast_rays_dda(self):
            """
            Casts a bunch of rays using a DDA algorithm and return the results. Used for rendering.
            """
            raycast_results = []

            player_x = self.player.pos_x
            player_y = self.player.pos_y
            player_angle = self.player.angle
            
            sin_player_angle = math.sin(player_angle)
            cos_player_angle = math.cos(player_angle)

            for sin_offset, cos_offset in self._ray_data:
                ## defaults
                texture_index = 0
                hit_cell = None
                hit_side = None
                
                ## calculate sin and cos using our precomputed offsets
                ray_direction_x = cos_player_angle * cos_offset - sin_player_angle * sin_offset
                ray_direction_y = sin_player_angle * cos_offset + cos_player_angle * sin_offset

                ## get all traversed cells
                traversed_cells = self.trace_cells(self.player.pos, ray_dir=(ray_direction_x, ray_direction_y))

                ## figure out where we hit something
                for cell, depth, cell_side in traversed_cells:
                    
                    if (cell.type == "empty"):
                        continue

                    if (cell.type == "door"):
                        hit = cell.intersect(player_x, player_y, ray_direction_x, ray_direction_y)
                        
                        if (hit is None):
                            continue
                        
                        depth, offset, texture_index = hit
                        hit_cell = cell
                        hit_side = cell_side
                        break

                    if (cell.type in ("wall", "button")):
                        hit_cell = cell
                        hit_side = cell_side

                        if (hit_side in ("east", "west")):
                            offset = player_y + depth * ray_direction_y
                        elif (hit_side in ("north", "south")):
                            offset = player_x + depth * ray_direction_x

                        break

                offset -= math.floor(offset)

                ## eliminate fisheye effect
                depth *= cos_offset

                ## calculate projection height
                projection_height = FpsSettings.PROJECTION_DISTANCE / (depth + 0.0001)

                raycast_results.append((depth, projection_height, hit_cell, offset, texture_index, hit_side))
            
            return raycast_results


        def trace_cells(self, pos, *, angle=None, ray_dir=None, distance=FpsSettings.MAX_DEPTH):
            ## Returns a list of all traversed cells. Continues until we reach distance or we leave the bounds of the map. Either angle or ray_dir must be given. 
            cells = []

            ## split position into components
            pos_x, pos_y = pos

            ## get starting cell coord
            cell_x = int(pos[0])
            cell_y = int(pos[1])

            ## calculate ray direction if not already given
            if (ray_dir is None):
                ray_direction_x = math.cos(angle)
                ray_direction_y = math.sin(angle)
            else:
                ray_direction_x, ray_direction_y = ray_dir

            ## calculate delta distance
            delta_distance_x = float('inf') if ray_direction_x == 0 else abs(1 / ray_direction_x)
            delta_distance_y = float('inf') if ray_direction_y == 0 else abs(1 / ray_direction_y)

            ## determine step direction
            step_x = -1 if ray_direction_x < 0 else 1
            step_y = -1 if ray_direction_y < 0 else 1

            ## calculate initial side distances
            if (ray_direction_x < 0):
                side_distance_x = (pos_x - cell_x) * delta_distance_x
            else:
                side_distance_x = (cell_x + 1 - pos_x) * delta_distance_x

            if (ray_direction_y < 0):
                side_distance_y = (pos_y - cell_y) * delta_distance_y
            else:
                side_distance_y = (cell_y + 1 - pos_y) * delta_distance_y
            
            depth = 0

            while depth < distance:

                ## figure out which side of the cell we hit
                if (side_distance_x < side_distance_y):
                    depth = side_distance_x
                    side_distance_x += delta_distance_x
                    cell_x += step_x
                    cell_side = "east" if step_x < 0 else "west"
                else:
                    depth = side_distance_y
                    side_distance_y += delta_distance_y
                    cell_y += step_y
                    cell_side = "south" if step_y < 0 else "north"

                ## try to get the cell
                cell = self.world_map.get((cell_x, cell_y))
                
                ## if the cell doesn't exist, we have left the map so we break the loop
                if (cell is None):
                    break

                cells.append((cell, depth, cell_side))

            return cells
        
        
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

#endregion