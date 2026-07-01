init python:
    class WallCell(CellBase):
        def __init__(self, coordinate, texture_id):
            super().__init__(coordinate)

            self.type = "wall"
            self.texture_id = texture_id


define FPS_WALL_TEXTURES = {
    1: Image("images/fps/textures/walls/stone_wall_01.jpg", oversample=4),
    2: Image("images/fps/textures/walls/stone_wall_02.png", oversample=1.875),
    3: Image("images/fps/textures/walls/stone_wall_03.png", oversample=1.875),
    4: Image("images/fps/textures/walls/stone_wall_04.png", oversample=1.875),
    5: Image("images/fps/textures/walls/wood_wall_01.png", oversample=1.875),
    6: Image("images/fps/textures/walls/stone_wall_05.png", oversample=1.875),
    254: Image("images/fps/textures/doors/metal_door.png", oversample=0.25),
    255: Image("images/fps/textures/doors/blue_door.png", oversample=0.25)
}
