from game.code.fps.classes.GameEvent_ren import GameEvent
from game.code.fps.classes.settings.Constants_ren import FpsConstants
from game.code.fps.enums.ENotificationType_ren import ENotificationType
from game.code.fps.other.named_tuples_ren import NotificationEntry

"""renpy
init -1 python:
"""

class Notification():
    def __init__(self):
        self.notification = None
        self.timer = None
        self.type = None

        self.notification_show_event = GameEvent()
        self.notification_hide_event = GameEvent()

    @property
    def text(self):
        return self.notification.text if self.notification else ""

    @property
    def is_active(self):
        return self.notification is not None


    def update(self, delta_time):

        if (not self.notification):
            return

        if (self.timer):
            if (self.timer > 0):
                self.timer -= delta_time
            else:
                self.timer = None

                self.notification_hide_event.invoke(self.notification)
                self.notification = None
                self.type = None


    def show(self, text, *, duration=FpsConstants.DEFAULT_NOTIFICATION_DURATION, type=ENotificationType.Default):
        self.notification = NotificationEntry(text, duration, type)
        self.timer = duration
        self.type = type

        self.notification_show_event.invoke(self.notification)
