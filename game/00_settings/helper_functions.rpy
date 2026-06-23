init -100 python:
    import struct
    def load_map(map_path):

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
                

    def get_image_size(image):
        r = renpy.render(image, 0, 0, 0, 0)
        size = r.get_size()
        return int(size[0]), int(size[1])


    ## Clamps a value between min_value and max_value
    def clamp(value, min_value, max_value):
        if (min_value > max_value):
            raise Exception("Parameter 'min_value' cannot be larger than 'max_value'!")
        return max(min_value, min(value, max_value))


    def lerp(a, b, t, clamp_value = True):
        ## Linear interpolation between a and b by a factor t, by default clamps the result between a and b
        result = (t * b) + ((1 - t) * a)

        min_value = (a if a < b else b)
        max_value = (b if b > a else a)

        return (clamp(result, min_value, max_value) if clamp_value else result)
    

    ## Inverse linear interpolation between a and b from a value, by default clamps result between 0 and 1
    def inverse_lerp(a, b, value, clamp_value = True):
        result = (value - a) / (b - a)
        return (clamp(result, 0, 1) if clamp_value else result)

    
    ## inverse sqrt approximation
    ## https://ajcr.net/fast-inverse-square-root-python/
    def isqrt(number):
        threehalfs = 1.5
        x2 = number * 0.5
        y = number
        
        packed_y = struct.pack('f', y)
        i = struct.unpack('i', packed_y)[0]
        i = 0x5f3759df - (i >> 1)
        packed_i = struct.pack('i', i)
        y = struct.unpack('f', packed_i)[0]
        
        y = y * (threehalfs - (x2 * y * y))
        return y
    
    ## normalize vector using inverse sqrt approximation
    def normalize(x, y):
        dot = x ** 2 + y ** 2
        inv_length = isqrt(dot)
        return (x * inv_length, y * inv_length)