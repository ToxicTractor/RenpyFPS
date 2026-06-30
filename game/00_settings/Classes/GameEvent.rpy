init -10 python:
    class GameEvent():
        def __init__(self, initial_listeners=[]):
            self._listeners = []

            if (isinstance(initial_listeners, list)):
                for listener in initial_listeners:
                    self._listeners.append(listener)
            else:
                self._listeners.append(initial_listeners)

        def add_listener(self, listener):
            if (listener not in self._listeners):
                self._listeners.append(listener)


        def remove_listener(self, listener):
            if (listener in self._listeners):
                self._listeners.remove(listener)


        def invoke(self, event_data=None):
            for listener in self._listeners:
                listener(event_data)