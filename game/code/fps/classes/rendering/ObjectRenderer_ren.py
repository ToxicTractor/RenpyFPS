import math
import renpy
from renpy import BrightnessMatrix ## not a real importable module but supresses warning
from renpy.display.transform import Transform
from game.code.fps.classes.rendering.Matrix3DRenderer_ren import Matrix3DRenderer
from game.code.fps.classes.rendering.RaycastingDDARenderer_ren import RaycastingDDARenderer
from game.code.fps.classes.settings.FpsSettings_ren import FpsSettings
from game.code.fps.enums.ECellType_ren import ECellType
from game.code.fps.other.helper_functions_ren import elementwise_add_tuple
from game.code.fps.other.named_tuples_ren import ProjectionResult

"""renpy
init python:
"""

class ObjectRenderer():
    OCCLUSION_EPSILON = 0.05 ## avoids flicker when a sprite sits right at a wall's depth

    def __init__(self, game, player, map):
        self.game = game
        self.player = player

        self.is_inside = map.is_inside
        self.floor_image = map.floor_image
        self.sky_image = map.sky_image
        self.sky_offset = 0

        self.objects_to_render = []
        self.depth_buffer = [float("inf") for _ in range(FpsSettings.RAY_COUNT)]
        self.raycast_hits = []

        self.dda_renderer = RaycastingDDARenderer(self)
        self.matrix_renderer = Matrix3DRenderer(self)

#region Public methods

    def update(self, delta_time):
        self.objects_to_render = []
        self.raycast_hits = raycast_hits = self.game.raycaster.cast_rays_dda()

        self._build_depth_buffer(raycast_hits)

        if (FpsSettings.USE_DDA_RENDERING):
            self.dda_renderer.update(raycast_hits)
        else:
            pass
            ## no update loop in matrix renderer yet 

        self._prepare_sprite_objects()


    def draw(self, screen, st):
        offset = elementwise_add_tuple(self.player.sway_offset, (FpsSettings.X_OFFSET, FpsSettings.Y_OFFSET))

        self._draw_sky(screen, offset)
        self._draw_floor(screen, offset)

        if (FpsSettings.USE_DDA_RENDERING):
            self.dda_renderer.draw(screen, offset, st)
        else:
            self.matrix_renderer.draw(screen, offset, st)


    def draw_object_item(self, screen, offset, st, projection_result):

        offset_x, offset_y = offset

        near_depth, far_depth, texture, crop, projection_size, pos, at, cell, _ = projection_result

        if (cell is not None and cell.type == ECellType.VerticalDoor):
            self._draw_vertical_door_horizontal_side(screen, offset, near_depth, far_depth, crop, pos, cell, st, at)

        item_transform = Transform(
            texture,
            crop=crop,
            size=projection_size,
            matrixcolor=BrightnessMatrix(-(near_depth / FpsSettings.MAX_DEPTH))
        )

        item_render = renpy.render(item_transform, int(projection_size[0]), int(projection_size[1]), st, at)

        screen.blit(item_render, (pos.x + offset_x, pos.y + offset_y))

#endregion

#region Private methods

    def _build_depth_buffer(self, raycast_hits):
        self.depth_buffer = [float("inf") for _ in range(FpsSettings.RAY_COUNT)]

        for ray_index, hits in enumerate(raycast_hits):
            for hit in hits:
                if (hit.cell.type == ECellType.VerticalDoor and hit.cell.open_amount > 0.0):
                    continue

                self.depth_buffer[ray_index] = hit.near_depth
                break


    def _prepare_sprite_objects(self):
        if (FpsSettings.USE_DDA_RENDERING):
            self.dda_renderer.prepare_sprite_objects(self.game.sprite_objects, self.game.npcs)
        else:
            self.matrix_renderer.prepare_sprite_objects(self.game.sprite_objects, self.game.npcs)


    def _draw_vertical_door_horizontal_side(self, screen, offset, near_depth, far_depth, crop, pos, cell, st, at):

        ## if the door is less than half open, we cannot see the surface so we just return.
        if (cell.open_amount < 0.5):
            return

        offset_x, offset_y = offset

        z = cell.get_horizontal_side_z()

        camera_z = 0.5

        near_y = (FpsSettings.HALF_SCREEN_HEIGHT + (camera_z - z) * FpsSettings.PROJECTION_DISTANCE / near_depth)
        far_y = (FpsSettings.HALF_SCREEN_HEIGHT + (camera_z - z) * FpsSettings.PROJECTION_DISTANCE / far_depth)

        top = int(min(near_y, far_y))
        bottom = int(max(near_y, far_y))

        height = bottom - top

        if height <= 0:
            return

        door_side_transform = Transform(
            cell.plane_texture,
            crop=crop,
            size=(FpsSettings.PROJECTION_SCALE, height),
            matrixcolor=BrightnessMatrix(-(near_depth / FpsSettings.MAX_DEPTH))
        )

        door_side_render = renpy.render(door_side_transform, FpsSettings.PROJECTION_SCALE, height, st, at)

        screen.blit(door_side_render, (pos.x + offset_x, top + offset_y))


    def _draw_floor(self, screen, offset):
        """
        Draws the floor to the screen.
        """
        offset_x, offset_y = offset

        ## we simply draw a box on the lower half of the screen for the floor
        floor_render = renpy.render(self.floor_image, FpsSettings.SCREEN_WIDTH, FpsSettings.HALF_SCREEN_HEIGHT, 0, 0)

        screen.blit(floor_render, (0 + offset_x, FpsSettings.HALF_SCREEN_HEIGHT + offset_y))


    def _draw_sky(self, screen, offset):
        """
        Draws the sky or ceiling to the screen.
        """
        offset_x, offset_y = offset

        ## if we are inside we just draw a box for the roof
        if (self.is_inside):

            ceiling_render = renpy.render(self.sky_image, FpsSettings.SCREEN_WIDTH, FpsSettings.HALF_SCREEN_HEIGHT, 0, 0)

            screen.blit(ceiling_render, (0 + offset_x, 0 + offset_y))

        ## if we are outside we draw a scrolling texture that repeat to simulate the sky
        else:

            sky_render = renpy.render(self.sky_image, FpsSettings.SCREEN_WIDTH, FpsSettings.SCREEN_HEIGHT, 0, 0)

            tile_width = FpsSettings.SCREEN_WIDTH
            sky_offset = (self.player.angle / (2 * math.pi) * tile_width) % tile_width

            x = -sky_offset + offset_x

            screen.blit(sky_render, (x, offset_y))
            screen.blit(sky_render, (x + tile_width, offset_y))

#endregion
