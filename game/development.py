"""
Module containing development class for drawing stats to page.
"""

import pygame


class Development:
    def __init__(self, game):
        self.game: "Game" = game

        self.screen = pygame.display.get_surface()
        self.font = pygame.font.SysFont("aria", 21)

        self.visible: bool = False  # If it should be displayed on screen

        self.clock: "Clock" = self.game.clock
        self._fps_list: list[int] = [0 for _ in range(200)]
        self._current_fps_index: int = 0
        self.avg_fps: int = 0

        self.items: list["function"] = []

        self.add(self.__draw_fps)  # Add the draw fps method to items
        self.add(self.__draw_page_stack)

    def __get_fps(self):
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

    def __draw_fps(self):
        fps_str = f"FPS: {self.avg_fps}"
        fps_surface = self.font.render(fps_str, True, (255, 255, 255))
        self.screen.blit(fps_surface, (20, 700))

    def __draw_page_stack(self):
        num_of_pages = f"Page stack:  {len(self.game.controller.page_stack)}"
        pages_surface = self.font.render(num_of_pages, True, (255, 255, 255))
        self.game.screen.blit(pages_surface, (20, 680))

    def add(self, func: "function") -> None:
        """
        Method adds function to items, function then gets executed each loop.
        :param func: Function name -> callable
        """
        self.items.append(func)

    def update(self):
        self.__get_fps()

    def draw(self):
        if self.visible:
            self.update()
            for item in self.items:
                item()  # Call each drawing function