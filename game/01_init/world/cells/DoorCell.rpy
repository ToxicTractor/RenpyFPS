init python:
    class DoorCell(CellBase):
        def __init__(self, coordinate, texture_id, offset=0.5, orientation="horizontal"):
            super().__init__(coordinate)

            self.type = "door"
            self.texture_id = texture_id
            self.offset = offset
            self.orientation = orientation
            self.open_amount = 0.0

        
        def intersect(self, player_x, player_y, ray_dx, ray_dy):
            
            if (self.orientation == "horizontal"):
                pass
            elif(self.orientation == "vertical"):
                pass


define FPS_DOOR_TEXTURES = {
    0: Image("images/fps/textures/doors/metal_door.png", oversample=4),
    1: Image("images/fps/textures/doors/blue_door.png", oversample=4)
}