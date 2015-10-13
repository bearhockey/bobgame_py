import pygame

from Box import Box


class BattleMenu(Box):
    def __init__(self, box_bounds, options=[], color=None):
        Box.__init__(self, box_bounds, color)
        self.options = options
        self.position = 0

    def draw(self, screen):
        if self.visible:
            Box.draw(self, screen)
            if self.options:
                for o in self.options:
                    position = self.inner_box.top + (self.options.index(o) * self.cursor_offset)
                    screen.blit(self.font.render(o, True, self.white),
                                (self.inner_box.left + self.cursor_offset + self.space*2, position + self.space))
            screen.blit(self.cursor, (self.inner_box.left + self.space,
                                      self.position * self.cursor_offset + self.space*1.5))

    def cursor_down(self):
        if self.position < 4:
            self.position += 1

    def cursor_up(self):
        if self.position > 0:
            self.position -= 1

    def open(self, color=None):
        Box.open(self, color)

    def close(self):
        Box.close(self)
