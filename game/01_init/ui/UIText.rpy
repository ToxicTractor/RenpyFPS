init python:
    class UIText():
        def __init__(self, text, pos, size=24, tint="#fff", dynamic_text_source=None):
            self.text = text
            self.pos = pos
            self.size = size
            self.tint = tint

            self._display_text = text
            self._dynamic_text_source = dynamic_text_source
        

        def draw(self, screen):
            
            self.update_display_text()

            text_render = renpy.render(Text(self._display_text, False, font="images/fps/ui/fonts/fps_font.ttf", color=self.tint, size=self.size), config.screen_width, config.screen_height, 0, 0)

            screen.blit(text_render, self.pos)
        

        def update_display_text(self):

            if (self._dynamic_text_source is None):
                return
            
            self._display_text = self.text.replace("<dynamic>", str(self._dynamic_text_source()))


        def update(self, delta_time):
            pass