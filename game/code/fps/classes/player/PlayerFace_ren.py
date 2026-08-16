import random
from game.code.fps.classes.GameEvent_ren import GameEvent
from game.code.fps.classes.settings.Constants_ren import FpsConstants
from game.code.fps.enums.EEmotion_ren import EFaceEmote
from game.code.fps.other.helper_functions_ren import clamp

"""renpy
init python:
"""

FPS_FACE_IMAGES = {
    EFaceEmote.Neutral: [
        ImageReference("fps_face_20_neutral"),
        ImageReference("fps_face_40_neutral"),
        ImageReference("fps_face_60_neutral"),
        ImageReference("fps_face_80_neutral"),
        ImageReference("fps_face_100_neutral"),
    ],
    EFaceEmote.Crazed: [
        ImageReference("fps_face_20_crazed"),
        ImageReference("fps_face_40_crazed"),
        ImageReference("fps_face_60_crazed"),
        ImageReference("fps_face_80_crazed"),
        ImageReference("fps_face_100_crazed"),
    ],
    EFaceEmote.Hurt: [
        ImageReference("fps_face_20_hurt"),
        ImageReference("fps_face_40_hurt"),
        ImageReference("fps_face_60_hurt"),
        ImageReference("fps_face_80_hurt"),
        ImageReference("fps_face_100_hurt"),
    ],
    EFaceEmote.LookLeft: [
        ImageReference("fps_face_20_left"),
        ImageReference("fps_face_40_left"),
        ImageReference("fps_face_60_left"),
        ImageReference("fps_face_80_left"),
        ImageReference("fps_face_100_left"),
    ],
    EFaceEmote.LookRight: [
        ImageReference("fps_face_20_right"),
        ImageReference("fps_face_40_right"),
        ImageReference("fps_face_60_right"),
        ImageReference("fps_face_80_right"),
        ImageReference("fps_face_100_right"),
    ]
}

class PlayerFace():
    def __init__(self, player_health):

        self.player_health = player_health
        self.current_emote = EFaceEmote.Neutral
        self.damage_threshold_interval = 20
        self.at = 0

        self.current_duration = 1

        self.hurt_event = GameEvent(self._set_hurt_emote)
        self.attack_event = GameEvent(self._set_crazed_emote)

        self.emote_count = len(FPS_FACE_IMAGES[EFaceEmote.Neutral])


    def update(self, delta_time, player_health):

        self.player_health = player_health

        if (self.at < self.current_duration):
            self.at += delta_time
            return

        if (self.current_emote in FpsConstants.NEUTRAL_EMOTES):
            self._set_new_idle_emote()
        else:
            self._set_neutral_emote()


    def get_image(self):

        index = clamp(self.player_health // self.damage_threshold_interval, 0, self.emote_count - 1)

        return FPS_FACE_IMAGES[self.current_emote][index]


    def _get_neutral_emote_duration(self):

        return random.uniform(1.0, 4.0)


    def _set_neutral_emote(self):
        self.current_duration = self._get_neutral_emote_duration()
        self.current_emote = EFaceEmote.Neutral
        self.at = 0


    def _set_hurt_emote(self):
        self.current_duration = 0.5
        self.current_emote = EFaceEmote.Hurt
        self.at = 0


    def _set_crazed_emote(self):
        self.current_duration = 1.0
        self.current_emote = EFaceEmote.Crazed
        self.at = 0


    def _set_new_idle_emote(self):

        if (self.current_emote == EFaceEmote.Neutral):
            self.current_emote = random.choice(FpsConstants.NEUTRAL_EMOTES)

            if (self.current_emote in FpsConstants.LOOK_EMOTES):
                self.current_duration = 1
            else:
                self.current_duration = self._get_neutral_emote_duration()

        elif (self.current_emote in FpsConstants.LOOK_EMOTES):

            self._set_neutral_emote()

        self.at = 0
