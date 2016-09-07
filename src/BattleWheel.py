import pygame


class BattleWheel(object):
    def __init__(self, actors, position=(100, 100), radius=100, background=(0, 0, 0)):
        print 'I am wheel'
        self.members = actors
        self.position = position
        self.radius = radius
        self.background = background

    def get_next(self):
        return self.members[0]

    def set_actor_time(self, time):
        actor = self.members.pop(0)
        self.members.insert(time, actor)

    def draw(self, screen):
        pygame.draw.circle(screen, self.background, self.position, self.radius-2)
        pygame.draw.circle(screen, (255, 255, 255), self.position, self.radius, 3)
