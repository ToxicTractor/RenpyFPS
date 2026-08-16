init python:
    class RaycastingDDARenderer():
        def __init__(self, object_renderer):
            self.object_renderer = object_renderer
            self.game = object_renderer.game

#region Public methods

        def prepare_cells(self, raycast_hits):
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


        def draw(self, screen, offset, st):
            """
            Draws objects to the screen. Objects inclued walls, NPCs, static objets, etc.
            """
            ## sort the list by depth to make sure we draw element in the correct order
            objects_to_render = sorted(self.object_renderer.objects_to_render, key=lambda p: p.near_depth, reverse=True)

            for projection_result in objects_to_render:
                self.draw_object_item(screen, offset, st, projection_result)

#endregion

#region Internal methods

        def draw_object_item(self, screen, offset, st, projection_result):
            offset_x, offset_y = offset

            near_depth, far_depth, texture, crop, projection_size, pos, at, cell, hit_direction = projection_result

            if (cell is not None and cell.type == ECellType.VerticalDoor):
                self._draw_vertical_door_horizontal_side(screen, offset, near_depth, far_depth, crop, pos, cell, st, at)

            pixel_slice = Transform(
                texture,
                crop=crop,
                size=projection_size,
                matrixcolor=BrightnessMatrix(-(near_depth / FpsSettings.MAX_DEPTH))
            )

            slice_render = renpy.render(pixel_slice, int(projection_size[0]), int(projection_size[1]), st, at)

            screen.blit(slice_render, (pos.x + offset_x, pos.y + offset_y))


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

            pixel_slice = Transform(
                cell.plane_texture,
                crop=crop,
                size=(FpsSettings.PROJECTION_SCALE, height),
                matrixcolor=BrightnessMatrix(-(near_depth / FpsSettings.MAX_DEPTH))
            )

            slice_render = renpy.render(pixel_slice, FpsSettings.PROJECTION_SCALE, height, st, at)

            screen.blit(slice_render, (pos.x + offset_x, top + offset_y))

#endregion
