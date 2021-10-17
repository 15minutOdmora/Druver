"""
Welcome page loads when the game is ran.
"""

import pygame

from game.pages.page import Page
from game.constants import Paths
from game.gui.text import CustomText
from game.gui.button import Button
from game.gui.image import StaticImage
from game.gui.grid import Grid


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
            text=CustomText(
                text="Start Game",
                size=30
            ),
            size=(130, 40)
        )
        self.grid.add_item(
            row=4,
            col=1,
            item=self.test_button,
            align="centre"
        )

        self.logo = StaticImage(
            image_path=Paths.DRUVER_BIG_LOGO
        )
        self.grid.add_item(
            row=1,
            col=1,
            item=self.logo,
            align="centre",
            padding="top 25"
        )

        self.add_item(self.grid)
