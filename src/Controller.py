import pygame


class Controller(object):
    def __init__(self, player_object):
        self.player = player_object
        print 'Keyboard controller initialized or whatever'
        self.delay_time = 15
        self.wait_time = 0

        self.current_action = None

        # da keys tho
        self.keys = {'down': pygame.K_DOWN,
                     'up': pygame.K_UP,
                     'left': pygame.K_LEFT,
                     'right': pygame.K_RIGHT,
                     'action': pygame.K_SPACE
                     }

    def poll(self, map_object, tbox, delay_timer, action_map):
        if self.wait_time > 0:
            self.wait_time -= 1
        elif pygame.key.get_focused() and delay_timer < 1:
            press = pygame.key.get_pressed()

            # ignore everything if text box is on screen
            if self.current_action:
                action_type = action_map.get_action_type(self.current_action)
                if action_type == 'text':
                    if press[self.keys['action']] != 0:
                        tbox.close()
                        self.next_action(action_map)
                        return self.delay_time
                elif action_type == 'wait':
                    self.next_action(action_map)
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
                            self.current_action = o.action()
                            action_map.trigger_action(self.current_action)
                            return self.delay_time

    def next_action(self, action_map):
        if 'next' in action_map.get_action(self.current_action):
            self.current_action = action_map.get_next_action(self.current_action)
            self.wait_time = action_map.trigger_action(self.current_action)
        else:
            self.current_action = None
        return self.delay_time
