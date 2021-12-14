"""
Module containing container classes,
Containers are StaticItems which contain other items. What makes container useful is that we can bundle multiple items
in a single container and place / move that container around and it moves contained items automatically.
Added items in the container should be added with the position relative to the containers position.
"""

import pygame

from game.constants import BaseColors
from game.gui.item import ResizableItem


class Container(ResizableItem):
    """
    Base abstract class for defining Items. This includes the needed methods / attributes.
    Container can be re-sized to given given size using methods, has option for size to be reset to initial.
    Once the container is resized so are all items contained in it.
    """
    def __init__(self,
                 position: list[int, int] = [0, 0],
                 size: tuple[int, int] = (100, 100),
                 resizable: bool = False
                 ):
        """
        :param position: list[int, int] position of container on screen. Is changeable
        :param size: tuple[int, int] size of container
        :param visible: bool if container is visible, development and testing purpose
        :param resizable: bool if container can be re-sized
        """
        super().__init__(position, size)

        self.resizable = resizable

        self.items_positions: list[tuple] = []  # List containing attached items positions
        self.resized_items_positions: list[tuple] = []

    def resize(self, factor: float) -> None:
        """
        Method re-sizes self and every item inside by a factor passed as an argument.
        :param factor: float representing scale to resize in the interval [0, inf]
        """
        super(Container, self).resize(factor)
        self.resized_size = [int(self.width * factor), int(self.height * factor)]
        for i, item in enumerate(self.items):  # Re-size and scale items positions based on factor
            self.resized_items_positions[i] = [int(self.items_positions[i][0] * factor),
                                               int(self.items_positions[i][1] * factor)]
            item.resize(factor)

    def reset_size(self) -> None:
        """
        Method resets size of self anf every item to the initial size.
        """
        super(Container, self).reset_size()
        self.size = self.initial_size  # Reset size of self rect
        for item in self.items:
            item.reset_size()

    def add_item(self, item: any, relative_position: tuple[int]) -> int:
        """
        Method adds item to self, on given position. Returns items position index in lists.
        :param item: Item to add
        :param relative_position: tuple[int] position to add item on, relative to self position
        :return: int index of item on self list
        """
        if self.resizable and not hasattr(item, "is_resized"):  # If container resizable, expect only resizable items
            raise ValueError("Container.add_item: Container is set to be resizable and only accepts resizable items.")
        self.items.append(item)
        item_position = [relative_position[0], relative_position[1]]
        self.items_positions.append(item_position)
        self.resized_items_positions.append(item_position)
        self.items[-1].position = item_position  # Update this items position
        return len(self.items) - 1

    def change_item_at_index(self, index: int, item: any) -> None:
        """
        Method changes items in its list of items, but keeps previous items position.
        :param index: int index of item position in list
        :param item: any type of item(Static, Resizable, ...)
        """
        self.items[index] = item
        self.items[index].position = self.items_positions[index]

    def update(self) -> None:
        """
        Updates all items positions relative to self. TODO: Items positions get assigned every time.
        """
        for i, item in enumerate(self.items):
            # Update items positions relative to current self position
            item.position = [self.scaled_x + self.resized_items_positions[i][0],
                             self.scaled_y + self.resized_items_positions[i][1]]
            item.selected = self.selected
            item.update()

    def draw(self) -> None:
        """
        Used for drawing itself and every item attached to it.
        """
        if self.visible:
            if self.is_resized:
                pygame.draw.rect(
                    self.screen,
                    BaseColors.items,
                    [self.scaled_x, self.scaled_y, self.resized_size[0], self.resized_size[1]],
                    width=1
                )
            else:
                pygame.draw.rect(
                    self.screen,
                    BaseColors.items,
                    self.rect,
                    width=1
                )
        for item in self.items:
            item.draw()
