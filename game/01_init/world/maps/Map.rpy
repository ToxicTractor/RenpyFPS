init python:
    class Map(ABC): ## abstract class to enforce inheritance for maps
        def __init__(self, path, debug_scale):
            self.debug_scale = debug_scale

            self.world_map = {}
            self.nav_map = []
            
            self.is_inside = False
            self.sky_image = None
            self.floor_image = None

            self.music_tracks = []

            map_data, self.player_start_pos = self._load_map(path)
            self._create_map(map_data)

#region Public methods

        def draw_2d(self, canvas):    
            """
            Draws a 2D representation of the map to the screen. Intended for debugging only.
            """
            for coordinate, cell in self.world_map.items():
                
                x, y = coordinate

                if (cell.type == "empty"):
                    continue
                
                if (cell.type == "wall"):
                    canvas.rect("#444", (x * self.debug_scale, y * self.debug_scale, self.debug_scale, self.debug_scale), 2)

                if (cell.type == "door"):
                    canvas.rect("#0f0" if cell.open_amount >= 1.0 else "#f00", (x * self.debug_scale, y * self.debug_scale, self.debug_scale, self.debug_scale), 2)


        def is_blocking(self, x, y, radius):

            cell = self.world_map[(int(x), int(y))]

            return cell.blocks_movement(x, y, radius)

#endregion

#region Private methods

        def _create_map(self, map_data):
            """
            Creates the map based on the map_data provided.
            """

            ## Create 2D array of the same size as the map that we use for navigation
            self.nav_map = [[0 for _ in range(len(map_data[0]))] for _ in range(len(map_data))]

            for y, row in enumerate(map_data):
                for x, value in enumerate(row):
                    
                    ## if the value is greater than 0 we add the value to the world_map
                    ## 0 is empty space
                    if (value > 0):
                        self.world_map[(x, y)] = WallCell((x, y), FPS_WALL_TEXTURES[value])
                    else:
                        self.world_map[(x, y)] = EmptyCell((x, y))
                    
                    ## add the walls to the navigation map
                    self.nav_map[y][x] = 0 if value < 1 else 1


        def _load_map(self, map_path):
            """
            Loads an image at the specified path and returns 2D array of map_data and the starting position of the player.
            """

            img = renpy.load_surface(map_path)
            rows, cols = renpy.image_size(map_path)

            data = [[0 for _ in range(cols)] for _ in range(rows)]

            player_start_pos = 0, 0

            for y in range(cols):
                for x in range(rows):
                    
                    ## note that y first is correct, we select first the collumn then the row when accessing a 2D array
                    r, g, b, a = img.get_at((x, y))
                    
                    ## green value of 255 indicates player starting position
                    ## adding half to spawn in the center of the cell
                    if (g == 255):
                        player_start_pos = x + 0.5, y + 0.5

                    ## if the alpha channel is not at 255, it counts as an empty square
                    if (a != 255):
                        continue

                    ## value of the red channel determines the wall type
                    data[y][x] = img.get_at((x, y))[0]

            return data, player_start_pos

#endregion