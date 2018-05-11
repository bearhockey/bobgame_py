import pygame

from src.box.Box import Box


class Notice(Box):
    def __init__(self, screen_size, text=None, color=None, font_size=None):
        if font_size is None:
            font_size = 24
        box_height = font_size * 2 + 48
        box_width = len(text) * font_size + 20 + 48
        box_bounds = pygame.Rect(screen_size[0]/2 - box_width/2, screen_size[1]/2 - box_height/2, box_width, box_height)
        Box.__init__(self, box_bounds=box_bounds, color=color, font_size=font_size)
        self.text = text
        Box.open(self, color=color)

    def draw(self, screen):
        if self.visible:
            self.overlay.fill(self.color)
            self.overlay.blit(self.font.render(self.text, True, self.white), (self.space, self.space))
            Box.draw(self, screen)

    def close(self):
        Box.close(self)
