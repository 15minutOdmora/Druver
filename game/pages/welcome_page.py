"""
Welcome page loads when the game is ran.
"""

import webbrowser

import pygame

from game.helpers import helpers
from game.pages.page import Page
from game.constants import Paths, DEVELOPMENT_URL
from game.gui.text import CustomText, Text
from game.gui.button import Button, AnimatedButton
from game.gui.image import StaticImage
from game.gui.grid import Grid


class WelcomePage(Page):
    def __init__(self, controller):
        super().__init__(controller)
        # Page grid
        self.grid = Grid(
            rows=10,
            columns=3,
            visible=False
        )
        # Logo on top of page
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
        # Start game button
        self.test_button = Button(
            self.controller,
            size=(180, 50),
            text=Text(
                text="Start Game",
                size=36
            ),
            on_click=helpers.create_callable(self.controller.redirect_to_page, "StartGamePage")
        )
        self.grid.add_item(
            row=4,
            col=1,
            item=self.test_button,
            align="centre"
        )
        # Settings button
        self.settings_button = Button(
            self.controller,
            size=(180, 50),
            text=Text(
                text="Settings",
                size=36
            )
        )
        self.grid.add_item(
            row=5,
            col=1,
            item=self.settings_button,
            align="centre"
        )
        # Credits button
        self.credits_button = Button(
            self.controller,
            size=(180, 50),
            text=Text(
                text="Credits",
                size=36
            )
        )
        self.grid.add_item(
            row=6,
            col=1,
            item=self.credits_button,
            align="centre"
        )
        # Web page button, on_click gets passed a callable that opens the page on the current browser
        self.web_page_button = Button(
            self.controller,
            size=(180, 50),
            text=Text(
                text="Web Page",
                size=36
            ),
            on_click=helpers.create_callable(
                webbrowser.open,
                DEVELOPMENT_URL,
                new=0,
                autoraise=True
            )
        )
        self.grid.add_item(
            row=7,
            col=1,
            item=self.web_page_button,
            align="centre"
        )
        # At end append grid
        self.add_item(self.grid)
