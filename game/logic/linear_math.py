"""
Module for different linear algebra math classes such as Vectors, Planes, ...
"""

import math


class Vector:
    """
    Class representing Vector. Each vector has length, dimension properties. Calling norm property returns new
    normalized vector.
    Possible operations between and on vectors: +, -, *, round, str
    """
    def __init__(self, values: list[int]):
        """
        :param values: list[int, ...] list containing values for each dimension of vector, i, j, k, ...
        """
        self.values = values

    @property
    def length(self) -> float:
        return math.sqrt(sum([val ** 2 for val in self.values]))

    @property
    def dimension(self) -> int:
        return len(self.values)

    @property
    def norm(self) -> "Vector":
        length = self.length
        return Vector(values=[val / length for val in self.values])

    def check_operation_is_possible(self, other) -> bool:
        """
        Method checks if any kind of operation is possible between self and other.
        :param other: Vector
        :return: bool
        """
        if type(other) is Vector:
            if self.dimension == other.dimension:
                return True
        raise ValueError(f"Vector: Operation not possible between {self} and {other}, types do not match.")

    def __add__(self, other) -> "Vector":
        if self.check_operation_is_possible(other):
            return Vector(values=[val + other.values[i] for i, val in enumerate(self.values)])

    def __sub__(self, other) -> "Vector":
        return self.__add__(other * -1)

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Vector(values=[val * other for val in self.values])
        elif isinstance(other, Vector):
            self.check_operation_is_possible(other)
            return sum([val * other.values[i] for i, val in enumerate(self.values)])

    def __neg__(self) -> "Vector":
        values = [val * -1 for val in self.values]
        return Vector(values)

    def __round__(self, n) -> "Vector":
        values = [round(val, n) for val in self.values]
        return Vector(values)

    def __iter__(self):
        for val in self.values:
            yield val

    def __str__(self) -> str:
        return f"<Vector: {self.values}>"

    def __repr__(self) -> str:
        return str(self)


def rotate_2d_vector(vector: Vector, angle: float) -> Vector:
    """
    Function rotates 2-dimensional vector by angle degrees anticlockwise.
    :param vector: Vector to rotate
    :param angle: float or int representing degrees to rotate by
    :return: Vector rotated vector of same size
    """
    if vector.dimension != 2:
        raise ValueError(f"rotate_2d_vector: Passed vector {vector} is not 2-dimensional.")
    ang = math.radians(angle)
    _x = vector.values[0]
    _y = vector.values[1]
    x = math.cos(ang) * _x - math.sin(ang) * _y
    y = math.sin(ang) * _x + math.cos(ang) * _y
    return Vector([x, y])


def rotate_3d_vector(vector: Vector, angle: float, around_axis: str = "x"):
    if vector.dimension != 3:
        raise ValueError(f"rotate_3d_vector: Passed vector {vector} is not 3-dimensional.")
    ang = math.radians(angle)
    _x, _y, _z = vector.values[0], vector.values[1], vector.values[2]
    if around_axis == "x":
        x = _x
        y = math.cos(ang) * _y - math.sin(ang) * _z
        z = math.sin(ang) * _y + math.cos(ang) * _z
    elif around_axis == "y":
        x = math.cos(ang) * _x + math.sin(ang) * _z
        y = _y
        z = - math.sin(ang) * _x + math.cos(ang) * _z
    elif around_axis == "z":
        x = math.cos(ang) * _x - math.sin(ang) * _y
        y = math.sin(ang) * _x + math.cos(ang) * _y
        z = _z
    else:
        raise ValueError(f"rotate_3d_vector: Passed around_axis = {around_axis} parameter is incorrect.")
    return Vector([x, y, z])


def make_vector(val):
    """
    Function creates vector from passed value. Raises error if not possible.
    :param val: list, tuple or Vector
    :return: Vector(val)
    """
    if isinstance(val, Vector):
        return val
    elif isinstance(val, list):
        return Vector(val)
    elif isinstance(val, tuple):
        return Vector(list(val))
    else:
        raise ValueError(f"make_vector: {val} can not be converted to vector.")


class Plane:
    """
    Class representing a plane, defined by a point and a normalized vector rectangular to self plane.
    """
    def __init__(self, point, vector):
        """
        :param point: list, tuple or Vector defining point on plane
        :param vector: list, tuple or Vector defining normalized vector rectangular to plane
        """
        self.p = make_vector(point)
        n = make_vector(vector)
        if n.length != 1:
            self.n = n.norm
        else:
            self.n = n

    def is_on_plane(self, point: Vector) -> bool:
        """
        Method checks if passed point(defined as vector) is lying on plane.
        :param point: Vector representing point
        :return: bool if on plane or not
        """
        if ((point - self.p) * self.n) == 0:
            return True
        return False

    def line_intersection(self, line: "Line") -> Vector:
        """
        Method finds intersection between self plane and some line. If intersection does not exist it raises and error.
        :param line: Line to check intersection
        :return: Vector representing point of intersection
        """
        # Check if intersection exists
        if round(line.v * self.n) == 0:
            raise ValueError(f"Plane.line_intersection: Line is parallel to line {line}")
        else:
            # Find d scalar
            d = ((self.p - line.p) * self.n) * (1 / (line.v * self.n))
            return line.p + (line.v * d)

    def __str__(self):
        return f"<Plane: point = {self.p}, vector = {self.n}>"

    def __repr__(self):
        return str(self)


class Line:
    """
    Class representing a line, defined by a point on line and a normalized vector pointing in direction of line.
    """
    def __init__(self, point, vector):
        """
        :param point: list, tuple or Vector defining point on line
        :param vector: list, tuple or Vector defining normalized vector in direction of plane
        """
        self.p = make_vector(point)
        v = make_vector(vector)
        if v.length != 1:
            self.v = v.norm
        else:
            self.v = v

    def plane_intersection(self, plane: Plane) -> Vector:
        """
        Method finds intersection between self line and some plane. If intersection does not exist it raises and error.
        :param plane: Plane to check intersection
        :return: Vector representing point of intersection
        """
        # Check if intersection exists
        if round(self.v * plane.n) == 0:
            raise ValueError(f"Line.plane_intersection: Line is parallel to plane {plane}")
        else:
            # Find d scalar
            d = ((plane.p - self.p) * plane.n) * (1 / (self.v * plane.n))
            return self.p + (self.v * d)

    def __str__(self):
        return f"<Line: point = {self.p}, vector = {self.v}>"

    def __repr__(self):
        return str(self)
