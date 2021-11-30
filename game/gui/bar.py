"""
Module for Bar classes.
"""

import pygame

from game.gui.item import StaticItem, Item
from game.gui.text import Text


class LoadingBar(StaticItem):
    """
    LoadingBar item is a rectangle which displays progress on screen by filling up.
    Has update_progress method where you can pass current progress as a float in the interval [0, 1],
    this method automatically updates self object.
    """
    def __init__(self,
                 position: list[int, int] = [0, 0],
                 size: tuple[int, int] = (1, 1),
                 visible: bool = True,
                 color: tuple[int] = (255, 255, 255),
                 line_width: int = 3
                 ):
        """
        :param position: list[int, int] position of bar on screen
        :param size: tuple[int, int] total size of bar
        :param visible: bool if bar visible
        :param color: tuple[int, int, int] color of bar
        :param line_width: int width of one rectangle lines
        """
        super().__init__(position, size, visible)
        self.color = color
        self.line_width = line_width

        self.progress_length = 1  # Between 1 and self.width

        self.progress_rect = pygame.Rect(self.x, self.y, self.progress_length, self.height)

    def update_progress(self, progress: float) -> None:
        """
        Method updates current progress of bar, and auto updates size of filling bar.
        :param progress: float in range [0, 1] representing progress
        """
        progress = min(1, max(0, progress))  # Put progress in between 0 and 1
        self.progress_length = int(self.width * progress)
        self.update()

    def update(self) -> None:
        """
        Method updates current filling bar.
        """
        self.progress_rect.width = self.progress_length

    def draw(self):
        """
        Method draws self to screen.
        """
        if self.visible:
            # Draw outline of bar
            pygame.draw.rect(
                self.screen,
                self.color,
                self.rect,
                self.line_width
            )
            # Draw progress filled rectangle
            pygame.draw.rect(
                self.screen,
                self.color,
                self.progress_rect,
                0
            )  # Pass 0 width -> fill rectangle


class InsertionPoint(StaticItem):
    """
    Insertion point object automatically blinks based on blink interval, used in InputBar.
    Size of line is set by width, height (size) attribute.
    """
    def __init__(self,
                 position: list[int, int] = [0, 0],
                 size: tuple[int, int] = (1, 1),
                 visible: bool = True,
                 color: tuple[int] = (255, 255, 255),
                 blink_interval: int = 10
                 ):
        """
        :param position: list[int, int] position of bar on screen
        :param size: tuple[int, int] total size of bar
        :param visible: bool if bar visible
        :param color: tuple[int, int, int] color of bar
        :param blink_interval: number of frames between switching on and off
        """
        super().__init__(position, size, visible)
        self.color = color
        self.blink_interval = blink_interval
        self.current_int = 0

    def update(self) -> None:
        """
        Method updates self.
        """
        self.current_int = (self.current_int + 1) % self.blink_interval
        if not self.current_int:
            self.visible = not self.visible

    def draw(self) -> None:
        """
        Method draws self to screen.
        """
        if self.visible and self.selected:
            pygame.draw.line(
                surface=self.screen,
                color=self.color,
                start_pos=self.position,
                end_pos=[self.x, self.y + self.height - 3],
                width=self.width
            )


class InputBar(Item):
    # Dictionary used for converting odd characters from input
    input_converter = {
        "left": "",
        "right": "",
        "up": "",
        "down": "",
        "enter": "\n",
        "space": " ",
        "mouse": ""
        }

    def __init__(self,
                 controller,
                 position: list[int, int] = [0, 0],
                 size: tuple[int, int] = (1, 1),
                 color: tuple[int] = (255, 255, 255),
                 line_width: int = 2
                 ):
        """
        :param controller: Main controller object
        :param position: list[int, int] position of bar on screen
        :param size: tuple[int, int] total size of bar
        :param visible: bool if bar visible
        :param color: tuple[int, int, int] color of bar
        :param line_width: int width of one rectangle lines
        """
        super().__init__(controller, position, size)

        self.color = color
        self.line_width = line_width

        self.characters = " "
        self.text = Text(
            position=[self.x + self.line_width + 3, self.y + 3],
            text=self.characters
        )
        self.last_char_time = pygame.time.get_ticks()
        self.char_debounce_interval = 125

        self.insertion_point = InsertionPoint(
            position=[self.x + self.line_width + 3, self.y + 3],
            size=[2, self.height - self.line_width // 2],
            visible=True,
            blink_interval=150
        )

    def char_time_difference(self) -> None:
        """
        If time difference between last added character and now is less than char_debounce_interval.
        :return: bool if less than interval
        """
        return pygame.time.get_ticks() - self.last_char_time >= self.char_debounce_interval

    def on_click(self) -> None:
        """
        Method sets self as selected and executes on_click function.
        """
        self.selected = True
        super(InputBar, self).on_click()

    def delete_character(self) -> None:
        """
        Method removes last character from field, updates necessary objects.
        """
        self.characters = self.characters[:-1]
        self.text.text = self.characters
        self.text.update()
        self.insertion_point.x = self.text.x + self.text.width

    def add_character(self, char: str) -> None:
        """
        Method adds character to field, updates necessary objects.
        :param char: str character to add to field
        """
        self.characters += char
        self.text.text = self.characters
        self.text.update()
        self.insertion_point.x = self.text.x + self.text.width

    def check_input(self) -> None:
        """
        Method checks input if any keys were pressed.
        :return:
        """
        # Get key pressed
        key_pressed = self.controller.key_pressed
        for key, value in key_pressed.items():
            if value:
                try:
                    char = InputBar.input_converter[key]
                except KeyError:
                    char = key
                if char == "backspace":
                    self.delete_character()
                else:
                    self.add_character(char)
                self.last_char_time = pygame.time.get_ticks()

    def get_text(self) -> str:
        """
        Method returns text currently inside input bar.
        :return: str representing text inside bar
        """
        return self.characters

    def update(self) -> None:
        """
        Method updates bar, fetches pressed keys.
        """
        super(InputBar, self).update()
        if self.mouse_clicked and not self.hovered:
            self.selected = False
        if self.selected and self.char_time_difference():
            self.check_input()
        self.insertion_point.selected = self.selected
        self.insertion_point.update()

    def draw(self) -> None:
        """
        Method draws bar, insertion point and text.
        """
        pygame.draw.rect(self.screen, self.color, self.rect, width=self.line_width)
        if self.selected:
            pygame.draw.rect(self.screen, self.color, self.rect, width=self.line_width + 2)
        self.text.draw()
        self.insertion_point.draw()
