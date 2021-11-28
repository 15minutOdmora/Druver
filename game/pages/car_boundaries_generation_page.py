"""
Page for generating car boundaries and tyre positions on shifted perspective view.
"""

from game.constants import SCREEN_SIZE, Paths
from game.helpers.helpers import create_callable
from game.helpers.file_handling import DirectoryReader, join_paths
from game.pages.page import Page
from game.gui.canvas import Canvas, SetOfPoints, Point
from game.gui.button import Button
from game.gui.text import CustomText, Text
from game.gui.container import Container
from game.gui.carousel import HorizontalCarousel
from game.gui.grid import Grid
from game.gui.image import FolderImages, ResizableImage

from game.logic.linear_math import *


half_screen = SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2


def get_relative_corner_positions(rect, relative_position, image_size):
    """
    Function calculates corner points of passed rectangle relative to a passed position.
    :param rect: list[lit[int]] list of start position on screen and end position on screen [[start], [end]]
    :param relative_position: list[int] position on screen to which the calculated positions should be relative to.
    :return: list of 4 lists containing each corner point of rectangle -> [top-left, top-right, bottom-left, bottom-right]
    """
    # Get image points, bottom left corner of image is on (0, 0)
    image_points = [
        [0, image_size[1]],
        list(image_size),
        [0, 0],
        [image_size[0], 0]
    ]
    # Get corner points
    start_pos, end_pos = rect[0], rect[1]
    width, height = end_pos[0] - start_pos[0], end_pos[1] - start_pos[1]
    relative_pos = relative_position
    left_x = start_pos[0] - relative_pos[0]
    right_x = start_pos[0] + width - relative_pos[0]
    top_y = image_size[1] - (start_pos[1] - relative_pos[1])
    bottom_y = image_size[1] - (start_pos[1] + height - relative_pos[1])
    corner_points = [
        [left_x, top_y],
        [right_x, top_y],
        [left_x, bottom_y],
        [right_x, bottom_y]
    ]
    return image_points, corner_points


class GenerateCarBoundariesPage(Page):
    def __init__(self, controller, car_name_func):
        super().__init__(controller)
        self.car_name = car_name_func()  # Fetch selected cars name

        # Back button
        self.add_item(
            item=Button(
                controller=self.controller,
                position=[10, 10],
                size=[60, 30],
                text="Back",
                on_click=create_callable(self.controller.go_back)
            )
        )
        # FolderImages
        self.folder_images = FolderImages(
            folder_path=join_paths(Paths.cars, self.car_name, "images"),
            position=[550, 170]
        )
        self.add_item(self.folder_images)
        # Canvas
        self.canvas = Canvas(
            self.controller,
            position=[550, 170],
            size=self.folder_images.size
        )
        self.canvas.set_color((255, 0, 0))
        self.canvas.change_currently_drawing("rectangle")
        self.add_item(self.canvas)
        # Reset button
        self.add_item(
            item=Button(
                controller=self.controller,
                position=[550, 130],
                size=(60, 30),
                text="Reset",
                on_click=create_callable(self.reset)
            )
        )
        # Canvas undo button
        self.add_item(
            item=Button(
                controller=self.controller,
                position=[640, 130],
                size=(60, 30),
                text="Undo",
                on_click=create_callable(self.canvas.undo)
            )
        )
        # Save shape button
        self.save_shape_button = Button(
            controller=self.controller,
            position=[710, 285],
            size=(60, 35),
            text="Save",
            on_click=create_callable(self.generate)
        )
        self.add_item(self.save_shape_button)
        # Save rectangle label
        self.save_rect_label = Text(
            text="Select corner points of car.",
            position=[780, 285]
        )
        self.add_item(self.save_rect_label)
        # Invisible next angle and generate all buttons.
        self.next_image_button = Button(
            controller=self.controller,
            position=[630, 330],
            size=(70, 35),
            text="Next angle",
            on_click=create_callable(self.generate_next)
        )
        self.next_image_button.visible = False
        self.add_item(self.next_image_button)

        self.image_points = None
        self.corner_points = None

        self.current_angle = 0

        self.currently_drawing = None

    def update(self) -> None:
        # Do stuff
        if self.image_points:
            self.save_rect_label.text = "Saved"
        # Call super method
        super(GenerateCarBoundariesPage, self).update()

    def draw(self) -> None:
        super(GenerateCarBoundariesPage, self).draw()
        if self.currently_drawing:
            self.currently_drawing.draw()

    def reset(self):
        self.folder_images.reset()
        self.canvas.clear()
        self.image_points, self.corner_points = None, None
        self.save_rect_label.text = "Select corner points of car."
        self.next_image_button.visible = False
        self.current_angle = 0
        self.currently_drawing = None

    def generate(self):
        items = self.canvas.get_drawn_items()
        if len(items) != 1:
            self.save_rect_label.text = "Only one Rectangle should be drawn!"
        else:
            # Get relative corner points of selected rectangle
            rect = items[0].get_points()
            self.image_points, self.corner_points = get_relative_corner_positions(
                rect,
                self.folder_images.position,
                self.folder_images.size
            )
            self.next_image_button.visible = True
            self.generate_next()

    def generate_next(self):
        self.folder_images.next_image()
        self.canvas.clear()

        v = Vector([0, 0, -1])
        u = v * -1
        self.current_angle -= 5.07
        sigma_normal_vector = [0, 0, 1]
        sigma_plane = Plane([0, 0, 0], sigma_normal_vector)
        pi_normal_vector = [0] + rotate_2d_vector(Vector([0, 1]), -25).values
        pi_plane = Plane([0, 0, 0], pi_normal_vector)
        projected_image_points = []
        for _point in self.image_points:
            point = _point + [0]  # Add third dimension z
            # Create line and find intersection with pi plane
            line = Line(point=point, vector=v)
            projected_image_points.append(line.plane_intersection(pi_plane))
        projected_corner_points = []
        for _point in self.corner_points:
            point = _point + [0]  # Add third dimension z
            # Create line and find intersection with pi plane
            line = Line(point=point, vector=v)
            projected_corner_points.append(line.plane_intersection(pi_plane))
        # Find center of corner points
        top_left = projected_corner_points[0]
        bottom_right = projected_corner_points[3]
        center_point = (top_left + bottom_right) * 0.5

        rotated_corner_points = []
        for vector in projected_corner_points:
            # Create vector from center point to point
            center_point_vector = vector - center_point
            rotated_to_xy_cpv = rotate_3d_vector(center_point_vector, 25, around_axis="x")
            rotated_center_point = rotate_3d_vector(rotated_to_xy_cpv, self.current_angle, around_axis="z")
            rotated_cpv = rotate_3d_vector(rotated_center_point, -25, around_axis="x")
            line = Line(rotated_cpv, u)
            rotated_corner_points.append(round(line.plane_intersection(sigma_plane), 1).values[:2])
        cp_line = Line(center_point, u)
        sigma_center_point = cp_line.plane_intersection(sigma_plane).values[:2]
        sigma_center_point = [sigma_center_point[0], self.folder_images.height - sigma_center_point[1]]
        self.currently_drawing = None
        set_of_points = SetOfPoints([])
        for point in rotated_corner_points:
            on_screen_point = [point[0] + self.folder_images.x + sigma_center_point[0], point[1] + self.folder_images.y + sigma_center_point[1]]
            set_of_points.add_point(
                point=Point(
                    screen=self.screen,
                    position=on_screen_point,
                    color=(255, 0, 0),
                    width=3
                )
            )
        self.currently_drawing = set_of_points
        print(self.current_angle // 5, self.folder_images.current_index)


class CarBoundariesPage(Page):
    """
    Development page for defining and generating car boundaries.
    """
    def __init__(self, controller):
        super().__init__(controller)

        # Back button
        self.add_item(
            item=Button(
                controller=self.controller,
                position=[10, 10],
                size=[60, 30],
                text="Back",
                on_click=create_callable(self.controller.go_back)
            )
        )
        # Carousel
        self.carousel = HorizontalCarousel(
            self.controller,
            item_size=[310, 400],
            position=[0, 150],
            size=[1280, 400],
            spacing=30
        )
        self.carousel.not_selected_item_resize_factor = 0.4
        self.carousel.visible = False
        car_previews = DirectoryReader.get_car_previews()
        for car in car_previews:
            cont = Container(
                position=[0, 0],
                size=[310, 400],
                visible=False,
                resizable=True
            )
            cont.add_item(
                item=CustomText(text=car["name"], size=80),
                relative_position=[25, 25]
            )
            cont.add_item(
                item=ResizableImage(join_paths(car["preview"], "0032.png")),
                relative_position=[5, 130]
            )
            self.carousel.add_item(cont, name=car["name"])
        self.add_item(self.carousel)
        # Left button
        self.scroll_left_button = Button(
            self.controller,
            [20, half_screen[1] - 50],
            size=(20, 100),
            on_click=create_callable(self.carousel.scroll_left),
            text=""
        )
        self.add_item(self.scroll_left_button)
        # Right button
        self.scroll_right_button = Button(
            self.controller,
            [1240, half_screen[1] - 50],
            size=(20, 100),
            on_click=create_callable(self.carousel.scroll_right),
            text=""
        )
        self.add_item(self.scroll_right_button)
        # Continue button
        self.continue_button = Button(
            controller=self.controller,
            position=[400, 600],
            size=(130, 35),
            text="Save and continue",
            on_click=create_callable(
                self.controller.redirect_to_page,
                "GenerateCarBoundariesPage",
                car_name_func=create_callable(self.carousel.get_currently_selected)
            )
        )
        self.add_item(self.continue_button)
