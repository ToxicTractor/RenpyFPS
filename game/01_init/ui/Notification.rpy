init -1 python:
    class Notification():
        DEFAULT_NOTIFICATION_DURATION = 2.5
        def __init__(self):
            self.notification = None
            self.timer = None

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
        

        def show(self, text, *, duration=DEFAULT_NOTIFICATION_DURATION, notification_type=ENotificationType.Default):
            self.notification = NotificationEntry(text, duration, notification_type)
            self.timer = duration

            self.notification_show_event.invoke(self.notification)