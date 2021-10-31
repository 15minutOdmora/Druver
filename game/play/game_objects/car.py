"""
Module for the car class and all related functions.
"""

import math

import pygame

from game.constants import SCREEN_SIZE
from game.helpers.file_handling import ImageLoader


class Car:
    def __init__(self, game, map, name, initial_position=[0, 0]):
        self.game = game
        self.screen = self.game.screen
        self.screen_position = [SCREEN_SIZE[0] // 2 - self.size[0] // 2, SCREEN_SIZE[1] // 2 - self.size[1] // 2]
        self.controller = self.game.controller
        self.position = initial_position

        # TODO: Load data from json object about car
        self.turning_velocity = 0.6
        self.angle = 0  # In degrees

        self.acceleration = 0.023
        self.deceleration = 0.019
        self.speed = 0
        self.max_speed = 5

    def rotate_image(self):
        rotated_image = pygame.transform.rotate(self.image, self.angle + 90)
        new_rect = rotated_image.get_rect(center=self.image.get_rect(topleft=self.screen_position).center)
        return rotated_image, new_rect

    def angle_to_speed_vector(self):
        return [math.cos(math.radians(self.angle)) * self.speed, math.sin(math.radians(self.angle)) * self.speed]

    def read_input(self):
        self.angle -= self.controller.key_pressed["right"] * self.turning_velocity
        self.angle += self.controller.key_pressed["left"] * self.turning_velocity
        if self.controller.key_pressed["up"]:
            self.speed += self.acceleration
        else:
            self.speed -= self.deceleration
        if self.controller.key_pressed["down"]:
            self.speed += self.deceleration

    def update(self):
        # Read input data
        self.read_input()
        self.speed = max(0, self.speed)
        self.speed = min(self.max_speed, self.speed)
        movement_change_vector = self.angle_to_speed_vector()
        self.position[0] -= movement_change_vector[0]
        self.position[1] += movement_change_vector[1]
        # Update map position at end
        self.map.offset = self.position

    def draw(self):
        rotated_image, new_rect = self.rotate_image()
        self.screen.blit(rotated_image, new_rect)