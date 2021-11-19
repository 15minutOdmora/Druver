"""
Module containing the loading page that appears when loading assets.
"""

import pygame

from game.gui.text import CustomText, Text
from game.gui.bar import LoadingBar


class LoadingPage:
    """
    Loading page gets displayed and updated when loading assets, it has an update method which will update and draw
    self to screen when called, this method should be passed to loading functions/methods for updating this page.
    """
    def __init__(self, total_calls: int = 0):
        """
        :param total_calls: int number representing total number of calls to the update method, used for updating
                            progress and loading bar(if added)
        """
        self.screen = pygame.display.get_surface()

        self.total_calls = total_calls
        self.current_calls = 0

        self.title = Text(
            text="Loading ...",
            position=[200, 280],
            size=100
        )

        self.loading_text = Text(
            text="Loading",
            position=[200, 425],
            size=26
        )
        self.loading_bar = LoadingBar(
            position=[200, 400],
            size=[880, 20]
        )

    def add_calls(self, to_add: int) -> None:
        """
        Method adds a number of calls to the total_calls variable, when update is called the total number of calls
        represents the 100% of loading.
        :param to_add: int number of calls to add
        """
        self.total_calls += to_add

    def update(self, message: str = "") -> None:
        """
        Method updates self items, progress and calls the draw method for self.
        :param message: str message to be displayed when loading (used for displaying what is currently loading)
        """
        self.current_calls += 1
        self.loading_bar.update_progress(round(self.current_calls / self.total_calls, 2))
        self.loading_text.text = message
        self.loading_text.update()
        self.draw()

    def draw(self) -> None:
        """
        Method draws self and all items to the screen and it also updates the display so the game does not freeze.
        """
        self.screen.fill((0, 0, 0))
        self.loading_bar.draw()
        self.loading_text.draw()
        self.title.draw()
        pygame.display.update()
