"""
Module for classes containing, loading and drawing image items.
"""

import pygame

from game.gui.item import ResizableItem, StaticItem
from game.helpers.file_handling import ImageLoader


class StaticImage(StaticItem):
    """
    Class for handling a single static image. This image can not be moved, refer to ResizableImage for moving images.
    inherits from static item.
    """
    def __init__(self,
                 image_path: str,
                 position: tuple[int, int] = (0, 0)
                 ):
        """
        :param image_path: str path to image, relative or absolute
        :param position: list[int, int] position of image on screen
        """
        self.image = ImageLoader.load_image(image_path)
        size = tuple(self.image.get_rect()[2:])
        super().__init__(position, size)

    def draw(self) -> None:
        """
        Used for drawing itself and every item attached to it.
        """
        self.screen.blit(self.image, self.position)
        for item in self.items:
            item.draw()


class ResizableImage(ResizableItem):
    """
    Class for handling a single static image that can be re-sized. Inherits from ResizableItem.
    Has all the properties of items + extended properties from ResizableImage.
    """
    def __init__(self,
                 image_path: str,
                 position: list[int, int] = [0, 0]
                 ):
        """
        :param image_path: str path to image, relative or absolute
        :param position: list[int, int] position of image on screen
        """
        self.image = ImageLoader.load_image(image_path)  # Original Image
        self.current_image = self.image  # Currently used image
        size = tuple(self.image.get_rect()[2:])
        super().__init__(position, size)  # Initialize parent class with fetched size

    def resize(self, factor: float) -> None:
        """
        Method will re-size image and its position based on a factor passed as argument.
        :param factor: float factor to scale item in range [0, inf]
        """
        super(ResizableImage, self).resize(factor)
        self.resized = pygame.transform.scale(self.image, self.resized_size)
        self.current_image = self.resized

    def reset_size(self) -> None:
        """
        Method will reset its size to the initially set one.
        """
        super(ResizableImage, self).reset_size()
        self.current_image = self.image

    def draw(self) -> None:
        """
        Method will draw itself and every item attached to it.
        """
        self.screen.blit(self.current_image, self.position)
        for item in self.items:
            item.draw()
