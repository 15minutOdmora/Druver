"""
Time trial module, has TimeTrial class that is similar to Page classes but items can't be added to it.
"""

from game.constants import SCREEN_SIZE, Paths, join_paths
from game.play.game_objects.map import Map
from game.play.game_objects.player import Player
from game.play.game_objects.car import Car
from game.gui.menus import PauseMenu


class TimeTrial:
    """ Time trial class, similar to a page, as it has the draw and update methods, but has own logic."""
    def __init__(self, controller):
        self.controller = controller

        self.pause_menu = PauseMenu(
            position=[0, 0],
            size=SCREEN_SIZE
        )
        # Load map
        self.map = Map(
            self.controller,
            folder_name="Mugello Dessert"
        )
        # Load player
        self.car = Car(self.controller, "FastBoi")
        self.player = Player(self.controller, self.map, self.car, "Testing")

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
