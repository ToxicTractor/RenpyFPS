init python:
    class Map01(Map):
        def __init__(self, debug_scale=1.0):
            super().__init__(
                "images/fps/maps/map.png", 
                debug_scale
            )

            self.floor_image = Solid("#333")
            self.sky_image = self.sky_image = Transform(
                Image("images/fps/textures/skies/sky_sunset.png"), 
                size=(FpsSettings.HALF_SCREEN_WIDTH, FpsSettings.HALF_SCREEN_HEIGHT)
            )

            self.music_tracks = [
                "audio/fps/music/e1m1.mp3",
                "audio/fps/music/e1m2.mp3",
                "audio/fps/music/e1m3.mp3",
                "audio/fps/music/e1m4.mp3",
                "audio/fps/music/e2m1.mp3",
            ]

