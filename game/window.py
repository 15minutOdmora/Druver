"""
Module for the Window class which handles everything related to window drawing and updating.
Game wide objects and settings should be set here.
"""

import pygame


class Window:
    def __init__(self, game: "Game"):
        self.game = game
        self.screen = self.game.screen

    def update(self) -> None:
        """
        Method loads the current page and everything else that should be drawn to the screen.
        """
        self.screen.fill((0, 0, 0))
        if not self.game.paused:  # If game is paused, do not update items
            self.game.controller.current_page.update()
        self.game.controller.current_page.draw()
        self.game.development.draw()  # Draw development
        pygame.display.update()

