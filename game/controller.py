"""
Module containing the controller class.

Controller class object acts as an intermediate between game wide objects, ex. page redirection, ...
"""

from typing import Callable
import sys
import inspect

from game.pages import *  # This imports every page from the packages __init__ file
from game.helpers.stack import Stack
from game.helpers import helpers

from game.play.time_trial import TimeTrial


class Controller:
    def __init__(self, game):
        self.game = game

        self.mouse_position: tuple[int, int] = (0, 0)
        self.mouse_clicked: bool = False
        self.esc_clicked: bool = False
        self.key_pressed: dict = {}

        self.pages = {
            "WelcomePage": WelcomePage,
            "StartGamePage": StartGamePage,
            "TimeTrial": TimeTrial
        }
        self.page_stack = Stack()

        self.current_page = WelcomePage

    @property
    def dt(self):
        return self.game.dt

    @property
    def paused(self):
        return self.game.paused

    @property
    def current_page(self):
        return self.page_stack.peak()

    @property
    def development(self):
        return self.game.development

    @current_page.setter
    def current_page(self, page):
        self.page_stack.push(page(self))  # Initialize page

    def redirect_to_page(self, to_page: str) -> None:
        """
        Method redirects to page defined as a string.
        Error gets displayed if page does not exist.
        :param to_page: String name of page to redirect to
        """
        if to_page in self.pages.keys():
            self.current_page = self.pages[to_page]  # Page gets initialized through setter
        else:
            print(f"Controller: Redirection error to page {to_page}.\n   Page does not exist.")

    def go_back(self) -> None:
        """
        Method goes back one page in the page stack.
        I f page stack is empty => error gets displayed.
        """
        if not self.page_stack.empty():
            self.page_stack.pop()
        else:
            print(f"Controller: Redirection error calling go_back.\n   Page stack is empty.")

    def pause_game(self) -> None:
        """
        Method pauses or un-pauses game once called base on the current state.
        """
        self.game.paused = not self.game.paused
