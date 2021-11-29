"""
Module containing the CarBoundariesGenerator class for generating car boundaries on a shifted perspective.
"""

from game.logic.linear_math import *


def get_relative_corner_positions(rect: list[list[int]], relative_position: list[int], image_size: list[int]):
    """
    Function calculates corner points of passed rectangle relative to a passed position.
    :param rect: list[list[int]] list of start position on screen and end position on screen [[start], [end]]
    :param relative_position: list[int] position on screen to which the calculated positions should be relative to.
    :param image_size: list[int] size of image the rectangle is placed above, y-axis is inverted on screen that is
                       why this is needed.
    :return: list of 4 lists containing each corner point of rectangle->[top-left, top-right, bottom-left, bottom-right]
    """
    # Get corner points
    start_pos, end_pos = rect[0], rect[1]
    width, height = end_pos[0] - start_pos[0], end_pos[1] - start_pos[1]
    # Get x, y values for every corner
    left_x = start_pos[0] - relative_position[0]
    right_x = start_pos[0] + width - relative_position[0]
    top_y = image_size[1] - (start_pos[1] - relative_position[1])
    bottom_y = image_size[1] - (start_pos[1] + height - relative_position[1])
    corner_points = [
        [left_x, top_y],
        [right_x, top_y],
        [left_x, bottom_y],
        [right_x, bottom_y]
    ]
    return corner_points


def get_image_corner_positions(image_size: list[int]) -> list[list[int]]:
    """
    Function returns the image corner positions on x-y plane where the bottom left corner of image
    is positioned at (0, 0).
    :param image_size: list[int] = [width, height] of image
    :return: list[list[int]] list of corner points on x-y plane
    """
    # Get image points, bottom left corner of image is on (0, 0)
    image_points = [
        [0, image_size[1]],
        list(image_size),
        [0, 0],
        [image_size[0], 0]
    ]
    return image_points


class CarBoundariesGenerator:
    """
    Class used for projecting points from one plane to another, rotating the point around a centre point at the second
    plane then projecting the point back to first plane. Described in the pdf file inside this directory.
    """
    def __init__(self,
                 center_point: list[int],
                 z_angle_of_projection: float,
                 ):
        """
        :param center_point: list[int] 2D point of rotation, gets converted to 3D point automatically
        :param z_angle_of_projection: float angle between planes. *Clockwise
        """
        self.fi = z_angle_of_projection  # Angle between planes
        self.zero_vector = Vector([0, 0, 0])
        self.sigma_n = Vector([0, 0, 1])  # Norm vector of sigma plane
        self.pi_n = rotate_3d_vector(self.sigma_n, -self.fi, around_axis="x")  # Norm vector of pi plane
        # Sigma plane is the first plane, pi plane is shifted by an angle (based on rendering)
        self.sigma_plane = Plane(self.zero_vector, self.sigma_n)
        self.pi_plane = Plane(self.zero_vector, self.pi_n)
        # Projection vectors
        self.v = Vector([0, 0, -1])
        self.u = self.v * -1
        # Center point on sigma plane and its projection on pi plane
        self.center_point = Vector(center_point + [0])
        self.center_v_line = Line(self.center_point, self.v)
        self.center_point_pi_plane = self.center_v_line.plane_intersection(self.pi_plane)
        # For later use of saving initial vectors (for each rectangle corner) in lists
        self.sets_of_vectors = []
        self.sets_names = []

    def add_set_of_points(self, points: list[list[int]], name: str = "") -> None:
        """
        Method adds a set of points (rectangle corners) to self along with the name of the rectangle.
        :param points: list[list[int]]
        :param name: str name representing points
        """
        vectors = []
        for point in points:
            if len(point) == 2:
                vectors.append(Vector(point + [0]))  # Add 3rd dimension
            else:
                vectors.append(Vector(point))
        self.sets_of_vectors.append(vectors)
        self.sets_names.append(name)

    def project_and_rotate_point(self, point: Vector, angle: float) -> Vector:
        """
        Method projects point to pi plane, rotates it around centre point by given angle and projects it back to
        sigma plane.
        :param point: Vector to project and rotate
        :param angle: Angle to rotate the point around centre point *CounterClockwise
        :return: Vector rotated vector
        """
        from_center_point = point - self.center_point
        point_v_line = Line(from_center_point, self.v)
        projected_vector = point_v_line.plane_intersection(self.pi_plane)
        # Rotate vector to sigma plane, rotate by angle, rotate back to pi plane
        sigma_vector = rotate_3d_vector(projected_vector, self.fi, around_axis="x")
        rotated_vector = rotate_3d_vector(sigma_vector, angle, around_axis="z")
        rotated_pi_vector = rotate_3d_vector(rotated_vector, -self.fi, around_axis="x")
        # Project vector back to sigma plane
        vector_u_line = Line(rotated_pi_vector, self.u)
        vector = vector_u_line.plane_intersection(self.sigma_plane)
        final_vector = self.center_point + vector
        return round(final_vector, 0).values

    def generate_points_rotated_by_angle(self, angle: float) -> tuple[str, list[list[int]]]:
        """
        Method generates every corner of set rectangles (in self.sets_of_vectors) rotated by angle. Returns
        a list containing tuples[name, rotated-points].
        :param angle: float angle to rotate point around center point *CounterClockwise
        :return: tuple[str, list[list[int]]] list of tuples[name, set_of_corner_points_of_rectangle=list]
        """
        # Go over every set
        sets_of_rotated_points = []
        for i, points in enumerate(self.sets_of_vectors):
            # Rotate every point
            rotated_points = []
            for point in points:
                rotated_points.append(self.project_and_rotate_point(point, angle))
            sets_of_rotated_points.append((self.sets_names[i], rotated_points))
        return sets_of_rotated_points
