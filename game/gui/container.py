"""
Module containing container classes,
Containers are StaticItems which contain other items. What makes container useful is that we can bundle multiple items
in a single container and place / move that container around.
Added items in the container should be added with the position relative to the containers position.
"""

import pygame

from game.constants import BaseColors
from game.gui.item import StaticItem


class Container(StaticItem):
    """
    Base abstract class for defining Items. This includes the needed methods / attributes.
    """

    def __init__(self, position: list[int] = [0, 0], size: tuple[int] = (100, 100), visible: bool = False):
        super().__init__(position, size, visible)

        self.items_positions: list[tuple] = []  # List containing attached items positions

    def add_item(self, item: any, relative_position: tuple[int]) -> int:
        """
        Method adds item to self, on given position. Returns items position index in lists.
        """
        self.items.append(item)
        item_position = (self.position[0] + relative_position[0], self.position[1] + relative_position[1])
        self.items_positions.append(item_position)
        self.items[-1].position = item_position  # Update this items position
        return len(self.items) - 1

    def change_item_at_index(self, index: int, item: any) -> None:
        """
        Method changes items in its list of items, but keeps previous items position.

        Args:
            index (int): Index of previous item in list
            item (Item): Any kind of item
        """
        self.items[index] = item
        self.items[index].position = self.items_positions[index]

    def update(self):
        """
        Updates all items positions. TODO: Items positions get assigned every time.
        """
        for i, item in enumerate(self.items):
            # Update items positions relative to current self position
            item.position = [self.x + self.items_positions[i][0], self.y + self.items_positions[i][1]]
            item.update()

    def draw(self):
        """ Used for drawing itself and every item attached to it. """
        if self.visible:
            pygame.draw.rect(
                self.screen,
                BaseColors.items,
                self.rect,
                width=1
            )
        for item in self.items:
            item.draw()
