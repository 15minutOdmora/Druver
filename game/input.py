"""
Module containing the input class which updates and handles keyboard / mouse input.
"""

import pygame


def get_key_pressed_dict() -> dict:
    """
    Method returns a dictionary of currently pressed keys (on current frame).
    :return: dict containing all used keys state
    """
    keys_pressed = pygame.key.get_pressed()
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
    """
    Main class for handling keyboard and mouse input.
    """
    def __init__(self, game):
        """
        :param game: Game main object in current game
        """
        self.game = game
        self.controller = self.game.controller

        self.escape_key_released = True  # Needed to know when it was released so game pause works correctly

        self.update()

    def update(self) -> bool:
        """
        Method checks and updates the currently clicked pressed down buttons.
        :return: bool -> False if game was quit, True otherwise
        """
        for event in pygame.event.get():
            # Mouse events
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.controller.mouse_clicked = True
            else:
                self.controller.mouse_clicked = False
            if event.type == pygame.MOUSEWHEEL:
                self.controller.mouse_scroll = event.y  # This attribute has to be reset outside this event loop
            if event.type == pygame.KEYDOWN:
                # Todo: Implement menus buttons selection with keyboard
                if event.key == pygame.K_d:  # This will enable development display
                    self.game.development.visible = not self.game.development.visible
                """elif event.key == pygame.K_r:
                    self.game.window.radio = not self.game.window.radio"""
                if event.key == pygame.K_ESCAPE:
                    if self.escape_key_released:
                        self.game.paused = not self.game.paused
                        self.escape_key_released = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    self.escape_key_released = True
            # Quit event
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
        # We do this at the end as mouse.get_pressed might not as expected if called before pygame.event.get()
        self.controller.mouse_position = pygame.mouse.get_pos()
        key_pressed = get_key_pressed_dict()
        self.controller.key_pressed = key_pressed
        self.controller.mouse_pressed = key_pressed["mouse"]["left"]
        self.controller.mouse_movement = pygame.mouse.get_rel()  # Movement of mouse on two consecutive calls
        return True
