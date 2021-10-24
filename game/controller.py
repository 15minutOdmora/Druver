"""
Module containing the controller class.

Controller class object acts as an intermediate between game wide objects, ex. page redirection, ...
"""

from typing import Callable
import sys
import inspect

from game.pages import *  # This imports every page from the packages __init__ file
from game.helpers.stack import Stack


class Controller:
    def __init__(self, game):
        self.game = game

        self.mouse_position: tuple[int, int] = (0, 0)
        self._mouse_clicked: bool = False
        self.key_pressed: dict = {}

        self.pages = {
            "WelcomePage": WelcomePage
        }
        self.page_stack = Stack()

        self.current_page = WelcomePage(self)

    @property
    def current_page(self):
        return self.page_stack.peak()

    @current_page.setter
    def current_page(self, page):
        self.page_stack.push(page)
