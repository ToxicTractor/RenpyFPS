init python:
    class PlayerFace():
        def __init__(self, player):

            self.player = player
            self.current_emote = "neutral"
            self.damage_threshold_interval = 20
            self.at = 0

            self.current_duration = 1

            self.player.hurt_event.add_listener(self.set_hurt_emote)
            self.player.attack_event.add_listener(self.set_crazed_emote)


        def draw(self, screen):
            
            face_render = renpy.render(self.get_image(), 256, 256, 0, 0)

            screen.blit(face_render, (832, 819))


        def update(self, delta_time):
            
            if (self.at < self.current_duration):
                self.at += delta_time
                return

            if (self.current_emote in ("neutral", "left", "right")):
                self.set_new_idle_emote()
            else:
                self.set_neutral_emote()


        def get_image(self):

            index = clamp(self.player.health // self.damage_threshold_interval, 0, len(FPS_FACE_IMAGES["neutral"]) - 1)

            return FPS_FACE_IMAGES[self.current_emote][index]
        

        def get_neutral_emote_duration(self):

            return random.uniform(1.0, 4.0)

        def set_neutral_emote(self):
            self.current_duration = self.get_neutral_emote_duration()
            self.current_emote = "neutral"
            self.at = 0

        def set_hurt_emote(self):
            self.current_duration = 0.5
            self.current_emote = "hurt"
            self.at = 0

        def set_crazed_emote(self):
            self.current_duration = 1.0
            self.current_emote = "crazed"
            self.at = 0

        def set_new_idle_emote(self):

            if (self.current_emote == "neutral"):
                self.current_emote = random.choice(("neutral", "left", "right"))

                if (self.current_emote in ("left", "right")):
                    self.current_duration = 1
                else:
                    self.current_duration = self.get_neutral_emote_duration()

            elif (self.current_emote in ("left", "right")):

                self.set_neutral_emote()

            self.at = 0


define FPS_FACE_IMAGES = {
    "neutral": [
        Image("images/fps/ui/face/face_20_neutral.png"),
        Image("images/fps/ui/face/face_40_neutral.png"),
        Image("images/fps/ui/face/face_60_neutral.png"),
        Image("images/fps/ui/face/face_80_neutral.png"),
        Image("images/fps/ui/face/face_100_neutral.png"),
    ],
    "crazed": [
        Image("images/fps/ui/face/face_20_crazed.png"),
        Image("images/fps/ui/face/face_40_crazed.png"),
        Image("images/fps/ui/face/face_60_crazed.png"),
        Image("images/fps/ui/face/face_80_crazed.png"),
        Image("images/fps/ui/face/face_100_crazed.png"),
    ],
    "hurt": [
        Image("images/fps/ui/face/face_20_hurt.png"),
        Image("images/fps/ui/face/face_40_hurt.png"),
        Image("images/fps/ui/face/face_60_hurt.png"),
        Image("images/fps/ui/face/face_80_hurt.png"),
        Image("images/fps/ui/face/face_100_hurt.png"),
    ],
    "left": [
        Image("images/fps/ui/face/face_20_left.png"),
        Image("images/fps/ui/face/face_40_left.png"),
        Image("images/fps/ui/face/face_60_left.png"),
        Image("images/fps/ui/face/face_80_left.png"),
        Image("images/fps/ui/face/face_100_left.png"),
    ],
    "right": [
        Image("images/fps/ui/face/face_20_right.png"),
        Image("images/fps/ui/face/face_40_right.png"),
        Image("images/fps/ui/face/face_60_right.png"),
        Image("images/fps/ui/face/face_80_right.png"),
        Image("images/fps/ui/face/face_100_right.png"),
    ]
}
