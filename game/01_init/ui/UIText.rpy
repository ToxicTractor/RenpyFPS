init python:
    class UIText():
        def __init__(self, text, pos, size=24, color="#fff", dynamic_text_source=None, outline_color=None, outline_width=0, outline_offset=(0, 0)):
            self.text = text
            self.pos = pos
            self.size = size
            self.color = color

            self._display_text = text
            self._dynamic_text_source = dynamic_text_source

            self.outline_color = outline_color
            self.outline_width = outline_width
            self.outline_offset = outline_offset
        

        def draw(self, screen):
            
            self.update_display_text()
            
            if (self.outline_color):
                text_displayable = Text(self._display_text, False, font="images/fps/ui/fonts/fps_font.ttf", color=self.color, size=self.size, outlines=[(self.outline_width, self.outline_color, self.outline_offset[0], self.outline_offset[1])])
            else:
                text_displayable = Text(self._display_text, False, font="images/fps/ui/fonts/fps_font.ttf", color=self.color, size=self.size)

            text_render = renpy.render(text_displayable, config.screen_width, config.screen_height, 0, 0)

            screen.blit(text_render, self.pos)
        

        def update_display_text(self):

            if (self._dynamic_text_source is None):
                return
            
            self._display_text = self.text.replace("<dynamic>", str(self._dynamic_text_source()))


        def update(self, delta_time):
            pass