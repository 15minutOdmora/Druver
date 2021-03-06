"""
Main entry point for the program, runs main loop and has the main game class definition.
"""

import pygame

from game import constants
from game.controller import Controller
from game.window import Window
from game.input import Input
from game.development import Development


class Game:
    """
    Main class for game, holds every game wide property and settings.
    """
    def __init__(self):
        # Pygame initial configuration
        pygame.init()
        self.screen = pygame.display.set_mode(constants.SCREEN_SIZE)
        pygame.display.set_caption(constants.NAME)
        # pygame.display.set_icon()  TODO: Add icon

        self.FPS = constants.FPS_CAP
        self.clock = pygame.time.Clock()
        self._dt = 0  # Change of time between seconds
        self.paused = False  # If game is paused

        self.development = Development(self)
        self.controller = Controller(self)
        self.window = Window(self)
        self.input = Input(self)

    @property
    def dt(self) -> float:
        """
        Difference in time between current frame and previous frame.
        """
        return self._dt * 0.001

    def run(self) -> None:
        """
        Main game loop.
        """
        running = True
        while running:
            self.window.update()
            running = self.input.update()
            self._dt = self.clock.tick()


if __name__ == "__main__":
    game = Game()
    game.run()
