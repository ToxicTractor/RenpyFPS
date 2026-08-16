from game.code.fps.classes.GameEvent_ren import GameEvent

"""renpy
init python:
"""

class InputKeyHandler():
    def __init__(self, key, *, on_key_down=None, on_key_up=None, on_key=None):

        self._pressed = False
        self._key = key

        self.on_key_down = GameEvent()
        self.on_key_up = GameEvent()
        self.on_key = GameEvent()

        if (on_key_down is not None):
            self.on_key_down.add_listener(on_key_down)
        if (on_key_up is not None):
            self.on_key_up.add_listener(on_key_up)
        if (on_key is not None):
            self.on_key.add_listener(on_key)


    def handle_input(self, input_event):
        if (input_event[self._key]):

            if (not self._pressed):
                self._pressed = True
                self.on_key_down.invoke()

            self.on_key.invoke()

        elif (self._pressed):
            self._pressed = False
            self.on_key_up.invoke()
