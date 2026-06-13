init python:
    
    def load_map(map_path):

        img = renpy.load_surface(map_path)
        rows, cols = renpy.image_size(map_path)

        data = [[None for _ in range(cols)] for _ in range(rows)]

        for y in range(cols):
            for x in range(rows):
                
                ## note that y first is correct, we select first the collumn then the row when accessing a 2D array
                data[y][x] = img.get_at((x, y))[3] ## use alpha value to create map for now

        return data
                
