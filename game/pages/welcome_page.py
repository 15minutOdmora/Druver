"""
Welcome page loads when the game is ran.
"""

import pygame

from game.gui.text import Text


class WelcomePage:
    def __init__(self, controller):
        self.screen = pygame.display.get_surface()
        self.controller = controller
        self.items = []
        self.background_color = (0, 0, 0)
        title = Text(
            text="Welcome Page",
            position=(200, 200)
        )
        self.add_item(title)

    def add_item(self, item: any):
        self.items.append(item)

    def update(self):
        # Calls update on all items
        pass

    def draw(self):
        for item in self.items:
            item.draw()
