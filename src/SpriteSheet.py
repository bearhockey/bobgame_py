import pygame


class SpriteSheet(object):
    def __init__(self, filename, pic_width, pic_height):
        try:
            self.sheet = pygame.image.load(filename).convert_alpha()
            self.height = pic_height
            self.width = pic_width
            self.frame = 0
            self.ping = "ping"
            self.frame_timer = 0
        except pygame.error:
            raise Exception("Unable to load spritesheet image: {0}".format(filename))

    def draw(self, source, destination, x, y, flipped=False):
        # rect = (x * self.width, y * self.height, self.width, self.height)
        try:
            rect = pygame.Rect(x * self.width, y * self.height, self.width, self.height)
        except TypeError:
            raise Exception("{0} {1} {2} {3}".format(x, y, self.width, self.height))
        if flipped:
            source.blit(pygame.transform.flip(self.sheet, 1, 0), destination, area=rect)
        else:
            try:
                source.blit(self.sheet, destination, area=rect)
            except TypeError:
                raise Exception("What? {0}".format(type(rect)))

    def animate(self, source, destination, row, wait_time, ping_pong=True, flipped=False):
        self.draw(source, destination, self.frame, row, flipped=flipped)
        if self.frame_timer == 0:
            self.frame_timer = wait_time
            if self.ping == "ping":
                if ((self.frame + 1) * self.width) >= self.sheet.get_width():
                    if ping_pong:
                        self.frame -= 1
                        self.ping = "pong"
                    else:
                        self.frame = 0
                else:
                    self.frame += 1
            else:
                if self.frame == 0:
                    self.frame += 1
                    self.ping = "ping"
                else:
                    self.frame -= 1
        else:
            self.frame_timer -= 1
