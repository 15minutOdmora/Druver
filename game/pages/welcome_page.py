"""
Welcome page loads when the game is ran.
"""

import pygame

from game.pages.page import Page
from game.gui.text import Text
from game.gui.button import Button


def on_click_test():
    print("Works")


class WelcomePage(Page):
    def __init__(self, controller):
        super().__init__(controller)

        self.test_button = Button(
            self.controller,
            text="Testing",
            on_click=on_click_test
        )
        self.add_item(self.test_button)
