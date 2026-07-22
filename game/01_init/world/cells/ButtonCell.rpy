init python:
    class ButtonCell(CellBase):
        def __init__(self, coordinate, wall_image, on_image, off_image, sides=[], is_on=False):
            super().__init__(coordinate)

            self.type = "button"
            self.images = [wall_image]
            self.image_ratios = [1]
            self.off_image = off_image
            self.on_image = on_image
            self.sides = sides
            self.is_on = is_on
            self.button_event = GameEvent()

            self.on_audio = "audio/fps/map/buttons/turn_on_switch.ogg"
            self.off_audio = "audio/fps/map/buttons/turn_off_switch.ogg"

        def blocks_movement(self, x, y, radius):
            return True
        
        @property
        def overlay_image(self):
            return self.on_image if self.is_on else self.off_image

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