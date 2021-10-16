"""
Abstract class definition for all pages to follow.
"""

from abc import ABC

import pygame


class Page(ABC):
    def __init__(self, controller):
        self.screen = pygame.display.get_surface()
        self.controller = controller
        self.items = []
        self.background_color = (0, 0, 0)

    def add_item(self, item: any):
        self.items.append(item)

    def update(self):
        # Calls update on all items
        pass

    def draw(self):
        for item in self.items:
            item.draw()
