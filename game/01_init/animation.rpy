init python:

    class AnimationData():

        def __init__(self, image_name, duration, loop=False):
            self.image_name = image_name
            self.image = ImageReference(image_name)
            self.duration = duration
            self.loop = loop