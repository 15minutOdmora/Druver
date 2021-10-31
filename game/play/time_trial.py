"""
Time trial module, has TimeTrial class that is similar to Page classes but items can't be added to it.
"""

from game.play.game_objects.map import Map
from game.play.game_objects.player import Player


class TimeTrial:
    """ Time trial class, similar to a page, as it has the draw and update methods, but has own logic."""
    def __init__(self, controller):
        self.controller = controller
        self.game = self.controller.game

        # Load map
        self.map = Map(
            game=self.game,
            folder_name="testing_map"
        )
        # Load player
        self.player = Player(self.game, self.map, "Testing")

    def update(self):
        if not self.game.paused:
            self.player.update()
            self.map.update()

    def draw(self):
        self.map.draw()
        self.player.draw()
