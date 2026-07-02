init python:
    class WallCell(CellBase):
        def __init__(self, coordinate, image):
            super().__init__(coordinate)

            self.type = "wall"
            self.image = image
        
        def blocks_movement(self, x, y, radius):
            return True


define FPS_WALL_TEXTURES = {
    1: Image("images/fps/textures/walls/stone_wall_01.jpg", oversample=4),
    2: Image("images/fps/textures/walls/stone_wall_02.png", oversample=1.875),
    3: Image("images/fps/textures/walls/stone_wall_03.png", oversample=1.875),
    4: Image("images/fps/textures/walls/stone_wall_04.png", oversample=1.875),
    5: Image("images/fps/textures/walls/wood_wall_01.png", oversample=1.875),
    6: Image("images/fps/textures/walls/stone_wall_05.png", oversample=1.875),
}
