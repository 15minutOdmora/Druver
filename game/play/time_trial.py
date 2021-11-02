"""
Time trial module, has TimeTrial class that is similar to Page classes but items can't be added to it.
"""

from game.play.game_objects.map import Map
from game.play.game_objects.player import Player
from game.play.game_objects.car import Car


class TimeTrial:
    """ Time trial class, similar to a page, as it has the draw and update methods, but has own logic."""
    def __init__(self, controller):
        self.controller = controller

        # Load map
        self.map = Map(
            self.controller,
            folder_name="testing_map"
        )
        # Load player
        self.car = Car(self.controller, "vasjacar")
        self.player = Player(self.controller, self.map, self.car, "Testing")

    def update(self):
        if not self.controller.paused:
            self.player.update()
            self.map.update()

    def draw(self):
        self.map.draw()
        self.player.draw()
