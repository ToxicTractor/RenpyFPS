init python:
    class WallCell(CellBase):
        def __init__(self, coord, images, overlay_images=None):
            super().__init__(coord)

            self.type = ECellType.Wall
            self._images = self._construct_wall_images_dict(images)
            self._overlay_images = self._construct_overlay_images_dict(overlay_images)


        def _construct_wall_images_dict(self, images):
            if (isinstance(images, dict)):
                return images
            else:
                return {key:images for key in (FpsConstants.DIRECTIONS)}

        def _construct_overlay_images_dict(self, images):
            new_dict = {}
            if (images is None):
                return new_dict
            
            if (not isinstance(images, dict)):
                images = {key:images for key in (FpsConstants.DIRECTIONS)}

            for side, wall_image in self._images.items():

                if (side not in images):
                    continue

                new_dict[side] = Composite(
                    (FpsSettings.TEXTURE_SIZE, FpsSettings.TEXTURE_SIZE),
                    (0, 0), wall_image,
                    (0, 0), images[side])

            return new_dict


        def get_texture(self, side):
            if (side in self._overlay_images):
                return self._overlay_images.get(side), 1.0
            else:
                return self._images.get(side), 1.0


define FPS_WALL_TEXTURES = {
    1: Image("images/fps/textures/walls/stone_wall_01.jpg", oversample=4),
    2: Image("images/fps/textures/walls/stone_wall_02.png", oversample=1.875),
    3: Image("images/fps/textures/walls/stone_wall_03.png", oversample=1.875),
    4: Image("images/fps/textures/walls/stone_wall_04.png", oversample=1.875),
    5: Image("images/fps/textures/walls/wood_wall_01.png", oversample=1.875),
    6: Image("images/fps/textures/walls/stone_wall_05.png", oversample=1.875),
}

define FPS_WALL_OVERLAY_TEXTURES = {
    0: Image("images/fps/textures/walls/overlays/get_a_job.png")
}