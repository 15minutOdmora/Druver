"""
Module for Bar classes.
"""

import pygame

from game.gui.item import StaticItem


class LoadingBar(StaticItem):
    """
    LoadingBar item is a rectangle which displays progress on screen by filling up.
    Has update_progress method where you can pass current progress as a float in the interval [0, 1],
    this method automatically updates self object.
    """
    def __init__(self,
                 position: list[int, int] = [0, 0],
                 size: tuple[int, int] = (1, 1),
                 visible: bool = True,
                 color: tuple[int] = (255, 255, 255),
                 line_width: int = 3
                 ):
        """
        :param position: list[int, int] position of bar on screen
        :param size: tuple[int, int] total size of bar
        :param visible: bool if bar visible
        :param color: tuple[int, int, int] color of bar
        :param line_width: int width of one rectangle lines
        """
        super().__init__(position, size, visible)
        self.color = color
        self.line_width = line_width

        self.progress_length = 1  # Between 1 and self.width

        self.progress_rect = pygame.Rect(self.x, self.y, self.progress_length, self.height)

    def update_progress(self, progress: float) -> None:
        """
        Method updates current progress of bar, and auto updates size of filling bar.
        :param progress: float in range [0, 1] representing progress
        """
        progress = min(1, max(0, progress))  # Put progress in between 0 and 1
        self.progress_length = int(self.width * progress)
        self.update()

    def update(self) -> None:
        """
        Method updates current filling bar.
        """
        self.progress_rect.width = self.progress_length

    def draw(self):
        """
        Method draws self to screen.
        """
        if self.visible:
            # Draw outline of bar
            pygame.draw.rect(
                self.screen,
                self.color,
                self.rect,
                self.line_width
            )
            # Draw progress filled rectangle
            pygame.draw.rect(
                self.screen,
                self.color,
                self.progress_rect,
                0
            )  # Pass 0 width -> fill rectangle
