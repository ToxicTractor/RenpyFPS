init -10 python:
    class GameEvent():
        def __init__(self):
            self._listeners = []

        def add_listener(self, listener):
            if (listener not in self._listeners):
                self._listeners.append(listener)


        def remove_listener(self, listener):
            if (listener in self._listeners):
                self._listeners.remove(listener)


        def invoke(self, event_data=None):
            for listener in self._listeners:
                listener(event_data)