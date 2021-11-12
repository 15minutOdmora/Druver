"""
Module containing different buttons.
"""

from typing import Callable

import pygame

from game.gui.item import Item
from game.gui.text import Text
from game.constants import BaseColors
from game.helpers.file_handling import DirectoryReader, ImageLoader


class Button(Item):
    def __init__(self,
                 controller,
                 position: list[int] = [0, 0],
                 size: tuple[int] = (150, 60),
                 on_click: Callable = lambda: None,
                 text: str = "",
                 fill_color: tuple[int] = BaseColors.button_fill,
                 border_color: tuple[int] = BaseColors.button_outline,
                 movable: bool = False) -> object:
        super().__init__(controller, position, size, on_click, movable)

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


class AnimatedButton(Item):
    def __init__(self,
                 controller,
                 folder_path: str,
                 position: list[int] = [0, 0],
                 on_click: Callable = lambda: None,
                 movable: bool = False,
                 animation_speed=1,
                 ):
        # Initialize image lists and indexes(current displayed images)
        self.normal_images, self.on_click_images, self.on_hover_images = [], [], []
        self.normal_images_index, self.on_click_images_index, self.on_hover_images_index = 0, 0, 0
        self.current_image_list = self.normal_images
        self.current_image_index = 0
        # Get all files into lists
        all_folders = DirectoryReader.get_all_folders(folder_path)
        possible_folders = {
            "normal": self.normal_images,
            "on_click": self.on_click_images,
            "on_hover": self.on_hover_images
        }
        for name, path in all_folders:
            if name in possible_folders.keys():
                possible_folders[name] += ImageLoader.load_transparent_folder(path)

        size = self.normal_images[0].get_size()
        self.was_clicked = False
        self.animation_speed = animation_speed

        super().__init__(controller, position, size, on_click, movable=movable)

    def update(self):
        """ Overwrite items update method. """
        self.hovered = self.rect.collidepoint(self.controller.mouse_position)
        if self.hovered:
            if not (self.on_hover_images_index >= len(self.on_hover_images) - 1):
                self.on_hover_images_index += self.animation_speed
            if self.controller.mouse_clicked or self.was_clicked:
                self.was_clicked = True
                if not (self.on_click_images_index >= len(self.on_click_images) - 1):
                    self.on_click_images_index += self.animation_speed
                    self.current_image_list = self.on_click_images
                    self.current_image_index = self.on_click_images_index
                else:
                    self.on_click()
                    self.was_clicked = False
            else:
                self.current_image_list = self.on_hover_images
                self.current_image_index = self.on_hover_images_index
                self.on_click_images_index = 0
        else:
            self.on_hover_images_index = 0
            self.current_image_list = self.normal_images
            self.current_image_index = self.normal_images_index
        for item in self.items:
            item.update()

    def draw(self):
        """ Overwrite items draw method. """
        self.screen.blit(self.current_image_list[round(self.current_image_index)], self.position)
        for item in self.items:
            item.draw()
