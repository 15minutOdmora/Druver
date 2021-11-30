"""
Page made for testing gui items and other functionality.
"""

import pygame

from game.pages.page import Page
from game.gui.bar import InputBar


class TestingPage(Page):
    def __init__(self, controller):
        super().__init__(controller)

        self.input_bar = InputBar(
            self.controller,
            position=[300, 300],
            size=(200, 30)
        )
        self.add_item(self.input_bar)
