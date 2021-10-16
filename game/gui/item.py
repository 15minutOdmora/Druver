"""
Abstract class definition for items that are defined in the gui package.
"""

from typing import Callable


class Item(ABC):
    """
    Base abstract class for defining Items. This includes the needed methods / attributes.
    """
    def __init__(self,
                 position=[0, 0],
                 size=(1, 1),
                 on_click: Callable = lambda: None
                 ):
        """
        :param position: list[int] -> Position of item on screen
        :param size: tuple[int] -> Size of item
        :param on_click: Callable -> Function to call when item is clicked
        """
        self.screen = pygame.display.get_surface()

        self.items: list[ActiveItem] = []  # List of items attached to self

        self.position = position

        self.size: size  # Some size, or function that fetches the size
        self.width, self.height = self.size

        self.selected: bool = False

        self._on_click: func = on_click

    def on_hover(self):
        # When mouse hovers item
        pass

    def on_click(self):
        # When mouse clicks on item
        self._on_click()

    def update(self):
        """ Used for updating all items attached to it(sizes, positions, etc.). """
        for item in self.items:
            item.update()

    def draw(self):
        """ Used for drawing itseld and every item attached to it. """
        # Logic for drawing itself goes here
        for item in self.items:
            item.draw()
