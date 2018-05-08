import pygame


class Controller(object):
    def __init__(self):
        print("Keyboard controller initialized or whatever")
        self.delay_timer = 0
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

    def delay(self):
        self.delay_timer += 10

    def poll_battle(self, battle):
        if self.delay_timer and self.delay_timer > 0:
            self.delay_timer -= 1
        elif pygame.key.get_focused():
            press = pygame.key.get_pressed()
            if battle.state == "TARGET":
                if press[self.keys["action"]] != 0:
                    battle.character_action(target=battle.battle_picker.get_target())
                    self.delay()
                elif press[self.keys["cancel"]] != 0:
                    battle.show_action_menu()
                    self.delay()
                elif press[self.keys["down"]] != 0:
                    battle.battle_picker.cursor_down()
                    self.delay()
                elif press[self.keys["up"]] != 0:
                    battle.battle_picker.cursor_up()
                    self.delay()
            elif battle.state == "MENU":
                if press[self.keys["action"]] != 0:
                    battle.choose_target(category=battle.battle_box.get_action()["TARGET"])
                    self.delay()
                elif press[self.keys["down"]] != 0:
                    battle.battle_box.cursor_down()
                    self.delay()
                elif press[self.keys["up"]] != 0:
                    battle.battle_box.cursor_up()
                    self.delay()

    def poll_menu(self, menu):
        if self.delay_timer and self.delay_timer > 0:
            self.delay_timer -= 1
        elif pygame.key.get_focused():
            press = pygame.key.get_pressed()
            if press[self.keys["action"]] != 0:
                # menu.act(action=menu.options.get_action())
                self.delay()
                return menu.get_action()
            elif press[self.keys["down"]] != 0:
                menu.cursor_down()
                self.delay()
            elif press[self.keys["up"]] != 0:
                menu.cursor_up()
                self.delay()

    def poll_main_menu(self, camera):
        if self.delay_timer and self.delay_timer > 0:
            self.delay_timer -= 1
        elif pygame.key.get_focused():
            press = pygame.key.get_pressed()
            if press[self.keys["cancel"]] != 0:
                camera.close_menu()
                self.delay()
            elif press[self.keys["action"]] != 0:
                camera.menu.act(action=camera.menu.options.get_action(), camera=camera)
                self.delay()
            elif press[self.keys["down"]] != 0:
                camera.menu.options.cursor_down()
                self.delay()
            elif press[self.keys["up"]] != 0:
                camera.menu.options.cursor_up()
                self.delay()

    def poll(self, camera, tbox, action_map):
        if self.delay_timer and self.delay_timer > 0:
            self.delay_timer -= 1
        elif pygame.key.get_focused():
            press = pygame.key.get_pressed()
            # ignore everything if text box is on screen
            if self.current_action:
                action_type = action_map.get_action_type(self.current_action)
                if action_type == "battle":
                    camera.start_battle(battle_info=action_map.get_action(self.current_action))
                    self.next_action(action_map)
                elif action_type == "text":
                    if press[self.keys["action"]] != 0:
                        tbox.close()
                        self.next_action(action_map)
                        self.delay()
                else:
                    self.next_action(action_map)
            else:
                # player directionals
                s = camera.player.speed
                camera.player.moving = False
                if press[self.keys["down"]] != 0:
                    camera.player.direction = "DOWN"
                    camera.player.moving = True
                    if not self.check_blocked(cord=(0, s), pass_rect=camera.player.pass_rect.copy(), map=camera.map):
                        camera.player.move(0, s)
                elif press[self.keys["up"]] != 0:
                    camera.player.direction = "UP"
                    camera.player.moving = True
                    if not self.check_blocked(cord=(0, -s), pass_rect=camera.player.pass_rect.copy(), map=camera.map):
                        camera.player.move(0, -s)

                if press[self.keys["left"]] != 0:
                    camera.player.direction = "LEFT"
                    camera.player.moving = True
                    if not self.check_blocked(cord=(-s, 0), pass_rect=camera.player.pass_rect.copy(), map=camera.map):
                        camera.player.move(-s, 0)
                elif press[self.keys["right"]] != 0:
                    camera.player.direction = "RIGHT"
                    camera.player.moving = True
                    if not self.check_blocked(cord=(s, 0), pass_rect=camera.player.pass_rect.copy(), map=camera.map):
                        camera.player.move(s, 0)

                if press[self.keys["cancel"]] != 0:
                    camera.open_menu()
                    self.delay()
                elif press[self.keys["action"]] != 0:
                    all_list = camera.map.object_list + camera.map.actor_list
                    for o in all_list:
                        if camera.player.get_action_rect().colliderect(o.position):
                            o.turn_to_face(direction=camera.player.direction)
                            self.trigger_action(action_map=action_map, action_id=o.action())

    @staticmethod
    def check_blocked(cord, pass_rect, map):
        for x in map.passmap:
            if pass_rect.move(cord[0], cord[1]).colliderect(x):
                return True
        for o in map.object_list:
            if pass_rect.move(cord[0], cord[1]).colliderect(o.position):
                return True
        for a in map.actor_list:
            if pass_rect.move(cord[0], cord[1]).colliderect(a.position):
                return True
        return False

    def trigger_action(self, action_map, action_id):
        self.current_action = action_id
        action_map.trigger_action(self.current_action)
        self.delay()

    def next_action(self, action_map):
        if "next" in action_map.get_action(self.current_action):
            self.current_action = action_map.get_next_action(self.current_action)
            action_map.trigger_action(self.current_action)
            print("NEXT ACTION IS {0}".format(self.current_action))
        else:
            print("CLEARING ACTION")
            self.current_action = None
        self.delay()
