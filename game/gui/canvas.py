"""
Module for canvas item, where different items defined in this module (line, rectangle, ...) can be drawn on canvas.
"""

import pygame

from game.gui.item import Item


class Line:
    """
    Class representing one drawable line used by canvas.
    """
    def __init__(self,
                 screen,
                 position: list[int],
                 end_point: list[int],
                 color: tuple[int, int, int] = (255, 255, 255),
                 width: int = 2):
        """
        :param screen: pygame.Surface to draw on
        :param position: list[int] position of line
        :param end_point: list[int] end position of line
        :param color: tuple[int, int, int] color of line
        :param width: int width of line
        """
        self.screen = screen
        self.position = position
        self.end_point = end_point
        self.color = color
        self.width = width

    def draw(self) -> None:
        pygame.draw.line(self.screen, self.color, self.position, self.end_point, width=self.width)


class Rectangle:
    """
    Class representing one drawable rectangle used by canvas.
    """
    def __init__(self,
                 screen,
                 position: list[int],
                 end_point: list[int],
                 color: tuple[int, int, int] = (255, 255, 255),
                 width: int = 2):
        """
        :param screen: pygame.Surface to draw on
        :param position: list[int] position of rectangle
        :param end_point: list[int] end position of rectangle
        :param color: tuple[int, int, int] color of rectangle
        :param width: int width of rectangle lines
        """
        self.screen = screen
        self.position = position
        self._end_point = end_point
        self.color = color
        self.width = width

        self.rect = pygame.Rect(
            [self.position[0], self.position[1]],
            [self.end_point[0] - self.position[0], self.end_point[1] - self.position[1]]
        )

    @property
    def end_point(self) -> list[int]:
        return self._end_point

    @end_point.setter
    def end_point(self, value: list[int]) -> None:
        self._end_point = value
        self.rect = pygame.Rect(
            [self.position[0], self.position[1]],
            [value[0] - self.position[0], value[1] - self.position[1]]
        )

    def draw(self) -> None:
        """
        Method draws rect on screen.
        """
        pygame.draw.rect(self.screen, self.color, self.rect, self.width)


class Canvas(Item):
    """
    Canvas used for drawing different shapes on screen. Canvas needs to be selected first (by mouse click on it) for it
    to draw shape. Shapes can be selected same as color through methods (best passed as on_click functions).
    """
    def __init__(self,
                 controller,
                 position: list[int] = [0, 0],
                 size: tuple[int, int] = (1, 1)
                 ):
        """
        :param controller: Controller main controller object used throughout game
        :param position: list[int] position of canvas on screen
        :param size: tuple[int, int] size of canvas
        """
        super().__init__(controller, position, size)
        self.debounce_interval = 300

        self.clicks = [0, 0]
        self.currently_drawing = False
        self.drawable = None

        self.current_color = (255, 255, 255)
        self.current_width = 2
        self.currently_drawing = Line

        self.available_shapes = {
            "line": Line,
            "rectangle": Rectangle
        }

    def __do_draw(self) -> None:
        """
        Private Method used for detecting drawing and drawing set sahapes on screen.
        """
        mouse_pos = self.controller.mouse_position
        if self.drawing:
            if self.clicks[0] == 0:
                self.drawable = self.currently_drawing(
                    self.screen,
                    mouse_pos,
                    mouse_pos,
                    color=self.current_color,
                    width=self.current_width
                )
                self.clicks[0] = 1
            else:
                self.drawable.end_point = mouse_pos
                self.items.append(self.drawable)
                self.drawing = False
                self.drawable = None
                self.clicks = [0, 0]

    def undo(self) -> None:
        """
        Method deletes last drawn shape on canvas.
        """
        if len(self.items) > 0:
            self.items.pop()

    def clear(self) -> None:
        """
        Method clears everything on canvas.
        """
        self.items = []

    def set_color(self, color: tuple[int, int, int]) -> None:
        """
        Method sets current color of shapes to be drawn.
        :param color: tuple[int, int, int] color to set
        """
        self.current_color = color

    def get_available_shapes(self) -> list[str]:
        """
        Method returns list of available shapes to draw on canvas.
        :return: list[str] list of strings where each string represents possible shape to draw
        """
        return list(self.available_shapes.keys())

    def change_currently_drawing(self, change_to: str) -> None:
        """
        Method changes currently drawing shape. Raises error if said shape is not implemented.
        :param change_to: str representing shape to select
        """
        if change_to in self.available_shapes.keys():
            self.currently_drawing = self.available_shapes[change_to]

    def update(self) -> None:
        """
        Method updates current canvas, sets if selected, sets drawing.
        """
        self.hovered = self.rect.collidepoint(self.controller.mouse_position)
        # Check if mouse was clicked on item, in the interval of the debounce time
        if self.hovered and self.mouse_clicked() and self.debounce_time():
            self.last_click_time = pygame.time.get_ticks()  # This has to be updated manually
            if self.selected:
                self.drawing = True
                self.__do_draw()
            self.selected = True
        # If was pressed and mouse is not on the item anymore still call on_click method works if movable = True
        if self.mouse_clicked() and not self.hovered:  # Only check if item is movable, otherwise get multiple clicks
            self.selected = False
            self.drawing = False

    def draw(self) -> None:
        """
        Method draws canvas (thicker if selected) and all items currently on it.
        :return:
        """
        if self.selected:
            pygame.draw.rect(self.screen, (255, 255, 255), self.rect, width=4)
            if self.drawable:
                self.drawable.end_point = self.controller.mouse_position
                self.drawable.draw()
        else:
            pygame.draw.rect(self.screen, (255, 255, 255), self.rect, width=2)
        for item in self.items:
            item.draw()
