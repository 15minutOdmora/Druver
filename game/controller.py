"""
Module containing the controller class.

Controller class object acts as an intermediate between game wide objects, used for page redirection, game pausing, ...
"""

from typing import Callable
import sys
import inspect

from game.pages import *  # This imports every page from the packages __init__ file
from game.helpers.stack import Stack, UniqueStack
from game.helpers import helpers

from game.play.time_trial import TimeTrial


class Controller:
    """
    Main object throughout the game. Mediator between game object and everything else.
    Contains page_stack attribute which is a Stack, containing visited pages.
    """
    def __init__(self, game):
        """
        :param game: Game object
        """
        self.game = game

        # Save as two consecutive mouse positions / clicks, accessible through properties
        self.mouse_position: list[tuple[int, int]] = (0, 0)
        self._mouse_pressed: bool = [False, False]
        self.mouse_clicked = False
        self.mouse_movement = (0, 0)
        self.mouse_scroll = 0  # Wheel on the mouse, 1 if up -1 if down roll
        self.esc_clicked: bool = False
        self.key_pressed: dict = {}

        self.pages = {
            "WelcomePage": WelcomePage,
            "StartGamePage": StartGamePage,
            "TimeTrial": TimeTrial,
            "SelectionPage": SelectionPage,
            "CarBoundariesPage": CarBoundariesPage,
            "GenerateCarBoundariesPage": GenerateCarBoundariesPage
        }
        self.page_stack = Stack()

        self.current_page = WelcomePage

    @property
    def mouse_pressed(self) -> bool:
        """
        Property returns if mouse was clicked on current game frame.
        :return: If clicked or not
        """
        return self._mouse_pressed[-1]  # Last click

    @mouse_pressed.setter
    def mouse_pressed(self, clicked: bool) -> None:
        """
        Property setter sets the last click on mouse.
        :param clicked: If clicked or not
        """
        self._mouse_pressed.append(clicked)
        self._mouse_pressed = self._mouse_pressed[-2:]  # Save as only the last 2 recent clicks

    @property
    def previous_mouse_pressed(self) -> bool:
        """
        Returns if mouse was clicked on the previous frame.
        :return: If clicked or not
        """
        return self._mouse_pressed[0]  # Left one is previous one as we add clicks on the end

    @property
    def dt(self):
        """
        Property for time difference between two last frames.
        :return: float
        """
        return self.game.dt

    @property
    def paused(self):
        """
        Property for if game is currently paused.
        :return: bool
        """
        return self.game.paused

    @property
    def current_page(self):
        """
        Property returns the top page on page_stack.
        :return: Page or ScrollablePage
        """
        return self.page_stack.peak()

    @current_page.setter
    def current_page(self, page):
        """
        Property setter for the current page
        :param page: Page
        """
        self.page_stack.push(page(self))  # Initialize page

    @property
    def development(self):
        """
        Property for the game development object
        :return: Development
        """
        return self.game.development

    def redirect_to_page(self, to_page: str, *args, **kwargs) -> None:
        """
        Method redirects to page defined as a string. Args and Kwargs can be passed to page class initialization.
        Error gets displayed if page does not exist.
        :param to_page: String name of page to redirect to
        """
        if to_page in self.pages.keys():
            self.page_stack.push(self.pages[to_page](self, *args, **kwargs))  # Initialize page and push on stack
        else:
            print(f"Controller: Redirection error to page {to_page}. Page does not exist.")

    def go_back(self) -> None:
        """
        Method goes back one page in the page stack.
        If page stack is empty => error gets raised.
        """
        if not self.page_stack.empty():
            self.page_stack.pop()
        else:
            print(f"Controller: Redirection error calling go_back.\n   Page stack is empty.")

    def pause_game(self) -> None:
        """
        Method for pausing and un-pausing game.
        """
        self.game.paused = not self.game.paused
