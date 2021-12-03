"""
Page for generating car boundaries and tyre positions on shifted perspective view.
"""

from game.constants import SCREEN_SIZE, Paths
from game.helpers.helpers import create_callable
from game.helpers.file_handling import DirectoryReader, join_paths, Json
from game.pages.page import Page
from game.gui.canvas import Canvas, SetOfPoints, Point
from game.gui.button import Button
from game.gui.text import CustomText, Text
from game.gui.container import Container
from game.gui.carousel import HorizontalCarousel
from game.gui.grid import Grid
from game.gui.image import FolderImages, ResizableImage

from game.logic.car_boundries_rotation import CarBoundariesGenerator, get_relative_corner_positions, get_image_corner_positions


half_screen = SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2


class GenerateCarBoundariesPage(Page):
    """
    Page used for selecting car boundaries on first image of car -> preview all points (every angle) by iterating
    with the Next button, generate all points and save to cars config file using Generate button.
    """
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
        # Type of boundaries selection
        self.car_boundaries_color = (0, 0, 255)  # Blue color
        self.car_tyre_position_color = (255, 0, 0)  # Red color
        # Select car boundaries button
        self.add_item(
            item=Button(
                controller=self.controller,
                position=[400, 250],
                size=(130, 30),
                text="Select boundaries",
                on_click=create_callable(self.canvas.set_color, self.car_boundaries_color)
            )
        )
        self.add_item(
            item=Button(
                controller=self.controller,
                position=[400, 290],
                size=(130, 30),
                text="Select tyre positions",
                on_click=create_callable(self.canvas.set_color, self.car_tyre_position_color)
            )
        )
        # Save shape button
        self.save_shape_button = Button(
            controller=self.controller,
            position=[710, 285],
            size=(60, 35),
            text="Save",
            on_click=create_callable(self.save_drawn)
        )
        self.add_item(self.save_shape_button)
        # Status label
        self.status_label = Text(
            position=[780, 285],
            text="Select shapes"
        )
        self.add_item(self.status_label)
        # Check next button
        self.check_next_button = Button(
            controller=self.controller,
            position=[550, 330],
            size=(100, 35),
            text="Check next",
            on_click=create_callable(self.check_next)
        )
        self.check_next_button.visible = False
        self.add_item(self.check_next_button)
        # Generate all button
        self.generate_all_button = Button(
            controller=self.controller,
            position=[660, 330],
            size=(100, 35),
            text="Generate all",
            on_click=create_callable(self.generate_all)
        )
        self.generate_all_button.visible = False
        self.add_item(self.generate_all_button)

        self.point_dict = {}

        self.currently_drawing_list = None
        self.boundaries_generator = None
        self.current_angle = 0
        self.angle_increment = 360 / self.folder_images.number_of_images

        self.first_next = True  # To check if next has been clicked already
        self.saved = False

    def update(self) -> None:
        """
        Update status label and every other item attached to self.
        """
        # Do stuff
        if not self.saved:
            if len(self.point_dict) > 0:
                self.status_label.text = f"Saved {len(self.point_dict)} rectangles."
        # Call super method
        super(GenerateCarBoundariesPage, self).update()

    def draw(self) -> None:
        """
        Method draws every item attached to self and the currently drawing items saved in currently drawing list ->
        these are drawn generated points.
        """
        super(GenerateCarBoundariesPage, self).draw()
        if self.currently_drawing_list:
            for item in self.currently_drawing_list:
                item.draw()

    def reset(self) -> None:
        """
        Method resets canvas and all other attributes.
        """
        self.canvas.clear()
        self.folder_images.reset()
        self.close_generation()
        self.current_angle = 0
        self.currently_drawing_list = None
        self.status_label.text = "Select tyre positions"
        self.first_next = True

    def open_generation(self) -> None:
        """
        Method sets generate and next buttons to visible.
        """
        self.check_next_button.visible = True
        self.generate_all_button.visible = True

    def close_generation(self) -> None:
        """
        Method hides generate and next buttons.
        """
        self.check_next_button.visible = False
        self.generate_all_button.visible = False

    def save_drawn(self) -> None:
        """
        Method saves drawn rectangles (marking tyre positions and car boundaries) to attribute.
        Initializes boundaries_generator.
        """
        items = self.canvas.get_drawn_items()
        if len(items) == 0:
            self.status_label.text = "No shapes drawn on canvas!"
        else:
            # For every item fetched from canvas
            # Check color and save its relative positions to point_sets
            for item in items:
                if item.color == self.car_boundaries_color:
                    self.point_dict["boundaries"] = get_relative_corner_positions(
                        rect=item.get_points(),
                        relative_position=self.folder_images.position,
                        image_size=self.folder_images.size
                    )
                elif item.color == self.car_tyre_position_color:
                    self.point_dict["tyres"] = get_relative_corner_positions(
                        rect=item.get_points(),
                        relative_position=self.folder_images.position,
                        image_size=self.folder_images.size
                    )
            if len(self.point_dict) > 0 and "tyres" in self.point_dict.keys():  # If points were added, tyres exist
                self.open_generation()
                # Get centre point of tyres positions -> initialize boundaries generator
                tyres = self.point_dict["tyres"]
                center_point = [(tyres[0][0] + tyres[1][0]) // 2, (tyres[0][1] + tyres[2][1]) // 2]
                # TODO add input to get angle of projection
                self.boundaries_generator = CarBoundariesGenerator(
                    center_point=center_point,
                    z_angle_of_projection=25
                )
                # Add points to boundaries generator
                self.boundaries_generator.add_set_of_points(self.point_dict["tyres"], "tyres")
                if "boundaries" in self.point_dict.keys():
                    self.boundaries_generator.add_set_of_points(self.point_dict["boundaries"], "boundaries")

    def get_drawable_set_of_points(self, points: list[list[int]], color: tuple[int, int, int]) -> SetOfPoints:
        """
        Method creates a SetOfPoints based on passed points list.
        :param points: list[list[int]] points to add to set
        :param color: tuple[int, int, int] color of points
        :return: SetOfPoints a drawable object
        """
        set_of_points = SetOfPoints([])
        for point in points:
            relative_x = self.folder_images.x + point[0]
            relative_y = self.folder_images.y + point[1]
            set_of_points.add_point(
                Point(
                    screen=self.screen,
                    position=[relative_x, relative_y],
                    color=color,
                    width=3
                )
            )
        return set_of_points

    def set_drawing_of_generated_sets_of_points(self, points: list[tuple[str, list[list[int]]]]) -> None:
        """
        Method creates SetOfPoints for each point set (tyre, boundaries), saves it to currently_drawing list for
        drawing on screen.
        :param points: list[tuple[str, list[list[int]]]] list of tuples(name, set_of_points)
        """
        self.currently_drawing_list = []
        for name, set_of_points in points:
            if name == "tyres":
                color = self.car_tyre_position_color
            else:
                color = self.car_boundaries_color
            self.currently_drawing_list.append(self.get_drawable_set_of_points(set_of_points, color))

    def check_next(self) -> None:
        """
        Method generates next points rotated by centre of tyre rect. Angle gets incremented by angle_increment
        """
        if self.boundaries_generator:
            if self.first_next:
                self.first_next = False
            else:
                self.current_angle -= self.angle_increment
                self.folder_images.next_image()
            points = self.boundaries_generator.generate_points_rotated_by_angle(-self.current_angle)
            relative_to_image = self.get_relative_to_image(points)
            self.set_drawing_of_generated_sets_of_points(relative_to_image)
            self.canvas.clear()

    def get_relative_to_image(self, points: list[tuple[str, list[list[int]]]]) -> list[tuple[str, list[list[int]]]]:
        """
        Method calculates the relative positions of generated points based on upper left corner of image.
        :param points: list[tuple[str, list[list[int]]]] list of tuples(name, set_of_points)
        :return: list[tuple[str, list[list[int]]]] -> modified list
        """
        _points = []
        img_height = self.folder_images.height
        for name, point_set in points:
            le_points = []
            for point in point_set:
                le_points.append(
                    [point[0], img_height - point[1]]
                )
            _points.append((name, le_points))
        return _points

    def generate_all(self) -> None:
        """
        Method generates every rotated point for both rectangles (tyres, boundaries) for every image of car /
        for every angle. It then saves the points to the cars config file under points: {tyres:[], boundaries: []}
        """
        if self.boundaries_generator:
            # Get center point relative to image
            centre_point = self.boundaries_generator.center_point.values  # Is vector
            centre_point = [centre_point[0], self.folder_images.height - centre_point[1]]
            positions_dictionary = {
                "tyres": [],
                "boundaries": [],
                "centre": centre_point
            }
            self.reset()  # Reset everything
            for i in range(self.folder_images.number_of_images):
                if i != 0:
                    self.current_angle -= self.angle_increment
                points = self.boundaries_generator.generate_points_rotated_by_angle(-self.current_angle)
                relative_to_image = self.get_relative_to_image(points)
                for name, points in relative_to_image:
                    if name in positions_dictionary.keys():
                        positions_dictionary[name].append(points)
            self.status_label.text = f"Saved {len(positions_dictionary['tyres'])} tyre points " \
                                     f"and {len(positions_dictionary['boundaries'])} boundaries."
            # Save to config file of car
            Json.update(join_paths(Paths.cars, self.car_name, "config.json"), {"points": positions_dictionary})
            self.saved = True


class CarBoundariesPage(Page):
    """
    Development page for defining and generating car boundaries. Here we select the car we would like to
    generate points from, we then redirect to the generation page defined above.
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
