"""
Module containing the input class which updates and handles keyboard / mouse input.
"""

import pygame


def get_key_pressed_dict(keys_pressed):
    mouse = pygame.mouse.get_pressed()
    return {
        "left": keys_pressed[pygame.K_LEFT],
        "right": keys_pressed[pygame.K_RIGHT],
        "up": keys_pressed[pygame.K_UP],
        "down": keys_pressed[pygame.K_DOWN],
        "enter": keys_pressed[pygame.K_RETURN],
        "space": keys_pressed[pygame.K_SPACE],
        "mouse": {
            "left": mouse[0],
            "rel": mouse[1],
            "right": mouse[2]
        }
    }


class Input:
    def __init__(self, game):
        self.game = game
        self.controller = self.game.controller

        self.update()

    def update(self) -> bool:
        """
        Method checks and updates the currently clicked pressed down buttons.
        :return: bool -> False if game was quit, True otherwise
        """
        self.controller.mouse_position = pygame.mouse.get_pos()
        self.controller.key_pressed = get_key_pressed_dict(pygame.key.get_pressed())
        for event in pygame.event.get():
            # Mouse events
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.controller.mouse_clicked = True
            else:
                self.controller.mouse_clicked = False
            if event.type == pygame.KEYDOWN:
                # Todo: Implement menus buttons selection with keyboard
                if event.key == pygame.K_d:  # This will enable development display
                    self.game.development.visible = not self.game.development.visible
                """elif event.key == pygame.K_r:
                    self.game.window.radio = not self.game.window.radio"""
                if event.key == pygame.K_ESCAPE:
                    self.controller.esc_clicked = True
            else:
                self.controller.esc_clicked = False
            # Quit event
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

        return True
