__author__ = 'max_hart'

import pygame
import json


class Map(object):
    def __init__(self, map_file):
        self.name = 'Hey'
        self.passmap = []
        with open(map_file) as data_file:
            self.map_data = json.load(data_file)
            data_file.close()
        print self.map_data['tilesets'][0]['image']
        self.map_tileset = pygame.image.load('..\\assets\\{0}'.format(self.map_data['tilesets'][0]['image']))

        self.map_size = 800, 600

        # why is this a warning, it's perfectly fine, this is annoying
        self.actual_map = pygame.Surface(self.map_size)
        self.build_map()

    def draw(self, screen, passmap=False):
        screen.blit(self.actual_map, (0, 0))
        if passmap:
            for block in self.passmap:
                pygame.draw.rect(screen, (255,255,255), block)

    def build_map(self):
        for layer in self.map_data['layers']:
            if layer['visible'] and layer['type'] == 'tilelayer':
                pos = 0
                t_width = self.map_data['tilesets'][0]['tilewidth']
                t_height = self.map_data['tilesets'][0]['tileheight']
                for i in layer['data']:
                    y_cord = int(pos / layer['width'])
                    x_cord = int(pos % layer['width'])

                    if layer['name'] == 'passmap':
                        if i != 0:
                            self.passmap.append(pygame.Rect(x_cord * t_width, y_cord * t_height, t_width, t_height))
                    else:
                        tile_x = (i - 1) % (self.map_data['tilesets'][0]['imagewidth'] / t_width)
                        tile_x = tile_x * t_width
                        tile_y = (i - 1) / (self.map_data['tilesets'][0]['imagewidth'] / t_height)
                        tile_y = tile_y * t_height

                        self.actual_map.blit(self.map_tileset, (x_cord * t_width, y_cord * t_height),
                                             area=pygame.Rect(tile_x, tile_y, self.map_data['tilesets'][0]['tilewidth'],
                                                              self.map_data['tilesets'][0]['tileheight']))
                    pos += 1
