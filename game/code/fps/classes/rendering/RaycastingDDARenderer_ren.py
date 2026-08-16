from game.code.fps.classes.settings.FpsSettings_ren import FpsSettings
from game.code.fps.enums.ECellType_ren import ECellType
from game.code.fps.enums.EDirection_ren import EDirection
from game.code.fps.other.named_tuples_ren import ProjectionResult, Vector2

"""renpy
init python:
"""

class RaycastingDDARenderer():
    def __init__(self, object_renderer):
        self.object_renderer = object_renderer
        self.game = object_renderer.game

#region Public methods

    def update(self, raycast_hits):

        self.__prepare_cells(raycast_hits)


    def draw(self, screen, offset, st):
        """
        Draws objects to the screen. Objects inclued walls, NPCs, static objets, etc.
        """
        ## sort the list by depth to make sure we draw element in the correct order
        objects_to_render = sorted(self.object_renderer.objects_to_render, key=lambda p: p.near_depth, reverse=True)

        for projection_result in objects_to_render:
            self.object_renderer.draw_object_item(screen, offset, st, projection_result)

#endregion

#region Private methods

    def __prepare_cells(self, raycast_hits):
        for ray_index, hits in enumerate(raycast_hits):
            for hit in hits:
                if (hit.cell.type == ECellType.Empty):
                    continue

                texture, texture_size_ratio = hit.cell.get_texture(hit.side)

                crop_x = int(hit.offset * (FpsSettings.TEXTURE_SIZE * texture_size_ratio - 1))
                crop_y = 0
                crop_width = 1
                crop_height = FpsSettings.TEXTURE_SIZE

                projection_height = FpsSettings.PROJECTION_DISTANCE / (hit.near_depth + 0.0001)
                height = int(projection_height)

                pos_x = ray_index * FpsSettings.PROJECTION_SCALE
                pos_y = FpsSettings.HALF_SCREEN_HEIGHT - projection_height // 2

                if (hit.cell.type is ECellType.VerticalDoor):
                    height = int(projection_height * (1.0 - hit.cell.open_amount))
                    y_offset = int(projection_height - height)
                    crop_height = int(crop_height * (1.0 - hit.cell.open_amount))

                    if (hit.cell.open_direction is EDirection.Down):
                        pos_y += y_offset
                    elif (hit.cell.open_direction is EDirection.Up):
                        crop_y = int(FpsSettings.TEXTURE_SIZE * hit.cell.open_amount)

                projection_result = ProjectionResult(
                    hit.near_depth,
                    hit.far_depth,
                    texture,
                    (crop_x, crop_y, crop_width, crop_height),
                    (FpsSettings.PROJECTION_SCALE, height),
                    Vector2(pos_x, pos_y),
                    0,
                    hit.cell,
                    hit.side
                )

                self.object_renderer.objects_to_render.append(projection_result)

#endregion
