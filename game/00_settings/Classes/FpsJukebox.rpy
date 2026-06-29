init python:
    class FpsJukebox():
        def __init__(self, map):
            self.map = map

        def play(self):

            renpy.music.play(self.map.music_tracks, loop=True)