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

        self.initial_position = position  # Save initial position
        self.rect = pygame.Rect(position[0], position[1], size[0], size[1])

        self.hovered = False
        self.visible = False
        self.selected: bool = False

        self._on_click: Callable = on_click
        self.last_click_time = 0  # Time of last click
        self.debounce_interval = 100  # Minimum milliseconds passed since last click to accept next click

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
    def width(self) -> int:
        return self.rect.width

    @width.setter
    def width(self, new_width: int) -> None:
        self.rect.width = new_width

    @property
    def height(self) -> int:
        return self.rect.height

    @height.setter
    def height(self, new_height: int) -> None:
        self.rect.height = new_height

    def debounce_time(self) -> bool:
        """
        Method checks if enough(debounce_interval) time passed from the time of the last click.
        Used for eliminating double clicks.
        :return: bool if enough time passed or not
        """
        return pygame.time.get_ticks() - self.last_click_time >= self.debounce_interval

    def reset_position(self) -> None:
        """
        Method resets items position to its initial one.
        """
        self.position = self.initial_position

    def on_hover(self):
        # When mouse hovers item
        pass

    def on_click(self):
        # When mouse clicks on item
        self._on_click()

    def update(self):
        """ Used for updating all items attached to it(sizes, positions, etc.). """
        self.hovered = self.rect.collidepoint(self.controller.mouse_position)
        if self.hovered and self.controller.mouse_clicked and self.debounce_time():
            self.last_click_time = pygame.time.get_ticks()
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
    The main difference between the Item class is the lack of on_hover / on_click methods, and that this class
    does not need the controller to be passed.
    Items can not be attached to this class.
    """
    def __init__(self,
                 position=[0, 0],
                 size=(1, 1),
                 visible: bool = True
                 ):
        """
        :param position: list[int] -> Position of item on screen
        :param size: tuple[int] -> Size of item
        :param on_click: Callable -> Function to call when item is clicked
        """
        self.screen = pygame.display.get_surface()

        self.items = []

        self.initial_position = position
        self.rect = pygame.Rect(position[0], position[1], size[0], size[1])

        self.visible = visible
        self.selected: bool = False

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
    def width(self) -> int:
        return self.rect.width

    @width.setter
    def width(self, new_width: int) -> None:
        self.rect.width = new_width

    @property
    def height(self) -> int:
        return self.rect.height

    @height.setter
    def height(self, new_height: int) -> None:
        self.rect.height = new_height

    def reset_position(self) -> None:
        """
        Method resets items position to its initial one.
        """
        self.position = self.initial_position

    def add_item(self, item: any, *args) -> None:
        """
        Method adds item to self.
        :param item: Item -> Any item that has the update and draw methods
        """
        self.items.append(item)

    def update(self):
        """ Used for updating all items attached to it(sizes, positions, etc.). """
        for item in self.items:
            item.update()

    def draw(self):
        """ Used for drawing itself and every item attached to it. """
        if self.visible:
            for item in self.items:
                item.draw()
