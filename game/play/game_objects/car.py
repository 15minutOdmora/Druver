"""
Module for the car class and all related functions.
"""

import math

import pygame

from game.constants import SCREEN_SIZE, Paths, join_paths
from game.helpers.file_handling import ImageLoader, Json


class Car:
    """@DynamicAttrs"""
    def __init__(self, controller, current_map, car_name: str, initial_position=[0, 0]):
        self.screen = pygame.display.get_surface()
        self.controller = controller
        self.position = initial_position
        self.map = current_map
        # Load car data
        self.name = car_name
        self.folder = join_paths(Paths.cars, self.name)
        self.images = ImageLoader.load_transparent_folder(join_paths(self.folder, "images"))
        self.number_of_images = len(self.images)
        self.angle_per_image = 360 // self.number_of_images  # This is the size of angle between each image
        self.image_index = 0
        self.image_size = self.images[0].get_size()
        self.half_image_size = self.image_size[0] // 2, self.image_size[1] // 2
        self.screen_position = [SCREEN_SIZE[0] // 2 - self.image_size[0] // 2, SCREEN_SIZE[1] // 2 - self.image_size[1] // 2]
        # Load configuration and update with base configuration so there are no attributes missing
        config = Json.load(join_paths(self.folder, "config.json"))
        base_config = Json.load(join_paths(Paths.cars, "base_config.json"))
        base_config.update(config)
        self.config = base_config

        # Pre set car data
        self.throttle = 0  # Number between 0 and 1
        self.brake_throttle = 0
        self.steering_angle = 0
        self.velocity = 0
        self.angle = 0

        # Load car specs from config file as attributes
        for key, value in self.config.items():
            setattr(self, key, value)

        self.controller.development.add(self.__draw_data)

    @property
    def dt(self):
        return self.controller.dt

    def update_throttle(self):
        self.throttle = min(1, self.throttle)
        self.brake_throttle = min(1, self.brake_throttle)

    def update_velocity(self):
        current_acceleration = self.throttle * self.acceleration * self.dt
        self.velocity += current_acceleration * self.dt

    def update_steering(self):
        # Ackerman steering model
        if self.steering_angle:
            turning_radius = self.length / math.sin(math.radians(self.steering_angle))
            angular_velocity = self.velocity / turning_radius
        else:
            angular_velocity = 0
        velocity_vector = pygame.math.Vector2(self.velocity, 0).rotate(-self.angle) * self.dt
        self.position[0] += velocity_vector.x
        self.position[1] += velocity_vector.y
        self.angle += math.degrees(angular_velocity) * self.dt

    def update_angle(self):
        if self.angle < 0:
            self.angle = 360 + self.angle
        elif self.angle > 360:
            self.angle = self.angle - 360

    def update_current_image_index(self):
        self.image_index = min(int((self.angle - 90) // self.angle_per_image), self.number_of_images - 1)

    def update_collision(self):
        center_pos = (self.position[0] + self.half_image_size[0], self.position[1] + self.half_image_size[1])
        val = self.map.get_mask_value(center_pos)
        if val[0] != 255:
            self.angle += 180

    def update(self):
        self.update_throttle()
        self.update_velocity()
        self.update_steering()
        self.update_angle()
        self.update_collision()
        self.update_current_image_index()

    def draw(self):
        self.screen.blit(self.images[self.image_index], self.screen_position)

    def __draw_data(self):
        # Car
        car = f"Car"
        car_surface = self.controller.development.font.render(car, True, (255, 255, 255))
        self.screen.blit(car_surface, (20, 300))
        # Throttle
        thr = f"Throttle: {self.throttle}, Brake: {self.brake_throttle}"
        thr_surface = self.controller.development.font.render(thr, True, (255, 255, 255))
        self.screen.blit(thr_surface, (30, 320))
        # Velocity
        vel = f"Velocity: {self.velocity}"
        vel_surface = self.controller.development.font.render(vel, True, (255, 255, 255))
        self.screen.blit(vel_surface, (30, 340))
        # Acceleration
        acc = f"Acceleration: {self.acceleration}"
        acc_surface = self.controller.development.font.render(acc, True, (255, 255, 255))
        self.screen.blit(acc_surface, (30, 360))
        # Steering
        ster = f"Steering angle: {self.steering_angle}"
        ster_surface = self.controller.development.font.render(ster, True, (255, 255, 255))
        self.screen.blit(ster_surface, (30, 380))
        # Position
        pos = f"Position: ({int(self.position[0])}, {int(self.position[1])})"
        pos_surface = self.controller.development.font.render(pos, True, (255, 255, 255))
        self.screen.blit(pos_surface, (30, 400))
