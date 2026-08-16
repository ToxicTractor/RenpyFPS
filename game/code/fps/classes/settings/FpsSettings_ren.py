import math
from abc import ABC
from renpy import config
from game.code.fps.enums.ENotificationType_ren import ENotificationType

"""renpy
init -100 python:
"""

class FpsSettings(ABC):
    
    ## Rendering
    USE_DDA_RENDERING = False

    ## Screen settings
    Y_OFFSET = -10
    X_OFFSET = -10
    SCREEN_SIZE = config.screen_width + abs(X_OFFSET) * 2, (config.screen_height + abs(Y_OFFSET) * 2) - 274 ## 274 is the height of the UI bar at the buttom of the screen
    SCREEN_WIDTH, SCREEN_HEIGHT = SCREEN_SIZE
    HALF_SCREEN_WIDTH = SCREEN_WIDTH // 2
    HALF_SCREEN_HEIGHT = SCREEN_HEIGHT // 2
    RAW_HALF_SCREEN_HEIGHT = (config.screen_height - 274) // 2 ## doesnt take the offset into account

    ## Raycasting settings
    FOV = math.pi / 3
    HALF_FOV = FOV / 2
    RAY_COUNT = SCREEN_WIDTH // 6 ## determines the width of the vertical slices of the projection. Major performance impact
    HALF_RAY_COUNT = RAY_COUNT // 2
    DELTA_ANGLE = FOV / RAY_COUNT
    MAX_DEPTH = 64

    ## Projection settings
    PROJECTION_DISTANCE = HALF_SCREEN_WIDTH / math.tan(HALF_FOV)
    PROJECTION_SCALE = SCREEN_WIDTH // RAY_COUNT

    ## Texture settings
    TEXTURE_SIZE = 256
    HALF_TEXTURE_SIZE = TEXTURE_SIZE // 2
    DEFAULT_FLOOR_COLOR = "#333"
    DEFAULT_CEILING_COLOR = "#444"

    ## Fade settings
    DEFAULT_FADE_DURATION = 0.5

    ## UI settings
    CROSSHAIR_COLOR = "#fff"
    CROSSHAIR_ALPHA = 0.75

    DEFAULT_NOTIFICATION_COLOR = "#fff"
    DEFAULT_NOTIFICATION_OUTLINES = [(2, "#111", 0, 0)]
    NOTIFICATION_OUTLINES = {
        ENotificationType.Default: DEFAULT_NOTIFICATION_OUTLINES,
        ENotificationType.Positive: [(2, "#111", 0, 0)],
        ENotificationType.Negative: [(2, "#111", 0, 0)],
    }
    NOTIFICATION_COLORS = {
        ENotificationType.Default: DEFAULT_NOTIFICATION_COLOR,
        ENotificationType.Positive: "#cfc",
        ENotificationType.Negative: "#fcc",
    }
