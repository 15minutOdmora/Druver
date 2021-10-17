"""
Module for class containing, loading and drawing images.
"""

import pygame

from game.gui.item import StaticItem
from game.helpers.file_handling import ImageLoader


class StaticImage(StaticItem):
    """
    Class for handling a single static image.
    """

    def __init__(self, image_path: str, position: tuple[int] = (0, 0)):
        """
        Args:
            image_path (str):  to image file to load from
            position (tuple[int]): Position of the top left corner of image. Defaults to (0, 0)
        """
        self.image = ImageLoader.load_image(image_path)
        size = tuple(self.image.get_rect()[2:])
        super().__init__(position, size)

    def draw(self):
        """ Used for drawing itseld and every item attached to it. """
        self.screen.blit(self.image, self.position)
        for item in self.items:
            item.draw()
