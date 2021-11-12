"""
Module for text classes.
"""

import pygame

from game.constants import Paths, BaseColors
from game.gui.item import ResizableItem, StaticItem


class Text(StaticItem):
    def __init__(self, position=(0, 0), text="", font="aria", size=21, color=(255, 255, 255)):
        self.screen = pygame.display.get_surface()
        pygame.font.init()
        self.color = color
        self.text = text
        self.font = pygame.font.SysFont(font, size)
        self.surface = self.font.render(text, True, self.color)
        size = self.font.size(text)

        super().__init__(position, size)

    def update(self):
        # Override parents method
        self.surface = self.font.render(self.text, True, self.color)
        self.size = self.font.size(self.text)

    def draw(self):
        self.screen.blit(self.surface, self.position)


class CustomText(ResizableItem):
    def __init__(self, text, font=Paths.LO_RES_NARROW, size=21, position=(0, 0), color=BaseColors.main_text):
        self.screen = pygame.display.get_surface()
        pygame.font.init()
        self.color = color
        self.text = text
        self.font = pygame.font.Font(font, size)
        self.surface = self.font.render(text, True, self.color)
        self.current_surface = self.surface
        size = self.font.size(text)

        super().__init__(position, size)

    def resize(self, factor: float):
        super(CustomText, self).resize(factor)
        self.resized = pygame.transform.scale(self.surface, self.resized_size)
        self.current_surface = self.resized

    def reset_size(self):
        super(CustomText, self).reset_size()
        self.current_surface = self.surface

    def update(self):
        self.surface = self.font.render(self.text, True, self.color)
        self.size = self.font.size(self.text)

    def draw(self):
        self.screen.blit(self.current_surface, self.position)
