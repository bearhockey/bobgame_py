import pygame

from src.box.Box import Box


class TextBox(Box):
    def __init__(self, box_bounds, text=None, color=None, picture=None):
        Box.__init__(self, box_bounds, color)

        self.text = text
        self.portrait = self.get_image(picture)
        self.background = None

        self.choice = False
        self.choice_box = pygame.Rect(self.box.right - self.box.width / 3 - 10, self.box.top - 100,
                                      self.box.width / 3, self.font_size * 2 + self.space * 3)
        self.choice_inner_box = pygame.Rect(self.choice_box.left + self.border, self.choice_box.top + self.border,
                                            self.choice_box.width - self.border * 2,
                                            self.choice_box.height - self.border * 2)

    @staticmethod
    def get_image(url):

        if url:
            return pygame.image.load(url).convert_alpha()
        else:
            return None

    def draw(self, screen):
        if self.visible:
            if self.background:
                screen.blit(self.background, (0, 0))
            self.overlay.fill(self.color)
            if self.portrait:
                portrait_offset = 150 + self.space
                self.overlay.blit(self.portrait, (self.space, (self.inner_box.height - 150) / 2))
            else:
                portrait_offset = 0
            # text
            i = 0
            for text in self.text:
                if i < 5:
                    text_offset = self.font_size * 1.3 * i
                    self.overlay.blit(self.font.render(text, True, self.white),
                                      (portrait_offset + self.space, (self.inner_box.height - 150) / 2 + text_offset))
                i += 1
            if self.choice:
                self.overlay.fill(self.white, self.choice_box)
                self.overlay.fill(self.color, self.choice_inner_box)
                self.overlay.blit(self.font.render("Yes", True, self.white),
                                  (self.choice_inner_box.left + self.space,
                                   self.choice_inner_box.top + self.space))
                self.overlay.blit(self.font.render("No", True, self.white),
                                  (self.choice_inner_box.left + self.space,
                                   self.choice_inner_box.top + self.space * 2 + self.font_size))

            Box.draw(self, screen)

    def open(self, text=None, portrait=None, color=None, choice=None, background=None):
        if text:
            self.text = text
        if portrait:
            self.portrait = self.get_image(portrait)
        if choice:
            self.choice = choice
        if background:
            self.background = self.get_image(background)
        Box.open(self, color)

    def close(self):
        self.background = None
        self.portrait = None
        self.text = None
        Box.close(self)
