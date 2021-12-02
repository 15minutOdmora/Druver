"""
Time trial module, has TimeTrial class that is similar to Page classes but items can't be added to it.
"""

import pygame

from game.constants import SCREEN_SIZE, Paths, join_paths
from game.play.game_objects.map import Map
from game.play.game_objects.player import Player
from game.play.game_objects.car import Car
from game.helpers.helpers import create_callable
from game.gui.menus import PauseMenu
from game.gui.button import Button
from game.gui.text import CustomText
from game.pages.loading_page import LoadingPage
from game.pages.welcome_page import WelcomePage


class TimeTrial:
    """
    Time trial class, similar to a page, as it has the draw and update methods, but has own logic.
    """
    def __init__(self, controller, map_name=lambda: "Mugello Dessert", car_name=lambda: "Sandal"):
        self.controller = controller
        self.map_name = map_name()
        self.car_name = car_name()

        self.pause_menu = PauseMenu(
            position=[0, 0],
            size=SCREEN_SIZE
        )
        self.pause_menu.add_item(
            item=Button(
                self.controller,
                position=[SCREEN_SIZE[0] // 2 - 20, SCREEN_SIZE[1] // 2 - 75],
                size=[150, 40],
                text="Quit",
                on_click=create_callable(self.controller.go_back_to, WelcomePage)
            )
        )
        # Create temporary loading page
        self.loading_page = LoadingPage()
        # Load map
        self.map = Map(
            self.controller,
            folder_name=self.map_name
        )
        # Load player
        self.car = Car(
            self.controller,
            current_map=self.map,
            car_name=self.car_name,
            initial_position=[2050, 1650]
        )
        self.player = Player(self.controller, self.map, self.car, "Testing")
        # Update number of total update calls to loading page
        self.loading_page.add_calls(self.map.get_number_of_loading_update_calls())
        self.map.load(self.loading_page.update)  # Pass update method to update loading_page data and screen

    def update(self):
        if not self.controller.paused:
            self.player.update()
            self.map.update()
            self.pause_menu.visible = False
        else:
            self.pause_menu.visible = True
            self.pause_menu.update()

    def draw(self):
        self.map.draw()
        self.player.draw()
        self.pause_menu.draw()
