"""
Page for generating car boundaries and tyre positions on shifted perspective view.
"""

from game.helpers.helpers import create_callable
from game.pages.page import Page
from game.gui.canvas import Canvas
from game.gui.button import Button


class CarBoundariesPage(Page):
    """
    TODO
    """
    def __init__(self, controller):
        super().__init__(controller)

        self.canvas = Canvas(
            controller,
            position=[200, 100],
            size=[880, 420]
        )
        self.canvas.visible = True
        self.add_item(self.canvas)

        self.undo_button = Button(
            controller=self.controller,
            position=[870, 530],
            size=[100, 35],
            text="Undo",
            on_click=create_callable(self.canvas.undo)
        )
        self.add_item(self.undo_button)

        self.clear_button = Button(
            controller=self.controller,
            position=[980, 530],
            size=[100, 35],
            text="Clear",
            on_click=create_callable(self.canvas.clear)
        )
        self.add_item(self.clear_button)

        self.set_blue_color_button = Button(
            controller=self.controller,
            position=[200, 530],
            size=[100, 35],
            text="Blue",
            on_click=create_callable(self.canvas.set_color, (0, 0, 255))
        )
        self.add_item(self.set_blue_color_button)

        self.set_white_color_button = Button(
            controller=self.controller,
            position=[310, 530],
            size=[100, 35],
            text="White",
            on_click=create_callable(self.canvas.set_color, (255, 255, 255))
        )
        self.add_item(self.set_white_color_button)

        self.set_red_color_button = Button(
            controller=self.controller,
            position=[420, 530],
            size=[100, 35],
            text="Red",
            on_click=create_callable(self.canvas.set_color, (255, 0, 0))
        )
        self.add_item(self.set_red_color_button)

        # Get available shaps to select from
        available_shapes = self.canvas.get_available_shapes()
        position = [90, 100]
        size = [100, 35]
        for shape in available_shapes:
            self.add_item(
                item=Button(
                    controller=self.controller,
                    position=position,
                    size=[100, 35],
                    text=shape,
                    on_click=create_callable(self.canvas.change_currently_drawing, shape)
                )
            )
            # Update position for next button
            position = [position[0], position[1] + size[1] + 10]
