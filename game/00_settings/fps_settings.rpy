init -100 python:
    import math

    class FpsSettings():
        
        ## Screen settings
        SCREEN_SIZE = config.screen_width, config.screen_height
        SCREEN_WIDTH, SCREEN_HEIGHT = SCREEN_SIZE
        HALF_SCREEN_WIDTH = SCREEN_WIDTH // 2
        HALF_SCREEN_HEIGHT = SCREEN_HEIGHT // 2

        ## Raycasting settings
        FOV = math.pi / 3
        HALF_FOV = FOV / 2
        RAY_COUNT = SCREEN_WIDTH // 4
        HALF_RAY_COUNT = RAY_COUNT // 2
        DELTA_ANGLE = FOV / RAY_COUNT
        MAX_DEPTH = 64

        ## Projection settings
        PROJECTION_DISTANCE = HALF_SCREEN_WIDTH / math.tan(HALF_FOV)
        PROJECTION_SCALE = SCREEN_WIDTH // RAY_COUNT

        ## Texture settings
        TEXTURE_SIZE = 256
        HALF_TEXTURE_SIZE = TEXTURE_SIZE // 2
