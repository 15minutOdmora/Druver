"""
Abstract class definition for items that are defined in the gui package.
"""

from typing import Callable

import pygame


class Item:
    """
    Base class for clickable and hoverable items.
    """
    def __init__(self,
                 controller,
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

        self.controller = controller

        self.items: list[ActiveItem] = []  # List of items attached to self

        self.rect = pygame.Rect(position[0], position[1], size[0], size[1])

        self.hovered = False
        self.visible = True
        self.selected: bool = False

        self._on_click: Callable = on_click

    @property
    def position(self) -> list[int]:
        return [self.rect.x, self.rect.y]

    @position.setter
    def position(self, pos: list[int]):
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    @property
    def x(self) -> int:
        return self.rect.x

    @x.setter
    def x(self, new_x: int):
        self.rect.x = new_x

    @property
    def y(self) -> int:
        return self.rect.y

    @y.setter
    def y(self, new_y: int):
        self.rect.y = new_y

    @property
    def size(self) -> tuple[int, int]:
        return self.rect.size

    @size.setter
    def size(self, new_size: tuple[int, int]):
        self.rect.size = new_size

    @property
    def width(self):
        return self.rect.width

    @width.setter
    def width(self, new_width):
        self.rect.width = new_width

    @property
    def height(self):
        return self.rect.height

    @height.setter
    def height(self, new_height):
        self.rect.height = new_height

    def on_hover(self):
        # When mouse hovers item
        pass

    def on_click(self):
        # When mouse clicks on item
        self._on_click()

    def update(self):
        """ Used for updating all items attached to it(sizes, positions, etc.). """
        self.hovered = self.rect.collidepoint(self.controller.mouse_position)
        if self.hovered and self.controller.mouse_clicked:
            self.on_click()
        for item in self.items:
            item.update()

    def draw(self):
        """ Used for drawing itself and every item attached to it. """
        # Logic for drawing itself goes here
        for item in self.items:
            item.draw()


class StaticItem:
    """
    Base class for defining static items that do not move, or can have actions performed on them.
    The main difference between the Item class is the lack of on_hover / on_click methods, and that thsi class
    does not need the controller to be passed.
    These also do not include other items.
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

        self.rect = pygame.Rect(position[0], position[1], size[0], size[1])

        self.visible = True
        self.selected: bool = False

        self._on_click: Callable = on_click

    @property
    def position(self) -> list[int]:
        return [self.rect.x, self.rect.y]

    @position.setter
    def position(self, pos: list[int]):
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    @property
    def x(self) -> int:
        return self.rect.x

    @x.setter
    def x(self, new_x: int):
        self.rect.x = new_x

    @property
    def y(self) -> int:
        return self.rect.y

    @y.setter
    def y(self, new_y: int):
        self.rect.y = new_y

    @property
    def size(self) -> tuple[int, int]:
        return self.rect.size

    @size.setter
    def size(self, new_size: tuple[int, int]):
        self.rect.size = new_size

    @property
    def width(self):
        return self.rect.width

    @width.setter
    def width(self, new_width):
        self.rect.width = new_width

    @property
    def height(self):
        return self.rect.height

    @height.setter
    def height(self, new_height):
        self.rect.height = new_height

    def update(self):
        """ Used for updating all items attached to it(sizes, positions, etc.). """
        pass

    def draw(self):
        """ Used for drawing itseld and every item attached to it. """
        pass
