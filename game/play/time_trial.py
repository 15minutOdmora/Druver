"""
Time trial module, has TimeTrial class that is similar to Page classes but items can't be added to it.
"""


class TimeTrial:
    """ Time trial class, similar to a page, as it has the draw and update methods, but has own logic."""
    def __init__(self, controller):
        self.controller = controller
        self.game = self.controller.game
        # Load player
        # Load map
        # Load timer
        pass

    def update(self):
        pass

    def draw(self):
        pass
