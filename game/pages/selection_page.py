"""
Page for the selection of map, car and other game related options.
"""

import pygame

from game.helpers import helpers
from game.pages.page import ScrollablePage, Page
from game.constants import Paths, DEVELOPMENT_URL
from game.gui.text import CustomText
from game.gui.button import Button
from game.gui.image import StaticImage
from game.gui.grid import Grid


class PlayerSelectionPage(Page):
    def __init__(self, controller):
        super().__init__(controller)

        # Title
        self.title = CustomText(
            text="Page 1",
            size=72
        )

        self.add_item(self.title)


class MapSelectionPage(Page):
    def __init__(self, controller):
        super().__init__(controller)

        # Title
        self.title = CustomText(
            text="Page 2",
            size=72
        )

        self.add_item(self.title)


class SelectionPage(ScrollablePage):
    def __init__(self, controller):
        super().__init__(controller)
        # Todo add scroller button thingy on the right side of screen
        self.add_page(PlayerSelectionPage(controller))
        self.add_page(MapSelectionPage(controller))
        self.add_page(TestPage(controller))
        self.add_page(TestPagee(controller))
        self.add_page(TestPageee(controller))
