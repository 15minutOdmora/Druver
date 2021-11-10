"""
Page for the selection of map, car and other game related options.
"""

import pygame

from game.helpers import helpers
from game.pages.page import ScrollablePage, Page
from game.constants import Paths, DEVELOPMENT_URL
from game.gui.text import CustomText, Text
from game.gui.button import Button
from game.gui.image import StaticImage
from game.gui.grid import Grid
from game.gui.carousel import HorizontalCarousel
from game.gui.container import Container


class PlayerSelectionPage(Page):
    def __init__(self, controller):
        super().__init__(controller)

        # Title
        self.title = CustomText(
            text="Page 1",
            size=72
        )

        self.add_item(self.title)

        # Carousel
        self.carousel = HorizontalCarousel(
            self.controller,
            item_size=[200, 300],
            position=[100, 200],
            size=[1000, 300]
        )
        for i in range(4):
            cont = Container(
                position=[0, 0],
                size=[200, 300],
                visible=True
            )
            cont.add_item(
                item=Text(text=str(i), size=20),
                relative_position=[50, 50]
            )
            cont.add_item(
                item=Text(text=str(i), size=20),
                relative_position=[50, 100]
            )
            self.carousel.add_item(cont)
        self.add_item(self.carousel)

        self.scroll_left_button = Button(
            self.controller,
            [100, 600],
            (100, 40),
            on_click=helpers.create_callable(self.carousel.scroll_left),
            text="Left"
        )
        self.add_item(self.scroll_left_button)

        self.scroll_right_button = Button(
            self.controller,
            [200, 600],
            (100, 40),
            on_click=helpers.create_callable(self.carousel.scroll_right),
            text="Right"
        )
        self.add_item(self.scroll_right_button)


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
