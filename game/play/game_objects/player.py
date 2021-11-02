"""
Module containing Player classes.
"""

import math

import pygame

from game.constants import SCREEN_SIZE
from game.helpers.file_handling import ImageLoader, Json


def rotate_vector(vector: list[int, int], angle: int):
    """
    Function returns rotated vector by angle degrees.

    :param vector: List [x, y] representing a vector
    :param angle: Number representing angle in degrees
    :return: List [x, y] representing rotated vector by angle degrees
    """
    rad_angle = math.radians(angle)
    new_x = vector[0] * math.cos(rad_angle) - vector[1] * math.sin(rad_angle)
    new_y = vector[0] * math.sin(rad_angle) + vector[1] * math.cos(rad_angle)
    return [new_x, new_y]


class Player:
    def __init__(self, controller, map, car, name, initial_position=[0, 0]):
        self.controller = controller
        self.screen = pygame.display.get_surface()
        self.map = map
        self.car = car
        self.name = name
        self.position = initial_position
        self.image = ImageLoader.load_transparent_image("game/assets/objects/cars/testing_car.png")
        self.size = self.image.get_size()
        self.screen_position = [SCREEN_SIZE[0] // 2 - self.size[0] // 2, SCREEN_SIZE[1] // 2 - self.size[1] // 2]

    def angle_to_speed_vector(self):
        return [math.cos(math.radians(self.angle)) * self.velocity, math.sin(math.radians(self.angle)) * self.velocity]

    def read_input(self):
        if self.controller.key_pressed["right"]:
            self.car.steering_angle -= self.car.turning_velocity * self.car.dt
        elif self.controller.key_pressed["left"]:
            self.car.steering_angle += self.car.turning_velocity * self.car.dt
        else:
            self.car.steering_angle = 0

        if self.controller.key_pressed["up"]:
            self.car.throttle += self.car.throttle_acceleration * self.car.dt
        else:
            self.car.throttle = 0
        if self.controller.key_pressed["down"]:
            self.car.break_throttle += self.car.throttle_acceleration * self.car.dt
        else:
            self.car.break_throttle = 0

    def update(self):
        # Read input data
        self.read_input()
        self.car.update()
        # Update map position at end
        self.map.offset = self.car.position

    def draw(self):
        self.car.draw()
