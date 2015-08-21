__author__ = 'max_hart'

import pygame


class MapObject(object):
    def __init__(self, object_json, tileset_info):
        self.name = 'You'
        self.data = object_json
        self.tileset_data = tileset_info
        x = (self.data['gid'] - 1) % (self.tileset_data['width'] / self.tileset_data['t_width'])
        x = x * self.tileset_data['t_width']
        y = (self.data['gid'] - 1) / self.tileset_data['t_width']
        y = y * self.tileset_data['t_height']
        self.tileset_rect = pygame.Rect(x, y, self.data['width'], self.data['height'])

        self.position = pygame.Rect(self.data['x'], self.data['y'], self.data['width'], self.data['height'])

    def draw(self, screen, tileset_image):
        screen.blit(tileset_image, self.position, area=self.tileset_rect)

    def action(self):
        print 'Action was done to object {0}'.format(self.data['id'])
