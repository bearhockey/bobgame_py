import pygame


class FloatingText(object):
    def __init__(self, text, box_position, font_size=24, color=None, alpha=255):
        self.text = text
        # it needs to be a little wider than most sprites, tbh
        self.position = pygame.Rect(box_position.left, box_position.top, 200, 50)
        self.alpha = alpha

        self.font_size = font_size
        self.font = pygame.font.Font(pygame.font.get_default_font(), self.font_size)
        if color:
            self.color = color
        else:
            self.color = (255, 255, 255)

    def update(self):
        if self.alpha > 0:
            self.alpha -= 5
            box = self.position
            self.position = pygame.Rect(box.left, box.top-1, box.width, box.height)

    def draw(self, screen):
        overlay = pygame.Surface((self.position.width, self.position.height))
        overlay.set_colorkey((255, 0, 255))
        overlay.fill((255, 0, 255))
        overlay.blit(self.font.render(self.text, True, (0, 0, 0)), (2, 2))
        overlay.blit(self.font.render(self.text, True, self.color), (0, 0))
        overlay.set_alpha(self.alpha)
        screen.blit(overlay, self.position)
