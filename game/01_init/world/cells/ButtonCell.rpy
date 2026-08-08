init python:
    class ButtonCell(CellBase):
        def __init__(self, coord, wall_images, on_images, off_images, sides, is_on=False, mirrored=False):
            super().__init__(coord)

            self.type = ECellType.Button
            self.sides = sides
            self.is_on = is_on
            self.mirrored = mirrored
            self.button_event = GameEvent()

            self.on_audio = "audio/fps/map/buttons/turn_on_switch.ogg"
            self.off_audio = "audio/fps/map/buttons/turn_off_switch.ogg"

            self._wall_images = self._construct_wall_images_dict(wall_images)
            self._on_images = self._construct_overlay_images_dict(on_images)
            self._off_images = self._construct_overlay_images_dict(off_images)

        @property
        def overlay_image(self):
            return self._on_image if self.is_on else self._off_image
        

        def _construct_wall_images_dict(self, wall_images):
            if (isinstance(wall_images, dict)):
                return wall_images
            else:
                return {key:wall_images for key in (FpsConstants.DIRECTIONS)}
        

        def _construct_overlay_images_dict(self, images):
            new_dict = {}
            if (images is None):
                return new_dict

            if (not isinstance(images, dict)):
                images = {key:images for key in (FpsConstants.DIRECTIONS)}

            for side, wall_image in self._wall_images.items():

                if (side not in images):
                    continue

                overlay_image = self._apply_image_flip(images[side], side)

                new_dict[side] = Composite(
                    (FpsSettings.TEXTURE_SIZE, FpsSettings.TEXTURE_SIZE),
                    (0, 0), wall_image,
                    (0, 0), overlay_image)

            return new_dict

        
        def _apply_image_flip(self, image, direction):

            if ((direction in (EDirection.Right, EDirection.Up) and not self.mirrored) or
                (direction in (EDirection.Left, EDirection.Down) and self.mirrored)):
                return Transform(image, xzoom=-1.0)
            else:
                return image


        def get_texture(self, side):

            if (side in self.sides):
                return (self._on_images.get(side) if self.is_on else self._off_images.get(side)), 1.0
            else:
                return self._wall_images.get(side), 1.0


        def is_interactable(self, side):

            if (side is None):
                return False

            return side in self.sides


        def interact(self):

            self.is_on = not self.is_on

            renpy.play(self.on_audio if self.is_on else self.off_audio)

            self.button_event.invoke()


        def is_button_side(self, hit_direction):
            
            if (self.sides is None):
                return False

            return hit_direction in self.sides


define FPS_BUTTON_TEXTURES = {
    0: Image("images/fps/textures/buttons/switch_01_on.png"),
    1: Image("images/fps/textures/buttons/switch_01_off.png"),
}