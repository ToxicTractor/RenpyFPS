import math
from game.code.fps.classes.settings.FpsSettings_ren import FpsSettings
from game.code.fps.enums.ECellType_ren import ECellType
from game.code.fps.enums.EDirection_ren import EDirection
from game.code.fps.other.named_tuples_ren import RaycastHitDDA
from game.code.fps.other.named_tuples_ren import CellTraceEntry

"""renpy
init python:
"""

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

        player_x = self.player.pos.x
        player_y = self.player.pos.y
        player_angle = self.player.angle

        sin_player_angle = math.sin(player_angle)
        cos_player_angle = math.cos(player_angle)

        world_map = self.world_map
        max_depth = FpsSettings.MAX_DEPTH

        start_cell_x = int(player_x)
        start_cell_y = int(player_y)

        for sin_offset, cos_offset in self._ray_data:
            ## list of hits for the ray
            ray_hits = []

            ## calculate sin and cos using our precomputed offsets
            ray_direction_x = cos_player_angle * cos_offset - sin_player_angle * sin_offset
            ray_direction_y = sin_player_angle * cos_offset + cos_player_angle * sin_offset

            ## calculate delta distance
            delta_distance_x = float('inf') if ray_direction_x == 0 else abs(1 / ray_direction_x)
            delta_distance_y = float('inf') if ray_direction_y == 0 else abs(1 / ray_direction_y)

            ## determine step direction
            step_x = -1 if ray_direction_x < 0 else 1
            step_y = -1 if ray_direction_y < 0 else 1

            cell_x = start_cell_x
            cell_y = start_cell_y

            ## calculate initial side distances
            if (ray_direction_x < 0):
                side_distance_x = (player_x - cell_x) * delta_distance_x
            else:
                side_distance_x = (cell_x + 1 - player_x) * delta_distance_x

            if (ray_direction_y < 0):
                side_distance_y = (player_y - cell_y) * delta_distance_y
            else:
                side_distance_y = (cell_y + 1 - player_y) * delta_distance_y

            depth = 0
            cell_side = EDirection.NONE
            cell = world_map[(cell_x, cell_y)]

            ## walk and interpret cells in a single pass, stopping the DDA the moment we know we've hit something opaque
            while True:

                if (cell.type == ECellType.Empty):
                    pass

                elif (cell.type in (ECellType.HorizontalDoor, ECellType.VerticalDoor)):

                    if not (cell.type == ECellType.VerticalDoor and cell.open_amount == 1.0):

                        hit = cell.ray_intersect(player_x, player_y, ray_direction_x, ray_direction_y)

                        if (hit is not None):
                            near_depth, far_depth, offset, hit_side = hit

                            ## we multiply depth by cos_offset to eliminate fisheye effect
                            ray_hits.append(RaycastHitDDA(near_depth * cos_offset, far_depth * cos_offset, cell, offset, hit_side))

                            if (cell.type == ECellType.HorizontalDoor or cell.open_amount == 0):
                                break

                elif (cell.type in (ECellType.Wall, ECellType.Button)):

                    if (cell_side in (EDirection.Right, EDirection.Left)):
                        offset = (player_y + depth * ray_direction_y) % 1.0
                    elif (cell_side in (EDirection.Up, EDirection.Down)):
                        offset = (player_x + depth * ray_direction_x) % 1.0

                    ## we multiply depth by cos_offset to eliminate fisheye effect
                    ray_hits.append(RaycastHitDDA(depth * cos_offset, 0, cell, offset, cell_side))
                    break

                if not (depth < max_depth):
                    break

                ## step to the next cell
                if (side_distance_x < side_distance_y):
                    depth = side_distance_x
                    side_distance_x += delta_distance_x
                    cell_x += step_x
                    cell_side = EDirection.Right if step_x < 0 else EDirection.Left
                else:
                    depth = side_distance_y
                    side_distance_y += delta_distance_y
                    cell_y += step_y
                    cell_side = EDirection.Down if step_y < 0 else EDirection.Up

                cell = world_map.get((cell_x, cell_y))

                ## if the cell doesn't exist, we have left the map so we stop
                if (cell is None):
                    break

            raycast_results.append(ray_hits)

        return raycast_results


    def trace_cells(self, pos, *, angle=None, ray_dir=None, distance=FpsSettings.MAX_DEPTH, stop_predicate=None):
        ## Returns a list of all traversed cells. Continues until we reach distance, we leave the bounds of the map, or stop_predicate(entry) returns True for a traversed cell. Either angle or ray_dir must be given.
        entries = []
        first_hit_distance = None

        ## split position into components
        pos_x, pos_y = pos

        ## get starting cell coord
        cell_x = int(pos[0])
        cell_y = int(pos[1])

        ## we always want to append the starting cell
        entries.append(CellTraceEntry(self.world_map[(cell_x, cell_y)], 0, EDirection.NONE))
        ## if we are inside of a cell that is not "empty", set first_hit_distance
        if (entries[0].cell.type != ECellType.Empty):
            first_hit_distance = 0

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
                cell_side = EDirection.Right if step_x < 0 else EDirection.Left
            else:
                depth = side_distance_y
                side_distance_y += delta_distance_y
                cell_y += step_y
                cell_side = EDirection.Down if step_y < 0 else EDirection.Up

            ## try to get the cell
            cell = self.world_map.get((cell_x, cell_y))

            ## if the cell doesn't exist, we have left the map so we break the loop
            if (cell is None):
                break

            if (cell.type != ECellType.Empty and first_hit_distance is None):
                first_hit_distance = depth

            entry = CellTraceEntry(cell, depth, cell_side)
            entries.append(entry)

            if (stop_predicate is not None and stop_predicate(entry)):
                break

        return entries, (first_hit_distance if first_hit_distance else 0)


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
