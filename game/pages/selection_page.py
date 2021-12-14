"""
Page for the selection of map, car and other game related options.
"""

import pygame

from game.helpers import helpers
from game.pages.page import ScrollablePage, Page
from game.constants import Paths, DEVELOPMENT_URL, SCREEN_SIZE
from game.gui.text import CustomText, Text
from game.gui.button import Button
from game.gui.image import StaticImage, ResizableImage, RotatingImages
from game.gui.grid import Grid
from game.gui.carousel import HorizontalCarousel
from game.gui.container import Container
from game.helpers.file_handling import DirectoryReader


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
            item_size=[310, 400],
            position=[0, 50],
            size=[1280, 400],
            spacing=30
        )
        self.carousel.not_selected_item_resize_factor = 0.4
        self.carousel.visible = False
        car_previews = DirectoryReader.get_car_previews()
        for car in car_previews:
            cont = Container(
                position=[0, 0],
                size=[310, 400],
                visible=False,
                resizable=True
            )
            cont.add_item(
                item=CustomText(text=car["name"], size=80),
                relative_position=[25, 25]
            )
            cont.add_item(
                item=RotatingImages(car["preview"]),
                relative_position=[5, 130]
            )
            self.carousel.add_item(cont, name=car["name"])
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

    def get_selected(self):
        return self.carousel.get_currently_selected()


class MapSelectionPage(Page):
    def __init__(self, controller):
        super().__init__(controller)

        # Title
        self.title = Text(
            text="Select Map",
            size=72,
        )
        self.add_item(self.title)

        # Carousel
        self.carousel = HorizontalCarousel(
            self.controller,
            item_size=[400, 500],
            position=[0, 50],
            size=[1280, 400],
            spacing=30
        )
        self.carousel.visible = False
        for i in range(8):
            cont = Container(
                position=[0, 0],
                size=[400, 500],
                visible=True,
                resizable=True
            )
            cont.add_item(
                item=CustomText(text="Map: " + str(i), size=80),
                relative_position=[30, 10]
            )
            cont.add_item(
                item=ResizableImage(
                    image_path="game/assets/maps/Mugello Dessert/preview.png"
                ),
                relative_position=[20, 100]
            )
            self.carousel.add_item(cont, name="Mugello Dessert")  # Todo: Make for different maps
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

    def get_selected(self):
        return self.carousel.get_currently_selected()


class SelectionPage(ScrollablePage):
    def __init__(self, controller, to_game_mode: str = "TimeTrial"):
        super().__init__(controller)

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
                on_click=helpers.create_callable(
                    self.controller.redirect_to_page,
                    to_game_mode,
                    map_name=helpers.create_callable(self.map_selection_page.get_selected),
                    car_name=helpers.create_callable(self.player_selection_page.get_selected)
                ),
                text="Save and play"
            )
        )
