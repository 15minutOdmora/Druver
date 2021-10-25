"""
Module containing Player classes.
"""


class Player:
    def __init__(self, name, car_name):
        self.name = name
        self.health = 100
        self.gun = None  # TODO: Future implementation

        # TODO: Load data from json object about car
        self.car_name = car_name
        self.position = [600, 700]
        self.speed = 0
        self.acceleration = 0.5
        self.deceleration = 0.6
        self.angle = 0  # In degrees

    def read_input(self):
        if self.controller.key_pressed["right"]:
            self.speed += 2
        if self.controller.key_pressed["left"]:
            self.speed -= 2
        if self.controller.key_pressed["up"]:
            self.speed += self.acceleration
        if self.controller.key_pressed["down"]:
            self.speed += self.deceleration

    def update(self):
        # Read input data
        self.read_input()


    def draw(self):
        pass
