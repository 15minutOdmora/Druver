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
    """
    Button class for drawing simple buttons on screen, each button is just a rectangle with text inside.
    """
    def __init__(self,
                 controller,
                 position: list[int] = [0, 0],
                 size: tuple[int] = (150, 60),
                 on_click: Callable = lambda: None,
                 text: str = "",
                 fill_color: tuple[int] = BaseColors.button_fill,
                 border_color: tuple[int] = BaseColors.button_outline,
                 movable: bool = False) -> object:
        """
        :param controller: Controller object
        :param position: list[int, int] position of button on screen
        :param size: tuple[int, int] size of button
        :param on_click: Callable function that is called when a click on the button is performed
        :param text: Text or str displayed and centered inside button
        :param fill_color: tuple[int, int, int] RGB of color to fill the button with
        :param border_color: tuple[int, int, int] RGB of color to outline the button with
        :param movable: bool if button can be moved
        """
        super().__init__(controller, position, size, on_click, movable)
        self.screen = pygame.display.get_surface()
        self.controller = controller
        # Check if passed argument is string => create Text object
        if type(text) is str:
            self.text = Text(
                text=text,
                size=22,
            )
        else:
            self.text = text
        # Set colors
        self._fill_color = fill_color  # These ones define the colors
        self._border_color = border_color
        self.fill_color = self._fill_color  # These ones get used
        self.border_color = self._border_color
        # Set position of text and add object to items
        self.text.position = self.get_text_position()
        self.items.append(
            self.text
        )

    def get_text_position(self) -> list[int, int]:
        """
        Method calculates the position of text inside button to that it is centered.
        :return: list[int, int] position of centered text
        """
        # Center text in button
        x_pos = int((self.x + (self.width * 0.5)) - (self.text.width * 0.5))
        y_pos = int((self.y + (self.height * 0.5)) - (self.text.height * 0.5))
        return [x_pos, y_pos]

    def update(self) -> None:
        """
        Method updates self and re-sets text position.
        """
        # Call parent method
        super(self.__class__, self).update()
        # And then re center text
        self.text.position = self.get_text_position()

    def draw(self) -> None:
        """
        Method draws button along with its text on screen.
        """
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
    """

    """
    def __init__(self,
                 controller,
                 folder_path: str,
                 position: list[int, int] = [0, 0],
                 on_click: Callable = lambda: None,
                 movable: bool = False,
                 animation_speed: float = 1,
                 ):
        """
        :param controller: Controller object
        :param folder_path: str path to folder of button images with sub-directories: on_hover, on_click, normal
        :param position: list[int, int] position of button on screen
        :param on_click: Callable function executed once the button receives a click
        :param movable: bool if button can be moved
        :param animation_speed: float or int representing animation speed (image iteration for every frame)
        """
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
        """
        Overwrite items update method from super.
        Display correct images and update all items.
        """
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
        """
        Overwrite super draw method.
        Draws currently displayed image on screen.
        """
        self.screen.blit(self.current_image_list[round(self.current_image_index)], self.position)
        for item in self.items:
            item.draw()
