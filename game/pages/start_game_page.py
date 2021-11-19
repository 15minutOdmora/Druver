"""
Page for starting new game, has options for type of game play = time trial, levels, ... etc.
"""

import pygame

from game.helpers import helpers
from game.pages.page import Page
from game.constants import Paths, DEVELOPMENT_URL
from game.gui.text import CustomText, Text
from game.gui.button import Button
from game.gui.image import StaticImage
from game.gui.grid import Grid


class StartGamePage(Page):
    def __init__(self, controller):
        super().__init__(controller)

        # Page grid
        self.grid = Grid(
            rows=10,
            columns=3,
            visible=False
        )
        # Title
        self.title = Text(
            text="Start Game",
            size=72
        )
        self.grid.add_item(
            row=1,
            col=1,
            item=self.title,
            align="centre"
        )
        # Back button
        self.back_button = Button(
            controller=self.controller,
            size=(60, 40),
            text=Text(
                text="Back",
                size=36
            ),
            on_click=helpers.create_callable(self.controller.go_back)
        )
        self.grid.add_item(
            row=0,
            col=0,
            item=self.back_button,
            align="top left",
            padding="top 10, left 10"
        )
        # Time trial button
        self.time_trial_button = Button(
            controller=self.controller,
            size=(150, 60),
            text=Text(
                text="Time Trial",
                size=36
            ),
            on_click=helpers.create_callable(self.controller.redirect_to_page, "SelectionPage")
        )
        self.grid.add_item(
            row=3,
            col=1,
            item=self.time_trial_button,
            align="centre"
        )
        # Levels button TODO: Add redirection
        self.levels_button = Button(
            controller=self.controller,
            size=(150, 60),
            text=Text(
                text="Levels",
                size=36
            )
        )
        self.grid.add_item(
            row=4,
            col=1,
            item=self.levels_button,
            align="centre"
        )
        # Add grid to page
        self.add_item(self.grid)
