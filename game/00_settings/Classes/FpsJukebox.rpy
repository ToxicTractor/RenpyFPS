init python:
    class FpsJukebox():
        def __init__(self):

            self.songs = [
                "audio/fps/music/e1m1.mp3",
                "audio/fps/music/e1m2.mp3",
                "audio/fps/music/e1m3.mp3",
                "audio/fps/music/e1m4.mp3",
                "audio/fps/music/e2m1.mp3",
            ]

        def play(self):

            renpy.music.play(self.songs, loop=True)