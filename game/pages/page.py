"""
Abstract class definition for all pages to follow.
"""

import math

import pygame

from game.gui.button import Button
from game.helpers.helpers import create_callable


class Page:
    def __init__(self, controller):
        self.screen = pygame.display.get_surface()
        self.controller = controller
        self.items = []
        self.items_positions = []  # Positions relative to the top left corner of page
        self.background_color = (0, 0, 0)
        size = self.screen.get_size()
        self.rect = pygame.Rect(0, 0, size[0], size[1])  # Initial position at (0, 0)

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

    def add_item(self, item: any):
        self.items.append(item)
        self.items_positions.append(item.position)

    def update(self):
        for i, item in enumerate(self.items):
            x = self.x + self.items_positions[i][0]
            y = self.y + self.items_positions[i][1]
            item.position = [x, y]
            item.update()

    def draw(self):
        for item in self.items:
            item.draw()


class ScrollablePage:
    """
    Scrollable Page is a longer(in height) page that can be scrolled up and down.
    You add pages to it, each added page is below the previously added page.
    Items can be added to it(as it is a page after all) which will be displayed on top of everything.
    """
    def __init__(self, controller):
        self.screen = pygame.display.get_surface()
        self.screen_size = self.screen.get_size()
        self.controller = controller
        self.items = []
        self.pages = []
        self.pages_positions = []
        self.currently_visible_pages = []

        self.current_height = 0  # y - pos of current upper left corner of screen on this long page
        self.scroll_move_by_wheel_input = 50  # Movement of one input from mouse wheel

        self.is_scrolling = False
        self.scroll_to_height = 0
        self.scroll_direction = 0
        self.scroll_speed = 12
        # Create movable scrolling button as
        self.scrolling_button = Button(
            self.controller,
            position=[self.screen_size[0] - 20, 0],
            size=[16, 100],
            on_click=create_callable(self.move_scrolling_button),
            movable=True
        )
        self.add_item(self.scrolling_button)

    @property
    def height(self) -> int:
        """
        Property returns the total height of page(number of pages * page height).
        :return: Integer number representing total height og page in px
        """
        return len(self.pages) * self.screen_size[1]  # Height of one screen is the same as one pages height

    @property
    def number_of_pages(self) -> int:
        """
        Property returns the amount of pages attached to self.
        :return: Integer number of pages
        """
        return len(self.pages)

    def scroll(self, change: int) -> None:
        """
        Method scrolls the page up(+int) or down(-int) for an amount of pixels.
        :param change: Integer value of the amount of pixels to move
        """
        # Boundaries of current_height are [0, height - screen_height] as it determines the upper left corner
        self.current_height = min(self.height - self.screen_size[1], max(0, self.current_height + change))
        self.controller.mouse_scroll = 0  # TODO this has to be reset to 0 here
        self.scrolling_button.y = int(self.current_height // self.number_of_pages)

    def scroll_to(self, index: int) -> None:
        """
        Method scrolls to page on given index.
        Note: If page is currently scrolling down, method call has no effect.
        :param index: Index of page in list to scroll to.
        """
        if index > len(self.pages) - 1:
            raise ValueError(f"ScrollablePage.scroll_to: Index {index} is out of range.")
        elif self.is_scrolling:  # If already scrolling => to_height was already set
            return
        else:
            self.scroll_to_height = self.pages_positions[index][1]  # Get height of page
            self.scroll_direction = math.copysign(1, self.scroll_to_height - self.current_height)
            self.is_scrolling = True

    def scroll_one_down(self) -> None:
        """
        Method scrolls one page down.
        """
        # Get current page index
        current_index = self.currently_visible_pages[0]  # We know it is the first one
        if current_index >= len(self.pages) - 1:
            self.scroll_to(current_index)
        else:
            self.scroll_to(current_index + 1)

    def scroll_one_up(self) -> None:
        """
        Method scrolls one page up.
        """
        # Get current page index
        current_index = self.currently_visible_pages[0]  # We know it's the first index
        if current_index <= 1:
            self.scroll_to(0)
        else:
            self.scroll_to(current_index - 1)

    def get_visible_pages(self) -> list[int, int]:
        """
        Method returns a list of currently visible pages on screen.
        If current_height = 0 -> returns [0, 1], always adds the page underneath.
        :return: List of indexes of pages in the self.pages list
        """
        current = int(self.current_height // self.screen_size[1])  # Current page the current_height is on
        visible = [current]
        if current < len(self.pages) - 1:  # If there is more pages append next index as it is probably visible
            visible.append(current + 1)
        return visible

    def move_scrolling_button(self) -> None:
        """
        Method gets converted into callable for on_click function in scrolling_button.
        Method updates scrolling buttons position on screen based on change of mouse movement.
        """
        change = self.controller.mouse_movement[1]
        self.scrolling_button.y = min(max(self.scrolling_button.y + change, 0),
                                      self.screen_size[1] - self.scrolling_button.height)

    def update_scrolling_button_data(self) -> None:
        """
        Method updates current page height based on scrolling_button height.
        """
        self.current_height = self.number_of_pages * self.scrolling_button.y

    def add_page(self, page: Page) -> None:
        """
        Method adds page to self, it gets added at the bottom of all current pages.
        :param page: Page to add
        """
        self.pages_positions.append([0, self.height])  # Add page at current height
        self.pages.append(page)
        # Update scrolling buttons height based on number of pages
        self.scrolling_button.height = int(self.screen_size[1] // len(self.pages))

    def add_item(self, item: any) -> None:
        """
        Method adds item to self as a page, these items positions do not change, so they stay static when page scrolling.
        :param item: Any item of either type Item or Static
        """
        self.items.append(item)

    def update_scroll(self):
        """
        Method checks if mouse was clicked and moves the page in that direction.
        """
        if self.is_scrolling:  # If scrolling by action of a button
            change_left = self.scroll_to_height - self.current_height
            if change_left == 0:
                self.is_scrolling = False
            elif abs(change_left) < self.scroll_speed:
                self.scroll(self.scroll_direction * change_left)
            else:
                self.scroll(self.scroll_direction * self.scroll_speed)
        elif self.controller.mouse_scroll != 0:  # If scrolling with roller
            self.scroll(-self.controller.mouse_scroll * self.scroll_move_by_wheel_input)
        else:
            self.update_scrolling_button_data()

    def update(self) -> None:
        """
        Method updates all of the items attached to self along with every page and its position.
        """
        # First update items attached to self, they have priority with clicks
        for item in self.items:
            item.update()
        self.update_scroll()
        # Update positions of visible pages and the pages them self
        self.currently_visible_pages = self.get_visible_pages()
        for i in self.currently_visible_pages:
            page, position = self.pages[i], self.pages_positions[i]
            page.position = [0, position[1] - self.current_height]
            page.update()

    def draw(self) -> None:
        """
        Method draws the currently visible pages.
        """
        # First draw pages
        for i in self.currently_visible_pages:
            self.pages[i].draw()
        for item in self.items:
            item.draw()
