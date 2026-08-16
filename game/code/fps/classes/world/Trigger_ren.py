from game.code.fps.classes.GameEvent_ren import GameEvent
from game.code.fps.enums.ETriggerShape_ren import ETriggerShape
from game.code.fps.enums.ETriggerType_ren import ETriggerType
from game.code.fps.other.helper_functions_ren import sqr_dist
from game.code.fps.other.named_tuples_ren import Vector2

"""renpy
init -1 python:
"""

class Trigger():
    def __init__(self, game, pos, size, trigger_shape=ETriggerShape.Rectangle, trigger_type=ETriggerType.PlayerOnly, once_only=False):
        self.game = game
        self.player = game.player
        self.pos = Vector2(*pos)
        self.width, self.height = size
        self._trigger_shape = trigger_shape
        self._trigger_type = trigger_type
        self._entities_in_trigger_last_frame = []
        self._once_only = False
        self._enter_triggered = False
        self._exit_triggered = False

        self.enter_event = GameEvent(self.on_enter_event)
        self.exit_event = GameEvent(self.on_exit_event)

        ## same events as above but they are invoked with the entity that triggered the event
        ## they are also called just after the normal events
        self.enter_entity_event = GameEvent()
        self.exit_entity_event = GameEvent()

    def update(self, delta_time):
        if (self._once_only and self._enter_triggered and self._exit_triggered):
            return

        if (self._trigger_type in (ETriggerType.PlayerOnly, ETriggerType.Any)):
            self._handle_entity_events(self.player)

        if (self._trigger_type in (ETriggerType.NpcOnly, ETriggerType.Any)):
            for npc in self.game.npcs:
                self._handle_entity_events(npc)


    def on_enter_event(self):
        self._enter_triggered = True


    def on_exit_event(self):
        self._exit_triggered = True


    def is_inside(self, pos):

        if (self._trigger_shape is ETriggerShape.Circle):
            ## treat size as radius
            return sqr_dist(self.pos, pos) <= self.size**2

        else:## fall back to a rectangle shape
            return (pos.x >= self.pos.x and
                    pos.x <= self.pos.x + self.width and
                    pos.y >= self.pos.y and
                    pos.y <= self.pos.y + self.height)


    def _handle_entity_events(self, entity):

        if (self.is_inside(entity.pos)):
            if (entity not in self._entities_in_trigger_last_frame):
                if (self._once_only and self._enter_triggered):
                    return

                self._entities_in_trigger_last_frame.append(entity)
                self.enter_event.invoke()
                self.enter_entity_event.invoke(entity)

        elif (entity in self._entities_in_trigger_last_frame):
            if (self._once_only and self._exit_triggered):
                return

            self._entities_in_trigger_last_frame.remove(entity)
            self.exit_event.invoke()
            self.exit_entity_event.invoke(entity)
