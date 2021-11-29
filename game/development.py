"""
Module containing development class for drawing stats to page.
"""

from typing import Callable

import pygame


class Development:
    """
    Class development used throughout the game, has method for adding functions that draw on screen.
    Used for displaying data from various modules and classes.
    """
    def __init__(self, game):
        """
        :param game: Game main game object containing all other main objects(window, input, controller, ...)
        """
        self.game: "Game" = game

        self.screen = pygame.display.get_surface()
        self.font = pygame.font.SysFont("aria", 21)

        self.visible: bool = False  # If it should be displayed on screen

        self.clock: "Clock" = self.game.clock
        self._fps_list: list[int] = [0 for _ in range(200)]
        self._current_fps_index: int = 0
        self.avg_fps: int = 0

        self.items: list = []
        self.callable_functions = []

        self.add(self.__draw_fps)  # Add the draw fps method to items
        self.add(self.__draw_page_stack)
        self.add(self.__draw_game_dt)

    def __get_fps(self) -> None:
        """
        Method calculates the average fps of 200 consecutive frames.
        """
        fps = self.clock.get_fps()
        if self._current_fps_index >= 200:
            self._current_fps_index = 0
        self._fps_list[self._current_fps_index] = fps
        avg_fps = sum(self._fps_list) / len(self._fps_list)
        self._current_fps_index += 1
        self.avg_fps = round(avg_fps)

    def __draw_fps(self) -> None:
        """
        Method draws fps data on screen.
        """
        fps_str = f"FPS: {self.avg_fps}"
        fps_surface = self.font.render(fps_str, True, (255, 255, 255))
        self.screen.blit(fps_surface, (20, 700))

    def __draw_page_stack(self) -> None:
        """
        Method draws number of pages currently in page_stack of controller.
        """
        num_of_pages = f"Page stack:  {len(self.game.controller.page_stack)}"
        pages_surface = self.font.render(num_of_pages, True, (255, 255, 255))
        self.game.screen.blit(pages_surface, (20, 680))

    def __draw_game_dt(self) -> None:
        """
        Method draws the number of seconds passed from the previous frame on screen.
        """
        dt = f"Last time diff {self.game.dt}"
        dt_surface = self.font.render(dt, True, (255, 255, 255))
        self.game.screen.blit(dt_surface, (20, 660))

    def add(self, func: Callable) -> None:
        """
        Method adds function to items, function then gets executed each loop.
        :param func: Function name -> callable
        """
        self.callable_functions.append(func)

    def add_item(self, item) -> None:
        """
        Method adds item to self.
        :param item: Item to add to self
        """
        self.items.append(item)

    def update(self):
        """
        Method used for updating all data stored in self.
        """
        self.__get_fps()
        for item in self.items:
            item.update()

    def draw(self) -> None:
        """
        Method draws self if set to visible, it also calls all functions added to self.items.
        """
        if self.visible:
            self.update()
            for item in self.items:
                item.draw()
            for func in self.callable_functions:
                func()  # Call each drawing function
