"""
Module containing different buttons.
"""

from typing import Callable

import pygame

from game.gui.item import Item
from game.gui.text import Text
from game.constants import BaseColors


class Button(Item):
    def __init__(self,
                 controller,
                 position: list[int] = [0, 0],
                 size=(150, 60),
                 on_click: Callable = lambda: None,
                 text: str = "",
                 fill_color: tuple = BaseColors.button_fill,
                 border_color: tuple = BaseColors.button_outline):
        super().__init__(controller, position, size, on_click)

        self.screen = pygame.display.get_surface()
        self.controller = controller

        if type(text) is str:
            self.text = Text(
                text=text,
                size=22,
            )
        else:
            self.text = text

        self._fill_color = fill_color  # These ones define the colors
        self._border_color = border_color
        self.fill_color = self._fill_color  # These ones get used
        self.border_color = self._border_color

        self.text.position = self.get_text_position()

        self.items = []

        self.items.append(
            self.text
        )

    def get_text_position(self) -> tuple[int]:
        # Center text in button
        x_pos = int((self.x + (self.width * 0.5)) - (self.text.width * 0.5))
        y_pos = int((self.y + (self.height * 0.5)) - (self.text.height * 0.5))
        return x_pos, y_pos

    def update(self):
        # Call parent method
        super(self.__class__, self).update()
        # And then re center text
        self.text.position = self.get_text_position()

    def draw(self):
        # Switch colors if hovered
        if self.hovered:
            self.border_color = self._border_color
            self.fill_color = self._fill_color
        else:
            self.border_color = self._fill_color
            self.fill_color = self._border_color

        pygame.draw.rect(
            self.screen,
            self.border_color,
            self.rect,
            width=0
        )
        pygame.draw.rect(
            self.screen,
            self.fill_color,
            self.rect,
            width=3
        )
        self.text.color = self.fill_color
        self.text.update()

        for item in self.items:
            item.draw()
