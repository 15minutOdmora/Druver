"""
Page for the selection of map, car and other game related options.
"""

import pygame

from game.helpers import helpers
from game.pages.page import ScrollablePage, Page
from game.constants import Paths, DEVELOPMENT_URL, SCREEN_SIZE
from game.gui.text import CustomText, Text
from game.gui.button import Button
from game.gui.image import StaticImage
from game.gui.grid import Grid
from game.gui.carousel import HorizontalCarousel
from game.gui.container import Container


half_screen = SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2


class PlayerSelectionPage(Page):
    def __init__(self, controller):
        super().__init__(controller)

        # Title
        self.title = CustomText(
            text="Select Car",
            size=72,
        )
        self.add_item(self.title)

        # Carousel
        self.carousel = HorizontalCarousel(
            self.controller,
            item_size=[300, 500],
            position=[0, 50],
            size=[1280, 400],
            spacing=30
        )
        self.carousel.not_selected_item_resize_factor = 0.4
        self.carousel.visible = False
        for i in range(8):
            cont = Container(
                position=[0, 0],
                size=[300, 500],
                visible=True,
                resizable=True
            )
            cont.add_item(
                item=CustomText(text="Car: " + str(i), size=80),
                relative_position=[50, 50]
            )
            self.carousel.add_item(cont)
        self.add_item(self.carousel)

        self.scroll_left_button = Button(
            self.controller,
            [20, half_screen[1] - 50],
            size=(20, 100),
            on_click=helpers.create_callable(self.carousel.scroll_left),
            text=""
        )
        self.add_item(self.scroll_left_button)

        self.scroll_right_button = Button(
            self.controller,
            [1240, half_screen[1] - 50],
            size=(20, 100),
            on_click=helpers.create_callable(self.carousel.scroll_right),
            text=""
        )
        self.add_item(self.scroll_right_button)


class MapSelectionPage(Page):
    def __init__(self, controller):
        super().__init__(controller)

        # Title
        self.title = CustomText(
            text="Select Map",
            size=72,
        )
        self.add_item(self.title)

        # Carousel
        self.carousel = HorizontalCarousel(
            self.controller,
            item_size=[450, 500],
            position=[0, 50],
            size=[1280, 400],
            spacing=30
        )
        self.carousel.visible = False
        for i in range(8):
            cont = Container(
                position=[0, 0],
                size=[450, 500],
                visible=True,
                resizable=True
            )
            cont.add_item(
                item=CustomText(text="Map: " + str(i), size=80),
                relative_position=[50, 50]
            )
            self.carousel.add_item(cont)
        self.add_item(self.carousel)

        self.scroll_left_button = Button(
            self.controller,
            [40, half_screen[1] - 50],
            size=(20, 100),
            on_click=helpers.create_callable(self.carousel.scroll_left),
            text=""
        )
        self.add_item(self.scroll_left_button)

        self.scroll_right_button = Button(
            self.controller,
            [1220, half_screen[1] - 50],
            size=(20, 100),
            on_click=helpers.create_callable(self.carousel.scroll_right),
            text=""
        )
        self.add_item(self.scroll_right_button)


class SelectionPage(ScrollablePage):
    def __init__(self, controller):
        super().__init__(controller)
        # Todo add scroller button thingy on the right side of screen
        self.player_selection_page = PlayerSelectionPage(controller)
        self.add_page(self.player_selection_page)
        self.map_selection_page = MapSelectionPage(controller)
        self.add_page(self.map_selection_page)

        self.scroll_speed = 6

        self.player_selection_page.add_item(
            Button(
                self.controller,
                [1000, SCREEN_SIZE[1] - 100],
                size=(130, 40),
                on_click=helpers.create_callable(self.scroll_one_down),
                text="Continue"
            )
        )
        self.map_selection_page.add_item(
            Button(
                self.controller,
                [1000, SCREEN_SIZE[1] - 160],
                size=(140, 40),
                on_click=helpers.create_callable(self.scroll_one_up),
                text="Go back"
            )
        )
        self.map_selection_page.add_item(
            Button(
                self.controller,
                [1000, SCREEN_SIZE[1] - 100],
                size=(160, 40),
                on_click=helpers.create_callable(self.controller.redirect_to_page, "TimeTrial"),
                text="Save and play"
            )
        )
