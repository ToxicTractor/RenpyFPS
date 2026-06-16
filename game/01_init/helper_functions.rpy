init python:
    
    def load_map(map_path):

        img = renpy.load_surface(map_path)
        rows, cols = renpy.image_size(map_path)

        data = [[None for _ in range(cols)] for _ in range(rows)]
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
                    data[y][x] = 0
                    continue

                ## value of the red channel determines the wall type
                data[y][x] = img.get_at((x, y))[0]

        return data, player_start_pos
                
