from src.box.Box import Box


class SelectBox(Box):
    def __init__(self, box_bounds, color=None):
        Box.__init__(self, box_bounds, color)
        self.options = []
        self.position = 0

    def draw(self, screen):
        if self.visible:
            self.overlay.fill(self.color)
            if self.options:
                for o in self.options:
                    position = self.inner_box.top + (self.options.index(o) * self.cursor_offset)
                    self.overlay.blit(self.font.render(o["NAME"], True, self.white),
                                      (self.cursor_offset + self.space*2, position + self.space))
            self.overlay.blit(self.cursor, (self.space, self.position * self.cursor_offset + self.space))
            Box.draw(self, screen)

    def get_action(self):
        return self.options[self.position]

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

    def reset(self):
        self.options.clear()
        self.position = 0
