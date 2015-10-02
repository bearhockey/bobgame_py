import pygame


class Controller(object):
    def __init__(self, player_object):
        self.player = player_object
        print 'Keyboard controller initialized or whatever'
        self.delay_time = 15

        # da keys tho
        self.keys = {'down': pygame.K_DOWN,
                     'up': pygame.K_UP,
                     'left': pygame.K_LEFT,
                     'right': pygame.K_RIGHT,
                     'action': pygame.K_SPACE
                     }

    def poll(self, map_object, tbox, delay_timer, action_map):
        if pygame.key.get_focused() and delay_timer < 1:
            press = pygame.key.get_pressed()

            # ignore everything if text box is on screen
            if tbox.visible:
                if press[self.keys['action']] != 0:
                    tbox.close()
                    return self.delay_time
            else:
                # player directionals
                s = self.player.speed
                test = None
                if press[self.keys['down']] != 0:
                    self.player.set_direction('down')
                    test = self.player.pass_rect.copy()
                    blocked = False
                    for x in map_object.passmap:
                        if test.move(0, s).colliderect(x):
                            blocked = True
                    for o in map_object.object_list:
                        if test.move(0, s).colliderect(o.position):
                            blocked = True
                    if not blocked:
                        self.player.move(0, s)
                elif press[self.keys['up']] != 0:
                    self.player.set_direction('up')
                    test = self.player.pass_rect.copy()
                    blocked = False
                    for x in map_object.passmap:
                        if test.move(0, -s).colliderect(x):
                            blocked = True
                    for o in map_object.object_list:
                        if test.move(0, -s).colliderect(o.position):
                            blocked = True
                    if not blocked:
                        self.player.move(0, -s)

                if press[self.keys['left']] != 0:
                    self.player.set_direction('left')
                    test = self.player.pass_rect.copy()
                    blocked = False
                    for x in map_object.passmap:
                        if test.move(-s, 0).colliderect(x):
                            blocked = True
                    for o in map_object.object_list:
                        if test.move(-s, 0).colliderect(o.position):
                            blocked = True
                    if not blocked:
                        self.player.move(-s, 0)
                elif press[self.keys['right']] != 0:
                    self.player.set_direction('right')
                    test = self.player.pass_rect.copy()
                    blocked = False
                    for x in map_object.passmap:
                        if test.move(s, 0).colliderect(x):
                            blocked = True
                    for o in map_object.object_list:
                        if test.move(s, 0).colliderect(o.position):
                            blocked = True
                    if not blocked:
                        self.player.move(s, 0)

                if test is not None:
                    self.player.moving = True
                else:
                    self.player.moving = False

                if press[self.keys['action']] != 0:
                    for o in map_object.object_list:
                        if self.player.get_action_rect().colliderect(o.position):
                            action_map.trigger_action(o.action())
                            return self.delay_time
