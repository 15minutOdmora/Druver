"""
Module containing menu classes. TODO in task.
"""

import pygame

from game.gui.item import StaticItem
from game.gui.image import StaticImage


class PauseMenu(StaticItem):
    def __init__(self,
                 position: list[int, int],
                 size: list[int],
                 background_color: tuple[int] = (100, 100, 100),
                 background_alpha: int = 100):
        """
        :param controller:
        :param position:
        :param size:
        :param background_image:
        """
        super().__init__(position, size)

        # Create background surface
        self.background_surface = pygame.Surface(self.size)
        self.background_surface.set_alpha(background_alpha)
        self.background_surface.fill(background_color)

    def draw(self):
        # Draw background then every other item
        if self.visible:
            self.screen.blit(self.background_surface, self.position)
        super(PauseMenu, self).draw()
