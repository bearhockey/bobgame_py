import pygame


class Controller(object):
    def __init__(self, player_object):
        self.player = player_object
        print("Keyboard controller initialized or whatever")
        self.delay_time = 10
        self.wait_time = 0

        self.current_action = None

        # da keys tho
        self.keys = {"down": pygame.K_DOWN,
                     "up": pygame.K_UP,
                     "left": pygame.K_LEFT,
                     "right": pygame.K_RIGHT,
                     "action": pygame.K_SPACE,
                     "cancel": pygame.K_ESCAPE
                     }

    def poll_battle(self, battle, delay_timer):
        if self.wait_time and self.wait_time > 0:
            self.wait_time -= 1
        elif pygame.key.get_focused() and delay_timer < 1:
            press = pygame.key.get_pressed()
            if battle.state == "TARGET":
                if press[self.keys["action"]] != 0:
                    battle.character_action(target=battle.battle_picker.get_target())
                    return self.delay_time
                elif press[self.keys["cancel"]] != 0:
                    battle.show_action_menu()
                    return self.delay_time
                elif press[self.keys["down"]] != 0:
                    battle.battle_picker.cursor_down()
                    return self.delay_time
                elif press[self.keys["up"]] != 0:
                    battle.battle_picker.cursor_up()
                    return self.delay_time
            elif battle.state == "MENU":
                if press[self.keys["action"]] != 0:
                    battle.choose_target(category=battle.battle_box.get_action()["TARGET"])
                    return self.delay_time
                elif press[self.keys["down"]] != 0:
                    battle.battle_box.cursor_down()
                    return self.delay_time
                elif press[self.keys["up"]] != 0:
                    battle.battle_box.cursor_up()
                    return self.delay_time

    def poll_menu(self, camera):
        if self.wait_time and self.wait_time > 0:
            self.wait_time -= 1
        elif pygame.key.get_focused():
            press = pygame.key.get_pressed()
            if press[self.keys["cancel"]] != 0:
                camera.close_menu()
                self.wait_time = 10

    def poll(self, camera, tbox, delay_timer, action_map):
        if self.wait_time and self.wait_time > 0:
            self.wait_time -= 1
        elif pygame.key.get_focused() and delay_timer < 1:
            press = pygame.key.get_pressed()
            # ignore everything if text box is on screen
            if self.current_action:
                action_type = action_map.get_action_type(self.current_action)
                if action_type == "battle":
                    camera.start_battle(battle_info=action_map.get_action(self.current_action))
                    self.next_action(action_map)
                elif action_type == "text":
                    if press[self.keys['action']] != 0:
                        tbox.close()
                        self.next_action(action_map)
                        return self.delay_time
                else:
                    self.next_action(action_map)
            else:
                # player directionals
                s = self.player.speed
                test = None
                if press[self.keys["down"]] != 0:
                    self.player.set_direction("down")
                    test = self.player.pass_rect.copy()
                    blocked = False
                    for x in camera.map.passmap:
                        if test.move(0, s).colliderect(x):
                            blocked = True
                    for o in camera.map.object_list:
                        if test.move(0, s).colliderect(o.position):
                            blocked = True
                    if not blocked:
                        self.player.move(0, s)
                elif press[self.keys["up"]] != 0:
                    self.player.set_direction("up")
                    test = self.player.pass_rect.copy()
                    blocked = False
                    for x in camera.map.passmap:
                        if test.move(0, -s).colliderect(x):
                            blocked = True
                    for o in camera.map.object_list:
                        if test.move(0, -s).colliderect(o.position):
                            blocked = True
                    if not blocked:
                        self.player.move(0, -s)

                if press[self.keys["left"]] != 0:
                    self.player.set_direction("left")
                    test = self.player.pass_rect.copy()
                    blocked = False
                    for x in camera.map.passmap:
                        if test.move(-s, 0).colliderect(x):
                            blocked = True
                    for o in camera.map.object_list:
                        if test.move(-s, 0).colliderect(o.position):
                            blocked = True
                    if not blocked:
                        self.player.move(-s, 0)
                elif press[self.keys["right"]] != 0:
                    self.player.set_direction("right")
                    test = self.player.pass_rect.copy()
                    blocked = False
                    for x in camera.map.passmap:
                        if test.move(s, 0).colliderect(x):
                            blocked = True
                    for o in camera.map.object_list:
                        if test.move(s, 0).colliderect(o.position):
                            blocked = True
                    if not blocked:
                        self.player.move(s, 0)

                if test is not None:
                    self.player.moving = True
                else:
                    self.player.moving = False

                if press[self.keys["cancel"]] != 0:
                    camera.open_menu()
                    self.wait_time = 10
                elif press[self.keys["action"]] != 0:
                    for o in camera.map.object_list:
                        if self.player.get_action_rect().colliderect(o.position):
                            self.current_action = o.action()
                            action_map.trigger_action(self.current_action)
                            return self.delay_time

    def next_action(self, action_map):
        if "next" in action_map.get_action(self.current_action):
            self.current_action = action_map.get_next_action(self.current_action)
            self.wait_time = action_map.trigger_action(self.current_action)
            print("NEXT ACTION IS {0}".format(self.current_action))
        else:
            print("CLEARING ACTION")
            self.current_action = None
        return self.delay_time
