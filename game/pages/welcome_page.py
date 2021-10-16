"""
Welcome page loads when the game is ran.
"""

import pygame

from game.pages.page import Page
from game.gui.text import Text
from game.gui.button import Button
from game.gui.grid import Grid


def on_click_test():
    print("Works")


class WelcomePage(Page):
    def __init__(self, controller):
        super().__init__(controller)

        self.grid = Grid(
            rows=10,
            columns=3,
            visible=False
        )

        self.test_button = Button(
            self.controller,
            text="Testing",
            on_click=on_click_test
        )
        self.grid.add_item(
            row=3,
            col=1,
            item=self.test_button,
            align="centre"
        )

        self.add_item(self.grid)
