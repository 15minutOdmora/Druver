"""
Module for the Window class which handles everything related to window drawing and updating.
Game wide objects and settings should be set here.
"""

import pygame


class Window:
    """
    Main class for handling everything window related.
    """
    def __init__(self, game: "Game"):
        """
        :param game: Game main object for current game
        """
        self.game = game
        self.screen = self.game.screen

    def update(self) -> None:
        """
        Method loads the current page and everything else that should be drawn to the screen.
        """
        self.screen.fill((0, 0, 0))
        self.game.controller.current_page.update()
        self.game.controller.current_page.draw()
        self.game.development.draw()  # Draw development
        pygame.display.update()

