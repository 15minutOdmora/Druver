"""
Module for text classes.
"""

import pygame


class Text:
    def __init__(self, text, font="aria", size=21, position=(0, 0), color=(255, 255, 255)):
        """
        :param text:
        :param font:
        :param size:
        :param position:
        :param color:
        """
        self.screen = pygame.display.get_surface()
        self.items = []
        self.color = color
        self.text = text

        pygame.font.init()
        self.font = pygame.font.SysFont(font, size)
        self.position = position
        self.surface = self.font.render(text, True, self.color)
        self.size = self.font.size(text)
        self.width, self.height = self.size

    def update(self):
        self.surface = self.font.render(self.text, True, self.color)
        self.size = self.font.size(self.text)
        self.width, self.height = self.size

    def draw(self):
        self.screen.blit(self.surface, self.position)
