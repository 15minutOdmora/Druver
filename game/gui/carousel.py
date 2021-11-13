"""
Module containing carousel items. A carousel is a container for items which can be selected.
Carousel holds items horizontally, has one item in front and two on each side, item scrolling is done with
a somewhat rounded movement.
"""

import pygame

from game.gui.item import Item


class HorizontalCarousel(Item):
    """
    Carousel class for holding items, acts as a selection sort of menu, has scrolling and re-sizing animations on items.
    All added items have to be of type Container with the resizable attribute set to true.
    All items should be of the same size, specified in the initialization of object.
    Currently visible items are based on the size of the carousel, items that pop outside of it are not drawn.
    Has methods scroll_left and scroll_right that can be used as on_click methods in buttons.
    """
    def __init__(
            self,
            controller,
            item_size: list[int, int],
            position: list[int, int] = [0, 0],
            size: list[int, int] = [1, 1],
            spacing: int = 0
            ):
        """
        :param controller: Controller main controller of game
        :param item_size: list[int, int] size of every item
        :param position: tuple[int, int] position of carousel on screen
        :param size: list[int, int] size of carousel, determines when items are visible
        :param spacing: int spacing(in px) between items horizontally
        """
        super().__init__(controller, position, size)
        self.item_size = item_size
        self.spacing = spacing  # Spacing between items

        # Centre position of item in self, subtract item size so item is centered
        self.center_position = [self.size[0] // 2 - item_size[0] // 2, 0]
        # Current index of selected item
        self.current_index = 0
        self.items_positions = []  # Relative position of items to self
        # Used in scrolling animation
        self.is_scrolling = False
        self.current_x = 0
        self.scroll_to_x = 0
        self.scroll_to_index = 0
        self.scroll_direction = 0
        self.scroll_speed = 3
        # Used in resizing animation
        self.not_selected_item_resize_factor = 0.2
        self.change_distance = self.item_size[0] + self.spacing

    def get_currently_visible_items(self) -> list[int]:
        """
        Method returns a list of indexes of currently visible items.
        :return: List of indexes[int] of currently visible items
        """
        visible = []
        for i in range(len(self.items)):
            item_pos = self.center_position[0] + self.current_x + (self.item_size[0] + self.spacing) * i
            if self.x - self.item_size[0] <= item_pos <= self.x + self.width:
                visible.append(i)
        return visible

    def scroll(self, change: int) -> None:
        """
        Method scrolls items by a given horizontal change
        :param change: int change in pixels, can be negative
        """
        self.current_x += change

    def scroll_right(self) -> None:
        """
        Method scrolls one item to the right, can be used for on_click methods in buttons.
        """
        if self.current_index == len(self.items) - 1 or self.is_scrolling:
            return
        self.scroll_to_index += 1
        self.scroll_to_x -= self.item_size[0] + self.spacing
        self.scroll_direction = -1
        self.is_scrolling = True

    def scroll_left(self) -> None:
        """
        Method scrolls one item to the left, can be used for on_click methods in buttons.
        """
        if self.current_index == 0 or self.is_scrolling:
            return
        self.scroll_to_index -= 1
        self.scroll_to_x += self.item_size[0] + self.spacing
        self.scroll_direction = 1
        self.is_scrolling = True

    def update_sizes(self, change_left: int) -> None:
        """
        Method updates sizes of all items based on their position (if being selected or un-selected).
        :param change_left: int change left for new item to be selected
        """
        normalized_change = abs(change_left / self.change_distance) * self.not_selected_item_resize_factor
        to_selected_resize_factor = round(1 - normalized_change, 2)
        to_unselected_resize_factor = round(1 - self.not_selected_item_resize_factor + normalized_change, 2)
        self.items[self.scroll_to_index].resize(to_selected_resize_factor)
        self.items[self.current_index].resize(to_unselected_resize_factor)

    def update_scrolling(self) -> None:
        """
        Method used internally for updating items positions based on scrolling change.
        """
        if self.is_scrolling:  # If scrolling by action of a button
            change_left = self.scroll_to_x - self.current_x
            if change_left == 0:
                self.is_scrolling = False
                self.items[self.current_index].selected = False  # Un-select previous item
                self.current_index = self.scroll_to_index
                self.items[self.current_index].selected = True
                self.items[self.current_index].reset_size()
            elif abs(change_left) < self.scroll_speed:
                self.scroll(change_left)
                self.update_sizes(change_left)
            else:
                self.scroll(self.scroll_speed * self.scroll_direction)
                self.update_sizes(change_left)

    def add_item(self, item) -> None:
        """
        Method adds one item to the list, items are containers containing items.
        Added container has to be re-sizable with te attribute resizable set to true.
        :param item: Container object
        """
        # Items get added one next to the other, first item is in the center of the carousel
        x_pos = self.position[0] + self.center_position[0] + ((self.item_size[0] + self.spacing) * len(self.items))
        self.items_positions.append([x_pos, self.y])
        self.items.append(item)
        if len(self.items) != 1:  # Leave first one in its full size
            self.items[-1].resize(1 - self.not_selected_item_resize_factor)

    def update(self) -> None:
        """
        Overwrite parent method. Update every items position and itself.
        """
        self.update_scrolling()
        for i, item in enumerate(self.items):          # self.current_index * self.item_size[0]
            item.position = [self.items_positions[i][0] + self.current_x, self.y]
            item.update()

    def draw(self) -> None:
        """
        Overwrite parent method of drawing. Draw every item and self if set to visible.
        """
        for index in self.get_currently_visible_items():
            self.items[index].draw()
        if self.visible:
            pygame.draw.rect(
                self.screen,
                (255, 255, 255),
                self.rect,
                2
            )
