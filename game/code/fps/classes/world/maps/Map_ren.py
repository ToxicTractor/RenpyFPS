from abc import ABC
from game.code.fps.classes.world.cells.EmptyCell_ren import EmptyCell
from game.code.fps.classes.world.cells.WallCell_ren import WallCell
from game.code.fps.enums.ECellType_ren import ECellType
from game.code.fps.other.named_tuples_ren import Vector2

"""renpy
init python:
"""

class Map(ABC): ## abstract class to enforce inheritance for maps
    def __init__(self, path, debug_scale):
        self.debug_scale = debug_scale

        self.world_map = {}

        self.is_inside = False
        self.sky_image = None
        self.floor_image = None

        self.music_tracks = []

        map_data, self.player_start_pos = self._load_map(path)
        self.width = len(map_data[0])
        self.height = len(map_data)

        self._create_map(map_data)

#region Public methods

    def update(self, delta_time):
        for cell in self.world_map.values():
            cell.update(delta_time)


    def draw_2d(self, canvas):    
        """
        Draws a 2D representation of the map to the screen. Intended for debugging only.
        """
        for coord, cell in self.world_map.items():

            x, y = coord

            if (cell.type == ECellType.Empty):
                continue

            if (cell.type == ECellType.Wall):
                canvas.rect("#fff8", (x * self.debug_scale, y * self.debug_scale, self.debug_scale, self.debug_scale), 2)

            if (cell.type == ECellType.Button):
                canvas.rect("#0f0" if cell.is_on else "#f00", (x * self.debug_scale, y * self.debug_scale, self.debug_scale, self.debug_scale), 2)

            if (cell.type == ECellType.HorizontalDoor):
                min_x, min_y, max_x, max_y = cell.get_aabb()
                x = min_x * self.debug_scale
                y = min_y * self.debug_scale
                width = (max_x - min_x) * self.debug_scale
                height = (max_y - min_y) * self.debug_scale
                canvas.rect("#0f0" if not cell.is_locked else "#f00", (x, y, width, height), 2)

#endregion

#region Private methods

    def _create_map(self, map_data):
        """
        Creates the map based on the map_data provided.
        """

        for y, row in enumerate(map_data):
            for x, value in enumerate(row):

                ## if the value is greater than 0 we add the value to the world_map
                ## 0 is empty space
                if (value > 0):
                    self.world_map[(x, y)] = WallCell((x, y), FPS_WALL_TEXTURES[value])
                else:
                    self.world_map[(x, y)] = EmptyCell((x, y))



    def _load_map(self, map_path):
        """
        Loads an image at the specified path and returns 2D array of map_data and the starting position of the player.
        """

        img = renpy.load_surface(map_path)
        rows, cols = renpy.image_size(map_path)

        data = [[0 for _ in range(cols)] for _ in range(rows)]

        player_start_pos = Vector2(0, 0)

        for y in range(cols):
            for x in range(rows):

                ## note that y first is correct, we select first the collumn then the row when accessing a 2D array
                r, g, b, a = img.get_at((x, y))

                ## green value of 255 indicates player starting position
                ## adding half to spawn in the center of the cell
                if (g == 255):
                    player_start_pos = Vector2(x + 0.5, y + 0.5)

                ## if the alpha channel is not at 255, it counts as an empty square
                if (a != 255):
                    continue

                ## value of the red channel determines the wall type
                data[y][x] = img.get_at((x, y))[0]

        return data, player_start_pos

#endregion
