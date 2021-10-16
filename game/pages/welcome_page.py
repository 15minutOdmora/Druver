"""
Welcome page loads when the game is ran.
"""

import pygame

from game.pages.page import Page
from game.gui.text import Text


class WelcomePage(Page):
    def __init__(self, controller):
        super().__init__(controller)

        self.title = Text(
            text="Welcome Page",
            position=(200, 200)
        )
        self.add_item(self.title)
