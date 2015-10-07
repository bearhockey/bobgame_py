import pygame


class MapObject(object):
    def __init__(self, object_json, tileset_info, text_box=None):
        self.name = 'You'
        self.data = object_json
        self.properties = self.data['properties']
        self.portrait = None

        if 'portrait' in self.properties:
            self.set_portrait(self.properties['portrait'])

        self.tile_set_data = tileset_info
        self.text_box = text_box
        x = (self.data['gid'] - 1) % (self.tile_set_data['width'] / self.tile_set_data['t_width'])
        x = x * self.tile_set_data['t_width']
        y = (self.data['gid'] - 1) / self.tile_set_data['t_width']
        y = y * self.tile_set_data['t_height']
        self.tileset_rect = pygame.Rect(x, y, self.data['width'], self.data['height'])

        self.position = pygame.Rect(self.data['x'], self.data['y'], self.data['width'], self.data['height'])

    def draw(self, screen, tileset_image):
        screen.blit(tileset_image, self.position, area=self.tileset_rect)

    def get_offset(self, cam_offset):
        new_x = self.position.left + cam_offset[0]
        new_y = self.position.top + cam_offset[1]
        return pygame.Rect(new_x, new_y, self.position.width, self.position.height)

    def action(self):
        if 'action' in self.properties:
            return self.properties['action']
        else:
            return None
