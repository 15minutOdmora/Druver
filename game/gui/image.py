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
        if isinstance(image_path, pygame.Surface):
            self.image = image_path
        else:
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


class RotatingImages(ResizableItem):
    """
    RotatingImages holds a folder of images, when item gets selected we scroll through images otherwise the image on the
    starting index is displayed and re-sized.
    Inherits from ResizableItem as it can be resized.
    """
    def __init__(self,
                 folder_path: str,
                 position: list[int, int] = [0, 0],
                 rotation_speed: float = 0.1,
                 starting_index: int = 30
                 ):
        """
        :param folder_path: str path to folder containing images
        :param position: list[int, int] position of item on screen
        :param rotation_speed: float speed of rotation, value increments current index of image every frame
        :param starting_index: int index of initial image displayed and , in folder for
        """
        self.images = ImageLoader.load_transparent_folder(folder_path)
        self.resizable_image = ResizableImage(self.images[starting_index])

        self.max_index = len(self.images) - 1
        self.starting_index = starting_index
        self.current_index = starting_index
        self.rotation_speed = rotation_speed

        size = self.resizable_image.size
        super().__init__(position, size)  # Initialize parent class with fetched size

    def resize(self, factor: float) -> None:
        """
        Method will re-size image and its position based on a factor passed as argument.
        :param factor: float factor to scale item in range [0, inf]
        """
        super(RotatingImages, self).resize(factor)
        self.resizable_image.resize(factor)

    def reset_size(self) -> None:
        """
        Method will reset its size to the initially set one.
        """
        super(RotatingImages, self).reset_size()
        self.resizable_image.reset_size()

    def draw(self) -> None:
        """
        Method will draw itself and every item attached to it.
        """
        self.resizable_image.position = self.position
        if self.selected:
            self.current_index += self.rotation_speed
            if self.current_index >= self.max_index:
                self.current_index = 0
            self.screen.blit(self.images[int(self.current_index)], self.position)
        else:
            self.current_index = self.starting_index
            self.resizable_image.draw()
        for item in self.items:
            item.draw()


class FolderImages(StaticItem):
    """
    Folder images holds a folder of images where only one is displayed, images can be iterated through.
    You can move to the next one, previous one, ...
    """
    def __init__(self,
                 folder_path: str,
                 position: tuple[int, int] = (0, 0)
                 ):
        """
        :param folder_path: str path to folder containing images, relative or absolute
        :param position: list[int, int] position of image on screen
        """
        self.images = ImageLoader.load_transparent_folder(folder_path)
        self.current_index = 0
        size = tuple(self.current_image.get_rect()[2:])
        super().__init__(position, size)

    @property
    def number_of_images(self) -> int:
        return len(self.images)

    @property
    def current_image(self):
        return self.images[self.current_index]

    def next_image(self) -> None:
        """
        Method moves to next image in folder. If we are at the end of the folder it goes back to first image.
        """
        if self.current_index + 1 <= self.number_of_images - 1:
            self.current_index += 1
        else:
            self.current_index = 0

    def previous_image(self):
        """
        Method moves back one image in folder. If we are at start of folder it goes at the end.
        """
        if self.current_index - 1 > 0:
            self.current_index -= 1
        else:
            self.current_index = self.number_of_images - 1

    def reset(self):
        """
        Method resets currently displayed image to the first one in the folder.
        """
        self.current_index = 0

    def draw(self) -> None:
        """
        Used for drawing itself and every item attached to it.
        """
        self.screen.blit(self.current_image, self.position)
        for item in self.items:
            item.draw()
