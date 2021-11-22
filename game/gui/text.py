"""
Module for text classes.
"""

import pygame

from game.constants import Paths, BaseColors
from game.gui.item import ResizableItem, StaticItem


class Text(StaticItem):
    """
    Class for holding text objects as items. Normal Text can not be re-sized, but can be movable.
    Inherits from StaticItem.
    """
    def __init__(self,
                 position: list[int, int] = [0, 0],
                 text: str = "Text",
                 font: str = Paths.LO_RES_NARROW,
                 size: int = 21,
                 color: tuple[int, int, int] = (255, 255, 255)
                 ):
        """
        :param position: list[int, int] position of text on screen
        :param text: str displayed text
        :param font: str font name or path to font file(ttf)
        :param size: int size of font
        :param color: tuple[int, int, int] RGB value of color of text
        """
        self.screen = pygame.display.get_surface()
        pygame.font.init()
        self.color = color
        self.text = text
        if "\\" in font:  # If passed font string has / it is a path to font file, load appropriately
            self.font = pygame.font.Font(font, size)
        else:
            self.font = pygame.font.SysFont(font, size)
        self.surface = self.font.render(text, True, self.color)
        size = self.font.size(text)
        # Call to super method with fetched size of surface
        super().__init__(position, size)

    def update(self) -> None:
        """
        Method will update self surface and position.
        """
        # Override parents method
        self.surface = self.font.render(self.text, True, self.color)
        self.size = self.font.size(self.text)

    def draw(self) -> None:
        """
        Method will draw text on screen.
        """
        self.screen.blit(self.surface, self.position)


class CustomText(ResizableItem):
    """
    CustomText inherits from ResizableItem and is there for re-sizable. Works the same as every other re-sizable item.
    It uses custom fonts provided as ttf files. No system-wide fonts can be used.
    """
    def __init__(self,
                 text: str,
                 font: str = Paths.LO_RES_NARROW,
                 size: int = 21,
                 position: list[int, int] = [0, 0],
                 color: tuple[int, int, int] = BaseColors.main_text
                 ):
        """
        :param text: str representing text to display
        :param font: str path to used font
        :param size: int representing size of font
        :param position: list[int, int] position of item on screen (upper left corner)
        :param color: tuple[int, int, int] representing RGB values of color
        """
        self.screen = pygame.display.get_surface()
        pygame.font.init()
        self.color = color
        self.text = text
        self.font = pygame.font.Font(font, size)
        self.surface = self.font.render(text, True, self.color)
        self.current_surface = self.surface
        size = self.font.size(text)

        super().__init__(position, size)

    def resize(self, factor: float) -> None:
        """
        Method will re-size image and its position based on a factor passed as argument.
        :param factor: float factor to scale item in range [0, inf]
        """
        super(CustomText, self).resize(factor)
        self.resized = pygame.transform.scale(self.surface, self.resized_size)
        self.current_surface = self.resized

    def reset_size(self) -> None:
        """
        Method will reset its size to the initially set one.
        """
        super(CustomText, self).reset_size()
        self.current_surface = self.surface

    def update(self) -> None:
        """
        Method will update self surface and position.
        """
        self.surface = self.font.render(self.text, True, self.color)
        self.size = self.font.size(self.text)

    def draw(self) -> None:
        """
        Method will draw text on screen.
        """
        self.screen.blit(self.current_surface, self.position)
