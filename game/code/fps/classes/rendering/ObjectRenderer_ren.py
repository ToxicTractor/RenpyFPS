import math
import renpy
from renpy import BrightnessMatrix ## not a real importable module but supresses warning
from renpy.display.transform import Transform
from game.code.fps.classes.rendering.Matrix3DRenderer_ren import Matrix3DRenderer
from game.code.fps.classes.rendering.RaycastingDDARenderer_ren import RaycastingDDARenderer
from game.code.fps.classes.settings.FpsSettings_ren import FpsSettings
from game.code.fps.enums.ECellType_ren import ECellType
from game.code.fps.other.helper_functions_ren import elementwise_add_tuple, ray_index_to_screen_x, screen_x_to_ray_index
from game.code.fps.other.named_tuples_ren import ProjectionResult, Rect, Vector2

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
        """
        Draws a single projection result as one flat, cropped-and-resized
        image blit. Shared by both renderers since sprites are always
        drawn this way regardless of which technique (DDA or matrix) is
        currently rendering the walls. What this blit actually covers
        depends on who built the projection result: a single one-column
        strip for a DDA wall/door face (one call per screen column - see
        RaycastingDDARenderer.prepare_cells), or the sprite's whole image
        in one call for a sprite/shadow (see SpriteObject.get_sprite_projection).
        """
        offset_x, offset_y = offset

        near_depth, far_depth, texture, crop, projection_size, pos, at, cell, hit_direction = projection_result

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

        for sprite_object in self.game.sprite_objects + self.game.npcs:
            projection_result = sprite_object.get_sprite_projection()

            if (projection_result):
                visible_segments = self._clip_projection_to_depth_buffer(projection_result)

                if not visible_segments:
                    continue

                self.objects_to_render.extend(visible_segments)

                shadow_projection = sprite_object.get_shadow_projection()

                if (shadow_projection):
                    ## shadow_projection.near_depth is deliberately forced to
                    ## MAX_DEPTH (see get_shadow_projection) so it always sorts
                    ## behind other objects - that's not its real distance, so
                    ## clip using far_depth (the shadow's true distance) instead
                    self.objects_to_render.extend(self._clip_projection_to_depth_buffer(shadow_projection, occlusion_depth=shadow_projection.far_depth))


    def _clip_projection_to_depth_buffer(self, projection_result, occlusion_depth=None):
        """
        Splits a flat billboard projection (sprite or shadow) into however
        many column-aligned sub-segments are actually nearer than the wall
        depth buffer, so it only draws the part of it that's really
        visible when it's standing partially behind a nearer wall (e.g.
        at a corner), instead of either drawing whole or not at all. Each
        segment reuses the same texture/depth, just cropped to its own
        slice of screen columns.

        occlusion_depth is the real world-space distance to compare
        against the wall depth buffer, defaulting to near_depth - shadows
        pass their actual far_depth instead, since their near_depth is
        deliberately forced to MAX_DEPTH for draw-order purposes and
        isn't their true distance.
        """
        left = projection_result.position.x
        right = left + projection_result.size.x

        if (FpsSettings.USE_DDA_RENDERING):
            start_ray = max(int(left // FpsSettings.PROJECTION_SCALE), 0)
            end_ray = min(int(right // FpsSettings.PROJECTION_SCALE), FpsSettings.RAY_COUNT - 1)
        else:
            start_ray = max(int(screen_x_to_ray_index(left)), 0)
            end_ray = min(int(screen_x_to_ray_index(right)), FpsSettings.RAY_COUNT - 1)

        ## no depth buffer coverage for this sprite's column range (fully
        ## off the raycast FOV) - draw it unclipped rather than dropping it
        if start_ray > end_ray:
            return [projection_result]

        sprite_depth = projection_result.near_depth if occlusion_depth is None else occlusion_depth

        ## run-length encode the visible (nearer-than-wall) ray columns
        ## into contiguous runs, since a sprite is only ever split at wall
        ## depth discontinuities - typically once or twice near a corner,
        ## never per-column
        runs = []
        run_start = None

        for ray_index in range(start_ray, end_ray + 1):
            visible = sprite_depth <= self.depth_buffer[ray_index] + self.OCCLUSION_EPSILON

            if visible:
                if run_start is None:
                    run_start = ray_index
            elif run_start is not None:
                runs.append((run_start, ray_index - 1))
                run_start = None

        if run_start is not None:
            runs.append((run_start, end_ray))

        if not runs:
            return []

        ## fast path: the whole sprite is visible, no need to touch its crop/size
        if runs[0] == (start_ray, end_ray):
            return [projection_result]

        segments = []

        for run_start_ray, run_end_ray in runs:
            if (FpsSettings.USE_DDA_RENDERING):
                run_left_x = run_start_ray * FpsSettings.PROJECTION_SCALE
                run_right_x = (run_end_ray + 1) * FpsSettings.PROJECTION_SCALE
            else:
                run_left_x = ray_index_to_screen_x(run_start_ray)
                run_right_x = ray_index_to_screen_x(run_end_ray + 1)

            seg_left = max(left, run_left_x)
            seg_right = min(right, run_right_x)

            if seg_right - seg_left <= 0.5:
                continue

            u0 = (seg_left - left) / projection_result.size.x
            u1 = (seg_right - left) / projection_result.size.x

            orig_crop = projection_result.crop
            crop_x0 = orig_crop.x + int(u0 * orig_crop.width)
            crop_x1 = orig_crop.x + int(u1 * orig_crop.width)

            segments.append(projection_result._replace(
                crop=Rect(crop_x0, orig_crop.y, max(1, crop_x1 - crop_x0), orig_crop.height),
                size=Vector2(seg_right - seg_left, projection_result.size.y),
                position=Vector2(seg_left, projection_result.position.y),
            ))

        return segments


    def _draw_vertical_door_horizontal_side(self, screen, offset, near_depth, far_depth, crop, pos, cell, st, at):
        """
        Draws the horizontal surface exposed above/below a vertical door
        as it slides open, one screen-column strip at a time - called
        from draw_object_item for each DDA wall/door column that hits a
        vertical door, so unlike that caller's generic blit this one is
        always genuinely a per-column pixel strip.
        """
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
