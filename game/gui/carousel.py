"""
Module containing carousel items. A carousel is a container for items which can be selected.
Carousel holds items horizontally, has one item in front and two on each side, item scrolling is done with
a somewhat rounded movement.
"""

import pygame

from game.gui.item import Item


class HorizontalCarousel(Item):
    def __init__(
            self,
            controller,
            item_size: list[int, int],
            position: list[int, int] = [0, 0],
            size: list[int, int] = [1, 1],
            ):
        super().__init__(controller, position, size)
        self.item_size = item_size
        # Centre position of item in self, subtract item size so item is centered
        self.center_position = [self.size[0] // 2 - item_size[0] // 2, 0]

        self.current_index = 0
        self.items_positions = []  # Relative position of items to self

    def __get_currently_visible_items(self) -> list[int]:
        """
        Method returns the indexes of currently visible items.
        :return: List of indexes[int]
        """
        pass

    def scroll_right(self):
        self.current_index = min(len(self.items) - 1, self.current_index + 1)

    def scroll_left(self):
        self.current_index = max(0, self.current_index - 1)

    def add_item(self, item) -> None:
        """
        Method adds one item to the list, items are containers containing items.
        Items get added as containers as containers are easy to move.
        :param item: Container object
        """
        # Items get added one next to the other, first item is in the center of the carousel
        x_pos = self.position[0] + self.center_position[0] + (self.item_size[0] * len(self.items))
        self.items_positions.append([x_pos, self.y])
        self.items.append(item)

    def update(self) -> None:
        """
        Overwrite parent method.
        """
        for i, item in enumerate(self.items):
            item.position = [self.items_positions[i][0] - self.current_index * self.item_size[0], self.y]
            item.update()

    def draw(self) -> None:
        """
        Overwrite parent method of drawing.
        """
        for item in self.items:
            item.draw()
        if self.visible:
            pygame.draw.rect(
                self.screen,
                (255, 255, 255),
                self.rect,
                2
            )
