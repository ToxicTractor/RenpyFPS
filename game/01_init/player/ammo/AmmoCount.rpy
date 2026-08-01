init python:
    class AmmoCount():
        def __init__(self, current=0, max=999):
            self.current = min(current, max)
            self.max = max

        def full(self):
            return self.current >= self.max

        def add(self, amount):
            self.current = min(self.current + amount, self.max)

        def remove(self, amount=1):
            self.current = max(self.current - amount, 0)